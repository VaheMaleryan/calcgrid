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

    def test_automation_never_discards_source_changes(self):
        self.assertNotIn('"checkout", "--", "dist/", "engine/"', inspect.getsource(autopilot.run_autopilot_cycle))


if __name__ == '__main__':
    unittest.main()
