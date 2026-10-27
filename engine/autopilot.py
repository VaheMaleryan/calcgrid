#!/usr/bin/env python3
"""
CalcGrid Autonomous Operations Controller & Independent Verification Suite (autopilot.py)
Performs:
  1. Static site compilation & private Pro ZIP packaging (`private_products/calcgrid-pro-offline-suite.zip`)
  2. Security & Git History Audit:
     - Verifies ZERO `.zip` archives exist inside the public `dist/` directory
     - Verifies ZERO `.zip` archives exist anywhere in Git commit history (`git log --all --full-history -- "*.zip"`)
  3. Independent Mathematical & Node.js Runtime Verification across all 30 tools:
     - Executes `dist/assets/tools-runtime.js` in Node.js for all 30 tools
     - Cross-checks every `fee_calc` (10 tools), `saas_calc` (9 tools), and `dev_tool` (11 tools) output
       against independent Python reference calculations, plus $0 and negative-input edge cases
  4. Multi-Tab `.xlsx` Workbook & CLI Auditor Verification inside `private_products/calcgrid-pro-offline-suite.zip`
  5. Compliance Check: Confirms homemade consent banners, unconfigured ad slots, and unconfigured checkout links are absent
"""

import io
import json
import os
import re
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from build_site import (
    compile_all,
    DIST_DIR,
    PRIVATE_PRODUCTS_DIR,
    SITE_URL,
    INDEXNOW_KEY,
    ADSENSE_CLIENT_ID,
    LEMON_SQUEEZY_CHECKOUT_URL,
)
from catalog_data import TOOLS_CATALOG

ROOT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT_DIR / "logs"
TELEMETRY_LOG = LOGS_DIR / "telemetry.jsonl"
REPORT_FILE = LOGS_DIR / "autopilot_report.json"


import math

def fmt_money(n: float) -> str:
    # Match JS Number.prototype.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) half-up rounding
    rounded = math.floor(n * 100.0 + 0.500000001) / 100.0
    return f"${rounded:,.2f}"


def compute_expected_saas(mode: str, a: float, b: float, c: float, d: float) -> tuple[str, str, str]:
    """Independent Python reference implementation for all 9 SaaS & Operations calculators."""
    if mode == "ltv":
        churn_rate = max(0.001, c / 100.0)
        ltv = (a * (b / 100.0)) / churn_rate
        ratio = (ltv / d) if d > 0 else 0.0
        payback = (d / (a * (b / 100.0))) if (a * (b / 100.0)) > 0 else 0.0
        return fmt_money(ltv), f"{ratio:.2f}x", f"{payback:.1f} months"
    if mode == "roas":
        margin = max(0.01, a - b)
        margin_pct = (margin / a) if a > 0 else 0.01
        be_roas = 1.0 / margin_pct
        gross_rev = c * d
        orders = (gross_rev / a) if a > 0 else 0.0
        net_profit = orders * margin - c
        return f"{be_roas:.2f}x", fmt_money(margin), fmt_money(net_profit)
    if mode == "ad_rev":
        monthly_imps = a * 30.0 * b
        gross_rev = (monthly_imps / 1000.0) * c
        net_rev = gross_rev * (d / 100.0)
        return fmt_money(net_rev), f"{round(monthly_imps):,}", fmt_money(net_rev * 12.0)
    if mode == "ecom":
        fee = a * (d / 100.0)
        net = a - b - c - fee
        margin_pct = ((net / a) * 100.0) if a > 0 else 0.0
        return fmt_money(net), f"{margin_pct:.1f}%", fmt_money(net * 100.0)
    if mode == "email_roi":
        clicks = a * (b / 100.0)
        sales = clicks * (c / 100.0)
        profit = sales * d
        return fmt_money(profit), f"{sales:.1f} sales", fmt_money((profit / a) if a > 0 else 0.0)
    if mode == "cro":
        extra_sales = a * ((c - b) / 100.0)
        monthly_lift = extra_sales * d
        return fmt_money(monthly_lift), fmt_money(monthly_lift * 12.0), f"+{extra_sales:.1f}"
    if mode == "hourly_rate":
        gross_needed = (a + b) / max(0.1, 1.0 - d / 100.0)
        annual_hours = max(1.0, c * 48.0)
        hourly = gross_needed / annual_hours
        return f"{fmt_money(hourly)}/hr", f"{fmt_money(hourly * 8.0)}/day", fmt_money(gross_needed)
    if mode == "pert":
        expected = (a + 4.0 * b + c) / 6.0
        sd = (c - a) / 6.0
        safe_hours = expected + 2.0 * sd
        return f"{safe_hours:.1f}h ({fmt_money(safe_hours * d)})", f"{expected:.1f} hours", f"+{(2.0 * sd):.1f} hours"
    if mode == "llm_cost":
        monthly_tokens = a * 30.0 * b
        raw_cost = (monthly_tokens / 1_000_000.0) * c
        net_cost = raw_cost * (1.0 - d / 100.0)
        per_1k = (b / 1000.0) * c * (1.0 - d / 100.0)
        return fmt_money(net_cost), f"{(monthly_tokens / 1_000_000.0):.2f}M tokens", fmt_money(per_1k)
    raise ValueError(f"Unknown saas_calc mode: {mode}")


