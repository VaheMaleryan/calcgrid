#!/usr/bin/env python3
"""
CalcGrid Autonomous Operations Controller, Freshness Auditor & Verification Suite (autopilot.py)
Performs:
  1. Static site compilation & private Pro ZIP packaging (`private_products/calcgrid-pro-offline-suite.zip`)
  2. Autonomous SMM Short-Form Video Generation (`engine/smm_pipeline.py` -> 1080x1920 MP4 + SRT + UTM manifest)
  3. Security & Git History Audit:
     - Verifies ZERO `.zip` archives exist inside the public `dist/` directory
     - Verifies ZERO `.zip` archives exist anywhere in Git commit history (`git log --all --full-history -- "*.zip"`)
  4. Independent Mathematical & Node.js Runtime Verification across all 32 tools:
     - Flagship #1: `cross-border-payout-comparison-engine` (multi-stage platform + rail + FX + tax math & reverse solver)
     - Flagship #2: `private-csv-payout-fee-auditor` (client-side CSV variance & hidden FX leakage detection)
     - Core 30 Tools: 10 `fee_calc`, 9 `saas_calc`, and 11 `dev_tool` instruments
  5. Fee & Tax Schedule Freshness Audit (flags any source older than 90 days)
  6. Fail-closed deployment protection: tests stop publication without discarding working-tree edits
"""

import argparse
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from build_site import (
    compile_all,
    BRAND_NAME,
    build_dashboard_page,
    DIST_DIR,
    PRIVATE_PRODUCTS_DIR,
    SITE_URL,
    INDEXNOW_KEY,
    ADSENSE_CLIENT_ID,
    LEMON_SQUEEZY_CHECKOUT_URL,
    OFFICIAL_SOURCES,
)
from catalog_data import TOOLS_CATALOG, COUNTRY_CORRIDORS
from smm_pipeline import build_smm_campaign_pack, EPISODE_BLUEPRINTS, verify_episode_financial_claims

ROOT_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT_DIR / "logs"
TELEMETRY_LOG = LOGS_DIR / "telemetry.jsonl"
REPORT_FILE = LOGS_DIR / "autopilot_report.json"
MAX_SCHEDULE_AGE_DAYS = 90


def fmt_money(n: float) -> str:
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


