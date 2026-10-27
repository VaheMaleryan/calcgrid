"""Regression checks for user data handling, reversibility, and deployment privacy."""
import ast
import inspect
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'engine'))
import autopilot
import build_site
from catalog_data import TOOLS_CATALOG


class RuntimeRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the established minimal DOM harness; assertions below test new failure cases.
        tree = ast.parse(inspect.getsource(autopilot.run_math_and_runtime_tests))
        cls.harness = next(ast.literal_eval(n.value) for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'node_harness' for t in n.targets))
        cls.harness = cls.harness.split('const results = {};')[0]
        cls.harness = cls.harness.replace("makeEl('csv-audit-input', customInputs.csv || cfg.sample_csv);", "makeEl('csv-audit-input', customInputs.csv !== undefined ? customInputs.csv : cfg.sample_csv); makeEl('csv-audit-status');")

    def run_js(self, assertions):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / 'test.js'
            catalog = Path(directory) / 'catalog.json'
            script.write_text(self.harness + "\nconst assert = require('node:assert/strict');\n" + assertions)
            catalog.write_text(json.dumps(TOOLS_CATALOG))
            result = subprocess.run(['node', str(script), str(ROOT / 'dist/assets/tools-runtime.js'), str(catalog)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_csv_quoted_fields_and_html_injection(self):
        self.run_js(r'''
const tool = tools.find(t => t.tool_type === 'csv_auditor');
const csv = '\uFEFFtx_id,provider,gross_usd,actual_net_usd\r\n"<img src=x onerror=alert(1)>, client",wise,100,95.21'.replace('\\uFEFF','\uFEFF');
const run = runToolInSandbox(tool, '', {csv});
assert.equal(run.elements['out-audit-gross'].textContent, '$100.00');
assert.equal(run.elements['csv-audit-body'].children.length, 1);
assert.ok(run.elements['csv-audit-body'].children[0].innerHTML.includes('&lt;img'));
assert.ok(!run.elements['csv-audit-body'].children[0].innerHTML.includes('<img'));
''')

    def test_csv_invalid_data_cannot_reuse_previous_results(self):
        self.run_js(r'''
const tool = tools.find(t => t.tool_type === 'csv_auditor');
const header = 'tx_id,provider,gross_usd,actual_net_usd\n';
for (const csv of ['',header+'x,unknown,100,90',header+'x,wise,NaN,90',header+'x,wise,-1,90',header+'x,wise,Infinity,90',header+'"x,wise,100,90',header+Array(51).fill('x,wise,100,90').join('\n')]) {
 const run = runToolInSandbox(tool, '', {csv});
 assert.equal(run.elements['out-audit-gross'].textContent, '$0.00');
 assert.ok(run.elements['csv-audit-status'].textContent.length > 0);
}
''')

    def test_reverse_solver_impossible_and_zero_target(self):
        self.run_js(r'''
const corridor = tools.find(t => t.tool_type === 'corridor_engine');
const bad = runToolInSandbox(corridor, '?country=AM&tax=60&origin_pct=90');
assert.equal(bad.elements['out-reverse'].textContent, 'Not achievable');
const zero = runToolInSandbox(corridor, '?target_net=0&origin_fix=0&tax=0&origin_pct=0');
assert.equal(zero.elements['out-reverse'].textContent, '$0.00');
const fee = tools.find(t => t.tool_type === 'fee_calc');
const fullFee = runToolInSandbox(fee, '', {pct:100,fx:0});
assert.equal(fullFee.elements['out-reverse'].textContent, 'Not achievable');
assert.equal(fullFee.elements['out-net'].textContent, '$0.00');
''')

    def test_corridor_reverse_round_trip_all_countries(self):
        self.run_js(r'''
const tool = tools.find(t => t.tool_type === 'corridor_engine');
const money = s => Number(s.replace(/[$,]/g,''));
for (const country of ['AM','GE','RS','PH','IN']) {
 for (const target of [1,100,1000,10000]) {
  const query = '?country='+country+'&target_net='+target+'&tax=1&origin_pct=10&origin_fix=0.99';
  const run = runToolInSandbox(tool,query);
  const gross = money(run.elements['out-reverse'].textContent);
  const roundTrip = runToolInSandbox(tool,query+'&amount='+gross);
  assert.ok(Math.abs(money(roundTrip.elements['out-net'].textContent)-target) <= 0.011, country+' '+target);
 }
}
''')

    def test_export_quotes_and_disarms_formulas(self):
        # Use the harness with Blob/URL capture added only to this test context.
        original = self.harness
        try:
            self.harness = original.replace("    URLSearchParams,", "    Blob: class { constructor(parts) { global.exportedCsv = parts[0]; } },\n    URLSearchParams,")
            self.harness = self.harness.replace("  vm.runInNewContext(runtimeCode, sandbox);", "  sandbox.URL = class extends URL { static createObjectURL(){ return 'blob:local'; } static revokeObjectURL(){} };\n  vm.runInNewContext(runtimeCode, sandbox);")
            self.harness = self.harness.replace("          addEventListener() {}", "          click() {}, addEventListener() {}")
            self.run_js(r'''
const tool = tools.find(t => t.tool_type === 'csv_auditor');
const run = runToolInSandbox(tool,'',{csv:'tx_id,provider,gross_usd,actual_net_usd\n"=1+2,client",wise,100,95.21'});
run.elements['btn-export-csv'].listeners.click();
assert.ok(global.exportedCsv.includes('"\'=1+2,client"'));
assert.ok(global.exportedCsv.startsWith('"tx_id","provider"'));
''')
        finally:
            self.harness = original

    def test_economic_edge_cases_do_not_invent_profit_or_safe_rates(self):
        self.run_js(r'''
const tool = mode => tools.find(t => t.config.mode === mode);
let run = runToolInSandbox(tool('roas'),'',{a:80,b:100,c:1500,d:2.5});
assert.equal(run.elements['val-r1'].textContent,'Not achievable');
assert.equal(run.elements['val-r3'].textContent,'$-2,437.50');
run = runToolInSandbox(tool('hourly_rate'),'',{a:48000,b:2400,c:25,d:99});
assert.equal(run.elements['val-r1'].textContent,'$4,200.00/hr');
for (const values of [{c:0},{d:100},{d:120}]) assert.equal(runToolInSandbox(tool('hourly_rate'),'',values).elements['val-r1'].textContent,'—');
assert.equal(runToolInSandbox(tool('ltv'),'',{c:0}).elements['val-r1'].textContent,'Unbounded at zero churn');
assert.equal(runToolInSandbox(tool('ltv'),'',{a:0,c:0}).elements['val-r1'].textContent,'$0.00');
assert.equal(runToolInSandbox(tool('pert'),'',{a:120,b:65,c:40}).elements['val-r1'].textContent,'—');
assert.equal(runToolInSandbox(tool('cro'),'',{a:10000,b:3,c:2,d:10}).elements['val-r3'].textContent,'-100.0');
''')

    def test_amd_currency_and_country_eligibility(self):
        self.run_js(r'''
const am = tools.find(t => t.slug === 'armenia-it-tax-turnover-calculator');
assert.equal(runToolInSandbox(am).elements['out-net'].textContent,'AMD 975,000.00');
const tool = tools.find(t => t.tool_type === 'corridor_engine');
const rs = runToolInSandbox(tool,'?country=RS');
assert.ok(!rs.elements['out-best-rail'].textContent.startsWith('Wise'));
const amRun = runToolInSandbox(tool,'?country=AM&tax=60');
assert.ok(amRun.elements['corridor-comparison-body'].children[3].innerHTML.includes('EXCLUDED'));
amRun.elements['in-country'].value = 'GE';
amRun.elements['in-country'].listeners.change();
assert.equal(Number(amRun.elements['in-tax-pct'].value),1);
''')

    def test_unicode_decoders_and_nested_schema_generation(self):
        self.run_js(r'''
const dev = mode => tools.find(t => t.config.dev_mode === mode);
const input = 'Բարեւ 🌍';
const encoded = Buffer.from(input).toString('base64');
assert.equal(runToolInSandbox(dev('base64'),'',{input:encoded,operation:'decode'}).elements['dev-output'].textContent,input);
assert.equal(runToolInSandbox(dev('base64'),'',{input:'hello%20world%23x',operation:'decode-url'}).elements['dev-output'].textContent,'hello world#x');
const token = Buffer.from('{"alg":"none"}').toString('base64url')+'.'+Buffer.from(JSON.stringify({name:input})).toString('base64url')+'.';
const jwt = runToolInSandbox(dev('jwt'),'',{input:token}).elements['dev-output'].textContent;
assert.ok(jwt.includes(input)); assert.ok(jwt.includes('SIGNATURE NOT VERIFIED'));
const schema = runToolInSandbox(dev('json_to_ts'),'',{input:'{"full name":"A","profile":{"id":2},"values":[1,"x"],"nullable":null}'}).elements['dev-output'].textContent;
assert.ok(schema.includes('"full name": string')); assert.ok(schema.includes('z.null()')); assert.ok(schema.includes('z.union([')); assert.ok(schema.includes('"id": number'));
''')

    def test_cron_validation_and_quoted_csv_conversion(self):
        self.run_js(r'''
const dev = mode => tools.find(t => t.config.dev_mode === mode);
for (const input of ['99 99 99 99 99','a b c d e','*/0 * * * *','5-2 * * * *']) assert.ok(runToolInSandbox(dev('cron'),'',{input}).elements['dev-output'].textContent.startsWith('Error:'));
assert.ok(runToolInSandbox(dev('cron'),'',{input:'*/15 9-17 * * 1-5'}).elements['dev-output'].textContent.startsWith('Valid'));
const csv = 'name,id,active\n"Doe, Jane",001,true';
const data = JSON.parse(runToolInSandbox(dev('csv_to_json'),'',{input:csv}).elements['dev-output'].textContent);
assert.deepEqual(data,[{name:'Doe, Jane',id:'001',active:true}]);
assert.ok(runToolInSandbox(dev('csv_to_json'),'',{input:'name,name\nx,y'}).elements['dev-output'].textContent.startsWith('Error:'));
const proto = JSON.parse(runToolInSandbox(dev('csv_to_json'),'',{input:'__proto__,value\nsafe,3'}).elements['dev-output'].textContent);
assert.equal(proto[0]['__proto__'],'safe');
''')

    def test_sql_literals_and_existing_utm_links_are_preserved(self):
        self.run_js(r'''
const dev = mode => tools.find(t => t.config.dev_mode === mode);
const sql = runToolInSandbox(dev('sql'),'',{input:"select 'select from where' as value from records where id=1"}).elements['dev-output'].textContent;
assert.ok(sql.includes("'select from where'"));
const utm = runToolInSandbox(dev('utm'),'',{input:'https://example.com/p?a=1&utm_source=old#details|Reddit|Organic_Post|Q4_Launch'}).elements['dev-output'].textContent;
const url = new URL(utm); assert.equal(url.hash,'#details'); assert.equal(url.searchParams.get('a'),'1'); assert.equal(url.searchParams.getAll('utm_source').length,1); assert.equal(url.searchParams.get('utm_source'),'reddit');
''')



class ReleaseBoundaries(unittest.TestCase):
    def test_private_paths_never_tracked_or_published(self):
        files = subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
        self.assertFalse([p for p in files if p.startswith(('logs/','private_products/','marketing_outbox/videos/','.env'))])
        self.assertFalse([p for p in (ROOT/'dist').rglob('*') if p.suffix in {'.zip','.mp4','.jsonl'}])

    def test_all_tool_pages_have_brand_social_and_accessible_structure(self):
        for tool in TOOLS_CATALOG:
            page = (ROOT/'dist/tools'/f"{tool['slug']}.html").read_text()
            with self.subTest(tool=tool['slug']):
                self.assertIn('og:image',page)
                self.assertIn('PayoutFolio',page)
                self.assertIn('id="main-content"',page)
                self.assertNotIn('{BRAND_NAME}',page)
                self.assertNotIn('dashboard.html',page)

    def test_static_runtime_sends_no_data(self):
        runtime = (ROOT/'dist/assets/tools-runtime.js').read_text()
        self.assertNotIn('window.fetch',runtime)
        self.assertNotIn('sendBeacon',runtime)
        self.assertIn("connect-src 'none'",(ROOT/'dist/_headers').read_text())

    def test_monetization_requires_explicit_approval(self):
        self.assertFalse(build_site.MONETIZATION_APPROVED)
        self.assertFalse(build_site.LEMON_SQUEEZY_CHECKOUT_URL)
        self.assertFalse(build_site.ADSENSE_CLIENT_ID)

    def test_cloudflare_urls_and_offline_links_are_separate(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            original = '<a href="../index.html">Home</a><a href="foo.html#bar">Tool</a><a href="https://example.com/legal.html">Reference</a><link rel="canonical" href="' + build_site.SITE_URL + '/tools/foo.html" />'
            page = output / 'page.html'
            page.write_text(original)
            with patch.object(build_site, 'DIST_DIR', output), patch.dict(build_site._LAUNCH_CFG, {'hosting_provider':'cloudflare'}):
                build_site.finalize_cloudflare_output()
            result = page.read_text()
            self.assertIn('href="../"', result)
            self.assertIn('href="foo#bar"', result)
            self.assertIn('https://example.com/legal.html', result)
            self.assertIn(build_site.SITE_URL + '/tools/foo"', result)
            self.assertIn('foo.html#bar', original)

    def test_automation_never_discards_source_changes(self):
        self.assertNotIn('"checkout", "--", "dist/", "engine/"', inspect.getsource(autopilot.run_autopilot_cycle))

    def test_private_cli_rejects_bad_amounts_and_protects_export(self):
        import zipfile
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            with zipfile.ZipFile(ROOT/'private_products/calcgrid-pro-offline-suite.zip') as archive:
                cli = folder/'reconcile.py'
                cli.write_bytes(archive.read('01_cli_batch_auditor/calcgrid_batch_reconciler.py'))
            source = folder/'transactions.csv'
            output = folder/'output.csv'
            for row in ['x,unknown,100,95','x,wise,NaN,95','x,wise,-1,95','x,wise,Infinity,95']:
                source.write_text('tx_id,provider,gross_usd,actual_net_usd\n'+row)
                result = subprocess.run([sys.executable,str(cli),'--input',str(source),'--output',str(output)],capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
            source.write_text('tx_id,provider,gross_usd,actual_net_usd\n=1+2,wise,100,95.21')
            result = subprocess.run([sys.executable,str(cli),'--input',str(source),'--output',str(output)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn("'=1+2",output.read_text())

    def test_social_disable_cannot_be_bypassed_by_direct_publish_call(self):
        from unittest.mock import patch
        import smm_pipeline
        with patch('urllib.request.urlopen',side_effect=AssertionError('No external publishing is allowed')):
            result = smm_pipeline.publish_verified_episode_via_api({'math_claims_verified':True},'fake-test-token','','')
        self.assertFalse(result['published'])
        self.assertIn('disabled',result['reason'])



if __name__ == '__main__':
    unittest.main()