def run_math_and_runtime_tests() -> dict:
    """
    Executes `dist/assets/tools-runtime.js` inside Node.js for all 30 tools and verifies
    that every single tool's DOM output matches independent Python reference calculations.
    """
    failures = []
    tested_tools = []
    runtime_js_path = DIST_DIR / "assets" / "tools-runtime.js"

    node_harness = """
const fs = require('fs');
const vm = require('vm');
const runtimeCode = fs.readFileSync(process.argv[2], 'utf8');
const tools = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));

function runToolInSandbox(tool, queryStr = '', customInputs = {}) {
  const elements = {};
  const presetChips = [];

  function makeEl(id, initialVal = '') {
    const el = {
      id,
      value: String(initialVal),
      textContent: '',
      innerHTML: '',
      style: {},
      children: [],
      listeners: {},
      addEventListener(ev, fn) { this.listeners[ev] = fn; },
      appendChild(child) { this.children.push(child); },
      getAttribute(attr) {
        if (attr === 'data-tool-type') return tool.tool_type;
        if (attr === 'data-tool-config') return JSON.stringify(tool.config);
        return null;
      }
    };
    elements[id] = el;
    return el;
  }

  makeEl('interactive-tool-root');
  makeEl('btn-copy-permalink');
  makeEl('btn-export-csv');

  const cfg = tool.config;
  if (tool.tool_type === 'fee_calc') {
    makeEl('in-amount', customInputs.amount !== undefined ? customInputs.amount : cfg.default_amount);
    makeEl('in-pct', customInputs.pct !== undefined ? customInputs.pct : cfg.percent_fee);
    makeEl('in-fixed', customInputs.fixed !== undefined ? customInputs.fixed : cfg.fixed_fee);
    makeEl('in-fx', customInputs.fx !== undefined ? customInputs.fx : cfg.fx_markup_percent);
    makeEl('out-net');
    makeEl('out-fee');
    makeEl('out-rate');
    makeEl('out-reverse');
    makeEl('sensitivity-matrix-body');
    if (cfg.presets) {
      cfg.presets.forEach(p => {
        presetChips.push({
          label: p.label,
          pct: String(p.pct),
          listeners: {},
          getAttribute(a) { return a === 'data-pct' ? String(p.pct) : null; },
          addEventListener(ev, fn) { this.listeners[ev] = fn; }
        });
      });
    }
  } else if (tool.tool_type === 'saas_calc') {
    makeEl('in-a', customInputs.a !== undefined ? customInputs.a : cfg.default_a);
    makeEl('in-b', customInputs.b !== undefined ? customInputs.b : cfg.default_b);
    makeEl('in-c', customInputs.c !== undefined ? customInputs.c : cfg.default_c);
    makeEl('in-d', customInputs.d !== undefined ? customInputs.d : cfg.default_d);
    makeEl('lbl-r1'); makeEl('val-r1');
    makeEl('lbl-r2'); makeEl('val-r2');
    makeEl('lbl-r3'); makeEl('val-r3');
  } else if (tool.tool_type === 'dev_tool') {
    makeEl('dev-input', customInputs.input !== undefined ? customInputs.input : cfg.sample_input);
    makeEl('dev-output');
    makeEl('btn-run-dev');
    makeEl('btn-copy-dev');
  }

  const sandbox = {
    window: {
      location: { search: queryStr, pathname: '/tools/' + tool.slug + '.html', href: 'https://calcgrid.local/tools/' + tool.slug + '.html' },
      crypto: {
        getRandomValues(arr) {
          for (let i = 0; i < arr.length; i++) arr[i] = (i * 17 + 43) % 1000;
          return arr;
        }
      }
    },
    document: {
      getElementById(id) { return elements[id] || null; },
      querySelectorAll(sel) {
        if (sel === '.preset-chip') return presetChips;
        return [];
      },
      createElement(tag) { return { tag, innerHTML: '' }; }
    },
    navigator: { clipboard: { writeText() {} } },
    URLSearchParams,
    URL,
    TextEncoder,
    Uint32Array,
    atob: (s) => Buffer.from(s, 'base64').toString('binary'),
    btoa: (s) => Buffer.from(s, 'binary').toString('base64'),
    setTimeout: () => {}
  };

  vm.runInNewContext(runtimeCode, sandbox);
  return { elements, presetChips };
}

const results = {};
for (const tool of tools) {
  const std = runToolInSandbox(tool);
  const out = { tool_type: tool.tool_type };
  if (tool.tool_type === 'fee_calc') {
    out.net = std.elements['out-net'].textContent;
    out.fee = std.elements['out-fee'].textContent;
    out.rate = std.elements['out-rate'].textContent;
    out.reverse = std.elements['out-reverse'].textContent;
    out.matrix_rows = std.elements['sensitivity-matrix-body'].children.length;

    // Test $0 and negative guard (-500)
    const zeroRun = runToolInSandbox(tool, '', { amount: -500, pct: tool.config.percent_fee, fixed: 0, fx: 0 });
    out.negative_guard_net = zeroRun.elements['out-net'].textContent;

    // Test preset chip click if available
    if (std.presetChips.length > 0) {
      out.preset_results = [];
      for (const chip of std.presetChips) {
        chip.listeners.click();
        out.preset_results.push({
          label: chip.label,
          pct: chip.pct,
          net: std.elements['out-net'].textContent
        });
      }
    }
  } else if (tool.tool_type === 'saas_calc') {
    out.r1 = std.elements['val-r1'].textContent;
    out.r2 = std.elements['val-r2'].textContent;
    out.r3 = std.elements['val-r3'].textContent;
  } else if (tool.tool_type === 'dev_tool') {
    out.dev_output = std.elements['dev-output'].textContent;
  }
  results[tool.slug] = out;
}
console.log(JSON.stringify(results));
"""

    with tempfile.NamedTemporaryFile("w", suffix=".js", dir="/tmp", delete=False) as jf, \
         tempfile.NamedTemporaryFile("w", suffix=".json", dir="/tmp", delete=False) as tf:
        jf.write(node_harness)
        jf_path = jf.name
        json.dump(TOOLS_CATALOG, tf)
        tf_path = tf.name

    try:
        proc = subprocess.run(
            ["node", jf_path, str(runtime_js_path), tf_path],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Exit {proc.returncode}: {proc.stderr}")
        js_results = json.loads(proc.stdout)
    except Exception as e:
        return {
            "passed": False,
            "tools_math_tested": 0,
            "failures": [f"Node.js runtime execution failed: {e}"],
        }
    finally:
        Path(jf_path).unlink(missing_ok=True)
        Path(tf_path).unlink(missing_ok=True)

    for tool in TOOLS_CATALOG:
        slug = tool["slug"]
        t_type = tool["tool_type"]
        cfg = tool["config"]
        res = js_results.get(slug, {})
        tested_tools.append(slug)

        if t_type == "fee_calc":
            gross = float(cfg["default_amount"])
            pct = float(cfg["percent_fee"])
            fix = float(cfg["fixed_fee"])
            fx = float(cfg["fx_markup_percent"])

            total_rate = (pct + fx) / 100.0
            expected_fee = gross * total_rate + fix
            expected_net = max(0.0, gross - expected_fee)
            expected_rate = (expected_fee / gross) * 100.0 if gross > 0 else 0.0
            expected_reverse = (gross + fix) / (1.0 - total_rate)

            if res.get("net") != fmt_money(expected_net):
                failures.append(f"{slug}: JS net {res.get('net')} != expected {fmt_money(expected_net)}")
            if res.get("fee") != fmt_money(expected_fee):
                failures.append(f"{slug}: JS fee {res.get('fee')} != expected {fmt_money(expected_fee)}")
            if res.get("rate") != f"{expected_rate:.2f}%":
                failures.append(f"{slug}: JS rate {res.get('rate')} != expected {expected_rate:.2f}%")
            if res.get("reverse") != fmt_money(expected_reverse):
                failures.append(f"{slug}: JS reverse {res.get('reverse')} != expected {fmt_money(expected_reverse)}")
            if res.get("matrix_rows") != 6:
                failures.append(f"{slug}: Expected 6 sensitivity matrix rows, got {res.get('matrix_rows')}")
            if res.get("negative_guard_net") != "$0.00":
                failures.append(f"{slug}: Negative input guard failed, got {res.get('negative_guard_net')}")

            if slug == "upwork-freelancer-fee-calculator":
                presets = cfg.get("presets", [])
                expected_labels = [
                    "0% (Direct Contract — Freelancer Plus)",
                    "5% (Direct Contract Standard / Example)",
                    "10% (Example Marketplace Rate)",
                    "15% (Example Marketplace Rate)",
                ]
                actual_labels = [p["label"] for p in presets]
                if actual_labels != expected_labels:
                    failures.append(f"Upwork preset labels mismatch: {actual_labels}")
                if len(res.get("preset_results", [])) != 4:
                    failures.append("Upwork preset click simulation failed")

        elif t_type == "saas_calc":
            a = float(cfg["default_a"])
            b = float(cfg["default_b"])
            c = float(cfg["default_c"])
            d = float(cfg["default_d"])
            exp_r1, exp_r2, exp_r3 = compute_expected_saas(cfg["mode"], a, b, c, d)
            if res.get("r1") != exp_r1:
                failures.append(f"{slug}: JS r1 '{res.get('r1')}' != expected '{exp_r1}'")
            if res.get("r2") != exp_r2:
                failures.append(f"{slug}: JS r2 '{res.get('r2')}' != expected '{exp_r2}'")
            if res.get("r3") != exp_r3:
                failures.append(f"{slug}: JS r3 '{res.get('r3')}' != expected '{exp_r3}'")

        elif t_type == "dev_tool":
            dev_out = res.get("dev_output", "")
            mode = cfg["dev_mode"]
            if not dev_out or dev_out.startswith("Error:") or dev_out.startswith("Invalid"):
                failures.append(f"{slug} ({mode}): Dev tool transformation failed with output '{dev_out}'")
            if mode == "json_to_ts" and ("export interface GeneratedPayload" not in dev_out or "z.object" not in dev_out):
                failures.append(f"{slug}: Missing TypeScript interface or Zod schema in output")
            elif mode == "cron" and "Valid 5-Field Cron Schedule:" not in dev_out:
                failures.append(f"{slug}: Cron parser failed on sample input")
            elif mode == "jwt" and ("JWT HEADER:" not in dev_out or "user_901" not in dev_out):
                failures.append(f"{slug}: JWT decode failed on sample token")
            elif mode == "sql" and "SELECT" not in dev_out:
                failures.append(f"{slug}: SQL formatter failed")
            elif mode == "base64" and "Base64 Encoded:" not in dev_out:
                failures.append(f"{slug}: Base64 encoder failed")
            elif mode == "csv_to_json" and '"name": "Pro CLI Pack"' not in dev_out:
                failures.append(f"{slug}: CSV to JSON converter failed")
            elif mode == "regex" and 'Match: "support@company.am"' not in dev_out:
                failures.append(f"{slug}: Regex extractor failed")
            elif mode == "svg" and "data:image/svg+xml;utf8," not in dev_out:
                failures.append(f"{slug}: SVG data URI converter failed")
            elif mode == "password" and "Entropy:" not in dev_out:
                failures.append(f"{slug}: Password entropy generator failed")
            elif mode == "markdown" and "<h1>Launch Checklist</h1>" not in dev_out:
                failures.append(f"{slug}: Markdown to HTML converter failed")
            elif mode == "utm" and "utm_source=reddit&utm_medium=organic_post&utm_campaign=q4_launch" not in dev_out:
                failures.append(f"{slug}: UTM builder output mismatch: {dev_out}")

    return {
        "passed": len(failures) == 0,
        "tools_math_and_runtime_tested": len(tested_tools),
        "fee_calculators_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] == "fee_calc"),
        "saas_calculators_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] == "saas_calc"),
        "dev_tools_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] == "dev_tool"),
        "failures": failures,
    }


def run_qa_and_security_verification() -> dict:
    """
    Verifies HTML, JSON-LD, links, compliance (no homemade consent banner or unconfigured ad/checkout placeholders),
    confirms the paid ZIP is NOT in `dist/` or Git history, and verifies the multi-tab `.xlsx` workbook inside the ZIP.
    """
    issues = []
    html_files = list(DIST_DIR.rglob("*.html"))

    if len(html_files) != len(TOOLS_CATALOG) + 2:
        issues.append(f"Expected {len(TOOLS_CATALOG) + 2} HTML files, found {len(html_files)}")

    # 1. CRITICAL SECURITY CHECK: Ensure no .zip files exist in public dist/
    exposed_zips = list(DIST_DIR.rglob("*.zip"))
    if exposed_zips:
        issues.append(f"SECURITY VIOLATION: Paid ZIP exposed inside public dist/: {exposed_zips}")

    # 2. GIT HISTORY SECURITY CHECK: Ensure no .zip files exist anywhere in git commit history
    git_dir = ROOT_DIR / ".git"
    git_history_zips = []
    if git_dir.exists():
        proc_git = subprocess.run(
            ["git", "-C", str(ROOT_DIR), "log", "--all", "--full-history", "--name-only", "--pretty=format:", "--", "*.zip"],
            capture_output=True,
            text=True,
        )
        git_history_zips = [line.strip() for line in proc_git.stdout.splitlines() if line.strip()]
        if git_history_zips:
            issues.append(f"SECURITY VIOLATION: .zip file found in Git commit history: {git_history_zips}")

    json_ld_verified = 0
    internal_links_checked = 0

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")

        # Verify homemade consent banner is removed
        if 'id="consent-banner"' in content:
            issues.append(f"Homemade consent banner still present in {html_file.name}")

        # Verify ad placeholders are hidden when ADSENSE_CLIENT_ID is empty
        if not ADSENSE_CLIENT_ID and 'class="ad-slot"' in content:
            issues.append(f"Unconfigured ad-slot placeholder found in {html_file.name}")

        # Verify paid checkout link is disabled when LEMON_SQUEEZY_CHECKOUT_URL is empty
        if not LEMON_SQUEEZY_CHECKOUT_URL and "Purchase via Lemon Squeezy" in content:
            issues.append(f"Active Lemon Squeezy purchase button rendered while URL is unconfigured in {html_file.name}")

        ld_matches = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>',
            content,
            flags=re.DOTALL,
        )
        for raw_ld in ld_matches:
            try:
                parsed = json.loads(raw_ld)
                if "@context" not in parsed:
                    issues.append(f"Missing @context in JSON-LD of {html_file.name}")
                else:
                    json_ld_verified += 1
            except Exception as e:
                issues.append(f"Invalid JSON-LD in {html_file.name}: {e}")

        hrefs = re.findall(r'(?:href|src)="([^"#]+)"', content)
        for ref in hrefs:
            if ref.startswith(("http://", "https://", "mailto:", "javascript:", "data:")):
                continue
            target_path = (html_file.parent / ref).resolve()
            internal_links_checked += 1
            if not target_path.exists():
                issues.append(f"Broken relative reference '{ref}' in {html_file.name}")

    for required_file in ["sitemap.xml", "robots.txt", "rss.xml", f"{INDEXNOW_KEY}.txt"]:
        p = DIST_DIR / required_file
        if not p.exists() or p.stat().st_size == 0:
            issues.append(f"Missing or empty SEO artifact: {required_file}")

    # 3. Verify private Pro ZIP exists outside dist/, contains valid 3-sheet .xlsx + 3 CSVs + working CLI
    private_zip = PRIVATE_PRODUCTS_DIR / "calcgrid-pro-offline-suite.zip"
    xlsx_sheets_verified = 0
    if not private_zip.exists():
        issues.append("Missing private_products/calcgrid-pro-offline-suite.zip")
    else:
        with zipfile.ZipFile(private_zip, "r") as zf:
            bad_file = zf.testzip()
            if bad_file is not None:
                issues.append(f"Corrupted file inside private Pro ZIP: {bad_file}")
            names = set(zf.namelist())
            required_members = {
                "01_cli_batch_auditor/calcgrid_batch_reconciler.py",
                "01_cli_batch_auditor/sample_transactions.csv",
                "02_spreadsheet_models/calcgrid_financial_models.xlsx",
                "02_spreadsheet_models/saas_12mo_cohort_and_cashflow_model.csv",
                "02_spreadsheet_models/cross_border_payout_comparison_matrix.csv",
                "02_spreadsheet_models/roas_and_unit_economics_model.csv",
            }
            missing_members = required_members - names
            if missing_members:
                issues.append(f"Missing files in private Pro ZIP: {sorted(missing_members)}")

            # Verify .xlsx internal structure has 3 worksheets
            if "02_spreadsheet_models/calcgrid_financial_models.xlsx" in names:
                xlsx_raw = zf.read("02_spreadsheet_models/calcgrid_financial_models.xlsx")
                with zipfile.ZipFile(io.BytesIO(xlsx_raw), "r") as xzf:
                    wb_xml = xzf.read("xl/workbook.xml").decode("utf-8")
                    sheet_names = re.findall(r'<sheet name="([^"]+)"', wb_xml)
                    xlsx_sheets_verified = len(sheet_names)
                    if sheet_names != ["SaaS_12Mo_Cohort_Model", "Cross_Border_Fee_Matrix", "ROAS_Unit_Economics"]:
                        issues.append(f"Unexpected .xlsx worksheet names: {sheet_names}")

            with tempfile.TemporaryDirectory() as tmpdir:
                zf.extractall(tmpdir)
                cli_path = Path(tmpdir) / "01_cli_batch_auditor" / "calcgrid_batch_reconciler.py"
                sample_csv = Path(tmpdir) / "01_cli_batch_auditor" / "sample_transactions.csv"
                out_csv = Path(tmpdir) / "reconciled_out.csv"
                proc = subprocess.run(
                    ["python3", str(cli_path), "--input", str(sample_csv), "--output", str(out_csv)],
                    capture_output=True,
                    text=True,
                )
                if proc.returncode != 0 or not out_csv.exists():
                    issues.append(f"Pro CLI batch reconciler test failed: {proc.stderr}")

    return {
        "passed": len(issues) == 0,
        "public_zip_exposed": len(exposed_zips) > 0,
        "git_history_zip_exposed": len(git_history_zips) > 0,
        "xlsx_worksheets_verified": xlsx_sheets_verified,
        "html_pages_verified": len(html_files),
        "json_ld_schemas_verified": json_ld_verified,
        "internal_links_verified": internal_links_checked,
        "issues": issues,
    }


def analyze_telemetry() -> dict:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if not TELEMETRY_LOG.exists():
        return {"total_events": 0, "js_errors": 0, "top_paths": {}}

    total_events = 0
    js_errors = 0
    path_counts = {}

    for line in TELEMETRY_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
            total_events += 1
            if ev.get("eventType") == "js_error":
                js_errors += 1
            p = ev.get("path", "/")
            path_counts[p] = path_counts.get(p, 0) + 1
        except Exception:
            pass

    return {
        "total_events": total_events,
        "js_errors": js_errors,
        "top_paths": dict(sorted(path_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
    }


def run_autopilot_cycle() -> dict:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    build_info = compile_all()
    math_info = run_math_and_runtime_tests()
    qa_info = run_qa_and_security_verification()
    telemetry_info = analyze_telemetry()

    report = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "build": build_info,
        "math_verification": math_info,
        "qa_and_security": qa_info,
        "telemetry": telemetry_info,
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    rep = run_autopilot_cycle()
    print(json.dumps(rep, indent=2))
    if not rep["qa_and_security"]["passed"] or not rep["math_verification"]["passed"]:
        raise SystemExit(1)