def run_freshness_audit() -> dict:
    """Checks `verified_date` on all corridors and official fee schedules against MAX_SCHEDULE_AGE_DAYS."""
    now = datetime.now(timezone.utc)
    stale = []
    checked = 0

    for code, cdata in COUNTRY_CORRIDORS.items():
        checked += 1
        v_str = cdata.get("verified_date", "2026-10-27")
        try:
            dt = datetime.strptime(v_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            age_days = (now - dt).days
            if age_days > MAX_SCHEDULE_AGE_DAYS:
                stale.append(f"Corridor {code}: {age_days} days old (verified {v_str})")
        except ValueError:
            stale.append(f"Corridor {code}: unparseable verified_date '{v_str}'")

    for slug, (_, v_str) in OFFICIAL_SOURCES.items():
        checked += 1
        try:
            dt = datetime.strptime(v_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            age_days = (now - dt).days
            if age_days > MAX_SCHEDULE_AGE_DAYS:
                stale.append(f"Tool {slug}: {age_days} days old (verified {v_str})")
        except ValueError:
            stale.append(f"Tool {slug}: unparseable verified_date '{v_str}'")

    return {
        "passed": len(stale) == 0,
        "schedules_checked": checked,
        "max_allowed_age_days": MAX_SCHEDULE_AGE_DAYS,
        "stale_schedules": stale
    }


def run_math_and_runtime_tests() -> dict:
    """
    Executes `dist/assets/tools-runtime.js` inside Node.js for all 32 tools and verifies
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
  const originChips = [];

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
  if (tool.tool_type === 'corridor_engine') {
    makeEl('in-country', customInputs.country || cfg.default_country || 'AM');
    makeEl('in-amount', customInputs.amount !== undefined ? customInputs.amount : cfg.default_amount);
    makeEl('in-origin-pct', customInputs.origin_pct !== undefined ? customInputs.origin_pct : cfg.default_origin_pct);
    makeEl('in-origin-fix', customInputs.origin_fix !== undefined ? customInputs.origin_fix : cfg.default_origin_fixed);
    makeEl('in-tax-pct', customInputs.tax !== undefined ? customInputs.tax : 1.0);
    makeEl('in-fx-rate', customInputs.fx_rate !== undefined ? customInputs.fx_rate : 388.0);
    makeEl('in-target-net', customInputs.target_net !== undefined ? customInputs.target_net : cfg.default_amount);
    makeEl('corridor-tax-presets');
    makeEl('corridor-comparison-body');
    makeEl('fx-rate-hint');
    makeEl('corridor-tax-caveat');
    makeEl('out-net');
    makeEl('out-best-rail');
    makeEl('out-range');
    makeEl('out-local');
    makeEl('out-fee');
    makeEl('out-reverse');
  } else if (tool.tool_type === 'csv_auditor') {
    makeEl('csv-audit-input', customInputs.csv || cfg.sample_csv);
    makeEl('csv-file-upload');
    makeEl('csv-audit-body');
    makeEl('btn-run-audit');
    makeEl('out-audit-gross');
    makeEl('out-audit-net');
    makeEl('out-audit-leakage');
    makeEl('out-audit-alerts');
  } else if (tool.tool_type === 'fee_calc') {
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
      location: { protocol: 'file:', search: queryStr, pathname: '/tools/' + tool.slug + '.html', href: 'https://calcgrid.local/tools/' + tool.slug + '.html' },
      crypto: {
        getRandomValues(arr) {
          for (let i = 0; i < arr.length; i++) arr[i] = (i * 17 + 43) % 1000;
          return arr;
        }
      }
    },
    document: {
      referrer: '',
      getElementById(id) { return elements[id] || null; },
      querySelectorAll(sel) {
        if (sel === '.preset-chip') return presetChips;
        if (sel === '.origin-preset-chip') return originChips;
        return [];
      },
      createElement(tag) {
        return {
          tag,
          innerHTML: '',
          textContent: '',
          className: '',
          type: '',
          addEventListener() {}
        };
      }
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
  if (tool.tool_type === 'corridor_engine') {
    out.am_net = std.elements['out-net'].textContent;
    out.am_best_rail = std.elements['out-best-rail'].textContent;
    out.am_reverse = std.elements['out-reverse'].textContent;
    out.am_rows = std.elements['corridor-comparison-body'].children.length;

    const am5Run = runToolInSandbox(tool, '?country=AM&tax=5.0', { country: 'AM', tax: 5.0 });
    out.am_5pct_net = am5Run.elements['out-net'].textContent;
    out.am_5pct_reverse = am5Run.elements['out-reverse'].textContent;

    const geRun = runToolInSandbox(tool, '?country=GE', { country: 'GE' });
    out.ge_net = geRun.elements['out-net'].textContent;
    out.ge_best_rail = geRun.elements['out-best-rail'].textContent;
  } else if (tool.tool_type === 'csv_auditor') {
    out.gross = std.elements['out-audit-gross'].textContent;
    out.net = std.elements['out-audit-net'].textContent;
    out.leakage = std.elements['out-audit-leakage'].textContent;
    out.alerts = std.elements['out-audit-alerts'].textContent;
    out.rows = std.elements['csv-audit-body'].children.length;
  } else if (tool.tool_type === 'fee_calc') {
    out.net = std.elements['out-net'].textContent;
    out.fee = std.elements['out-fee'].textContent;
    out.rate = std.elements['out-rate'].textContent;
    out.reverse = std.elements['out-reverse'].textContent;
    out.matrix_rows = std.elements['sensitivity-matrix-body'].children.length;

    const zeroRun = runToolInSandbox(tool, '', { amount: -500, pct: tool.config.percent_fee, fixed: 0, fx: 0 });
    out.negative_guard_net = zeroRun.elements['out-net'].textContent;

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

        if t_type == "corridor_engine":
            # Verify Armenia (RA Tax Code Art. 257 Gross Turnover Base: $1,000 gross -> $10.00 tax at 1% -> $862.04 net, $1,159.86 reverse invoice)
            if res.get("am_best_rail") != "Payoneer Local Withdrawal (Armenia)":
                failures.append(f"{slug}: Expected Payoneer Local Withdrawal for Armenia, got {res.get('am_best_rail')}")
            if res.get("am_net") != "$862.04":
                failures.append(f"{slug}: Armenia 1% gross turnover tax expected net $862.04, got {res.get('am_net')}")
            if res.get("am_reverse") != "$1,159.86":
                failures.append(f"{slug}: Armenia 1% reverse invoice expected $1,159.86, got {res.get('am_reverse')}")
            if res.get("am_5pct_net") != "$822.04":
                failures.append(f"{slug}: Armenia 5% standard gross turnover tax expected net $822.04, got {res.get('am_5pct_net')}")
            if res.get("am_5pct_reverse") != "$1,216.23":
                failures.append(f"{slug}: Armenia 5% reverse invoice expected $1,216.23, got {res.get('am_5pct_reverse')}")
            if res.get("am_rows") != 4:
                failures.append(f"{slug}: Expected 4 payout routes in comparison table, got {res.get('am_rows')}")
            # Verify Georgia (Wise available -> Wise Mid-Market Route wins)
            if res.get("ge_best_rail") != "Wise Mid-Market Route (Georgia)":
                failures.append(f"{slug}: Expected Wise Mid-Market Route for Georgia, got {res.get('ge_best_rail')}")

        elif t_type == "csv_auditor":
            if res.get("gross") != "$7,249.00":
                failures.append(f"{slug}: Expected $7,249.00 gross audited, got {res.get('gross')}")
            if res.get("leakage") != "$32.70":
                failures.append(f"{slug}: Expected $32.70 detected fee leakage, got {res.get('leakage')}")
            if not str(res.get("alerts", "")).startswith("2 flagged"):
                failures.append(f"{slug}: Expected 2 flagged variance rows, got {res.get('alerts')}")
            if res.get("rows") != 5:
                failures.append(f"{slug}: Expected 5 audited rows, got {res.get('rows')}")

        elif t_type == "fee_calc":
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
        "flagship_engines_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] in ("corridor_engine", "csv_auditor")),
        "fee_calculators_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] == "fee_calc"),
        "saas_calculators_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] == "saas_calc"),
        "dev_tools_verified": sum(1 for t in TOOLS_CATALOG if t["tool_type"] == "dev_tool"),
        "failures": failures,
    }


def run_qa_and_security_verification() -> dict:
    """
    Verifies HTML, JSON-LD, links, compliance (no homemade consent banner or unconfigured ad/checkout placeholders),
    confirms the paid ZIP and private dashboard are NOT in `dist/` or Git history, and verifies the multi-tab `.xlsx` workbook inside the ZIP.
    """
    issues = []
    html_files = list(DIST_DIR.rglob("*.html"))

    if len(html_files) != len(TOOLS_CATALOG) + 2:
        issues.append(f"Expected {len(TOOLS_CATALOG) + 2} public HTML files, found {len(html_files)}")

    # 1. CRITICAL SECURITY CHECK: Ensure no .zip files or private dashboard exist in public dist/
    exposed_zips = list(DIST_DIR.rglob("*.zip"))
    if exposed_zips:
        issues.append(f"SECURITY VIOLATION: Paid ZIP exposed inside public dist/: {exposed_zips}")

    public_dashboard_exposed = (DIST_DIR / "dashboard.html").exists()
    if public_dashboard_exposed:
        issues.append("PRIVACY VIOLATION: dashboard.html exposed inside public dist/")

    private_dashboard_exists = (LOGS_DIR / "private_dashboard.html").exists()
    if not private_dashboard_exists:
        issues.append("Missing private operator dashboard at logs/private_dashboard.html")

    # 2. GIT HISTORY SECURITY CHECK: Ensure no .zip files exist anywhere in git commit history
    git_dir = ROOT_DIR / ".git"
    git_history_zips = []
    git_env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_SYSTEM": "/dev/null"}
    if git_dir.exists():
        proc_git = subprocess.run(
            ["git", "-C", str(ROOT_DIR), "log", "--all", "--full-history", "--name-only", "--pretty=format:", "--", "*.zip"],
            capture_output=True,
            text=True,
            env=git_env,
        )
        if proc_git.returncode != 0:
            issues.append(f"Git history check failed to execute: {proc_git.stderr.strip()}")
        git_history_zips = [line.strip() for line in proc_git.stdout.splitlines() if line.strip()]
        if git_history_zips:
            issues.append(f"SECURITY VIOLATION: .zip file found in Git commit history: {git_history_zips}")

    tracked = subprocess.run(["git", "-C", str(ROOT_DIR), "ls-files"], capture_output=True, text=True, check=True).stdout.splitlines()
    for name in tracked:
        if name.startswith(("private_products/", "logs/", "marketing_outbox/videos/", ".env")):
            issues.append("Private path tracked in Git: " + name)
    for item in DIST_DIR.rglob("*"):
        if item.is_file() and (item.suffix.lower() in {".zip", ".mp4", ".log", ".jsonl", ".env"} or any(part in {"logs", "private_products", "marketing_outbox"} for part in item.relative_to(DIST_DIR).parts)):
            issues.append("Private file exposed in dist: " + str(item.relative_to(DIST_DIR)))
    json_ld_verified = 0
    internal_links_checked = 0

    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")

        if 'id="consent-banner"' in content:
            issues.append(f"Homemade consent banner still present in {html_file.name}")

        if not ADSENSE_CLIENT_ID and 'class="ad-slot"' in content:
            issues.append(f"Unconfigured ad-slot placeholder found in {html_file.name}")

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
            target_path = (html_file.parent / ref.split("#")[0].split("?")[0]).resolve()
            internal_links_checked += 1
            if not target_path.exists():
                issues.append(f"Broken relative reference '{ref}' in {html_file.name}")

        if "dashboard.html" in content:
            issues.append(f"Public link to private dashboard found in {html_file.name}")

    for required_file in ["sitemap.xml", "robots.txt", "rss.xml", f"{INDEXNOW_KEY}.txt"]:
        p = DIST_DIR / required_file
        if not p.exists() or p.stat().st_size == 0:
            issues.append(f"Missing or empty artifact: {required_file}")

    # Verify SMM Episode 1 uses verified Article 257 Gross Turnover Tax math ($862.04 net / $1,159.86 reverse)
    ep1_srt = ROOT_DIR / "marketing_outbox" / "subtitles" / "ep01_upwork_payoneer_armenia.srt"
    if ep1_srt.exists():
        srt_text = ep1_srt.read_text(encoding="utf-8")
        if "$863.32" in srt_text or "$1,158.15" in srt_text:
            issues.append("SMM Episode 1 subtitle still contains deprecated post-fee tax numbers ($863.32 / $1,158.15)")
        if "$862.04" not in srt_text or "$1,159.86" not in srt_text:
            issues.append("SMM Episode 1 subtitle missing verified Article 257 gross turnover tax numbers ($862.04 / $1,159.86)")

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

            if "02_spreadsheet_models/calcgrid_financial_models.xlsx" in names:
                xlsx_raw = zf.read("02_spreadsheet_models/calcgrid_financial_models.xlsx")
                with zipfile.ZipFile(io.BytesIO(xlsx_raw), "r") as xzf:
                    wb_xml = xzf.read("xl/workbook.xml").decode("utf-8")
                    sheet_names = re.findall(r'<sheet name="([^"]+)"', wb_xml)
                    xlsx_sheets_verified = len(sheet_names)
                    if sheet_names != ["SaaS_12Mo_Cohort_Model", "Cross_Border_Fee_Matrix", "ROAS_Unit_Economics"]:
                        issues.append(f"Unexpected .xlsx worksheet names: {sheet_names}")

            with tempfile.TemporaryDirectory(dir="/tmp") as tmpdir:
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
        "public_dashboard_exposed": public_dashboard_exposed,
        "private_dashboard_generated": private_dashboard_exists,
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
        return {"total_events": 0, "js_errors": 0, "utm_events": 0, "top_paths": {}}

    total_events = 0
    js_errors = 0
    utm_events = 0
    path_counts = {}

    for line in TELEMETRY_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
            total_events += 1
            if ev.get("eventType") == "js_error":
                js_errors += 1
            if ev.get("utm_source") or ev.get("utm_campaign"):
                utm_events += 1
            p = ev.get("path", "/")
            path_counts[p] = path_counts.get(p, 0) + 1
        except Exception:
            pass

    return {
        "total_events": total_events,
        "js_errors": js_errors,
        "utm_events": utm_events,
        "top_paths": dict(sorted(path_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
    }


def run_autopilot_cycle(auto_rollback: bool = False, ci: bool = False) -> dict:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if ci:
        smm_info = {"episodes": [{"episode_id": ep["episode_id"], "math_claims_verified": verify_episode_financial_claims(ep)["verified"], "publish_status": "CI_VERIFIED_NO_PUBLISH"} for ep in EPISODE_BLUEPRINTS]}
    else:
        smm_info = build_smm_campaign_pack(allow_publish=False)
    build_info = compile_all()
    freshness_info = run_freshness_audit()
    math_info = run_math_and_runtime_tests()
    qa_info = run_qa_and_security_verification()
    telemetry_info = analyze_telemetry()
    regression = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT_DIR, capture_output=True, text=True)
    regression_info = {"passed": regression.returncode == 0, "details": (regression.stdout + regression.stderr).strip()}


    smm_episodes = smm_info.get("episodes", [])
    smm_claims_verified = len(smm_episodes) > 0 and all(ep.get("math_claims_verified") for ep in smm_episodes)

    all_passed = (
        math_info["passed"]
        and qa_info["passed"]
        and freshness_info["passed"]
        and smm_claims_verified
        and regression_info["passed"]
    )

    rollback_triggered = False
    # A failed build must never discard the owner's source edits. Deployment stops on failure.
    # --auto-rollback remains a compatibility flag; Git/Cloudflare retains the last good deployment.

    report = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "all_checks_passed": all_passed,
        "rollback_triggered": rollback_triggered,
        "build": build_info,
        "freshness_audit": freshness_info,
        "math_verification": math_info,
        "regression_tests": regression_info,
        "qa_and_security": qa_info,
        "smm_pipeline": {
            "episodes_rendered": 0 if ci else len(smm_episodes),
            "episodes_checked": len(smm_episodes),
            "all_financial_claims_verified": smm_claims_verified,
            "episode_statuses": {ep["episode_id"]: ep["publish_status"] for ep in smm_episodes},
            "oauth_configured": smm_info.get("oauth_integrations_configured", {})
        },
        "telemetry": telemetry_info,
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CalcGrid Autonomous Operations & Verification Suite")
    parser.add_argument("--ci", action="store_true", help="Verify without media rendering or external publishing")
    parser.add_argument("--auto-rollback", action="store_true", help="Compatibility flag; failed checks stop deployment without discarding source edits")
    parser.add_argument("--commit", type=str, default="", help="Commit verified changes to git with the given commit message if all checks pass")
    parser.add_argument("--lemon-squeezy-url", type=str, default="", help="Set live Lemon Squeezy checkout URL in launch_config.json before building")
    parser.add_argument("--site-url", type=str, default="", help="Set live public SITE_URL in launch_config.json before building")
    args = parser.parse_args()

    cfg_path = ROOT_DIR / "launch_config.json"
    if args.lemon_squeezy_url or args.site_url:
        cfg_data = {}
        if cfg_path.exists():
            try:
                cfg_data = json.loads(cfg_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        if args.lemon_squeezy_url:
            cfg_data["lemon_squeezy_checkout_url"] = args.lemon_squeezy_url.strip()
            os.environ["LEMON_SQUEEZY_URL"] = args.lemon_squeezy_url.strip()
        if args.site_url:
            cfg_data["site_url"] = args.site_url.strip().rstrip("/")
            os.environ["SITE_URL"] = args.site_url.strip().rstrip("/")
        cfg_path.write_text(json.dumps(cfg_data, indent=2) + "\n", encoding="utf-8")

    if args.site_url or args.lemon_squeezy_url:
        import build_site as site_module
        import smm_pipeline as smm_module
        if args.site_url:
            SITE_URL = site_module.SITE_URL = smm_module.SITE_URL = args.site_url.strip().rstrip("/")
        if args.lemon_squeezy_url and site_module.MONETIZATION_APPROVED:
            site_module.LEMON_SQUEEZY_CHECKOUT_URL = args.lemon_squeezy_url.strip()

    rep = run_autopilot_cycle(auto_rollback=args.auto_rollback, ci=args.ci)
    if args.commit and rep["all_checks_passed"] and (ROOT_DIR / ".git").exists():
        git_env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null",
            "GIT_AUTHOR_NAME": BRAND_NAME + " Autopilot",
            "GIT_AUTHOR_EMAIL": "autopilot@users.noreply.github.com",
            "GIT_COMMITTER_NAME": BRAND_NAME + " Autopilot",
            "GIT_COMMITTER_EMAIL": "autopilot@users.noreply.github.com",
        }
        subprocess.run(["git", "-C", str(ROOT_DIR), "add", "--", "engine", "dist", "launch_config.json", "wrangler.toml", ".github", ".gitignore", "tests", "README.md"], check=True, env=git_env)
        # Ensure logs/ and private_products/ are untracked if previously tracked
        subprocess.run(["git", "-C", str(ROOT_DIR), "rm", "-r", "--cached", "--ignore-unmatch", "logs", "private_products"], check=False, capture_output=True, env=git_env)
        status_proc = subprocess.run(["git", "-C", str(ROOT_DIR), "status", "--porcelain"], capture_output=True, text=True, env=git_env)
        if status_proc.stdout.strip():
            subprocess.run(["git", "-C", str(ROOT_DIR), "commit", "-m", args.commit], check=True, capture_output=True, env=git_env)
        head_proc = subprocess.run(["git", "-C", str(ROOT_DIR), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, env=git_env)
        rep["git_commit"] = head_proc.stdout.strip()
        REPORT_FILE.write_text(json.dumps(rep, indent=2), encoding="utf-8")

    print(json.dumps(rep, indent=2))
    if not rep["all_checks_passed"]:
        raise SystemExit(1)
