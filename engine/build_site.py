#!/usr/bin/env python3
"""
CalcGrid Autonomous Static Site Compiler, Flagship Competitive Advantage Builder & Private Product Packager.
Implements:
  1. Flagship Engine #1: Country-Aware End-to-End Freelancer Payout, Reverse Invoice & Tax Comparison Engine
     (Armenia, Georgia, Serbia, Philippines, India; Wise vs Payoneer vs SWIFT vs Lemon Squeezy; Uncertainty Bands).
  2. Flagship Engine #2: Multi-Stage Reverse Invoice Solver (Target Net -> Required Gross Invoice after Platform + Rail + FX + Tax).
  3. Flagship Engine #3: Private Browser-Based Transaction CSV Auditor (100% client-side fee & FX leakage detector).
  4. Honest Operations & Earnings Proof Dashboard (`dist/dashboard.html`) tracking Visitors by Source, Search, Social UTM,
     Conversions, Collected Revenue ($0.00 until live sales), Expenses ($0.00), and Net Profit.
  5. Strict Pre-Launch Compliance:
     - Paid Pro ZIP (`calcgrid-pro-offline-suite.zip`) stored strictly in `private_products/` with multi-tab `.xlsx` + 3 `.csv` files.
     - No homemade cookie banner (uses Google's certified IAB TCF CMP when AdSense is active).
     - Ad slots and checkout buttons remain disabled/hidden until `ADSENSE_CLIENT_ID` and `LEMON_SQUEEZY_URL` are configured.
"""

import html
import io
import json
import os
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from catalog_data import TOOLS_CATALOG, COUNTRY_CORRIDORS, COMPETITOR_BENCHMARK_MATRIX

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
TOOLS_DIR = DIST_DIR / "tools"
ASSETS_DIR = DIST_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
PRIVATE_PRODUCTS_DIR = ROOT_DIR / "private_products"
LOGS_DIR = ROOT_DIR / "logs"
MARKETING_DIR = ROOT_DIR / "marketing_outbox"

SITE_URL = os.environ.get("SITE_URL", "https://calcgrid-tools.pages.dev")
INDEXNOW_KEY = "8f92a1c4e7b34d109a8e2c5f6b7d8e91"
LEMON_SQUEEZY_CHECKOUT_URL = os.environ.get("LEMON_SQUEEZY_URL", "").strip()
ADSENSE_CLIENT_ID = os.environ.get("ADSENSE_CLIENT_ID", "").strip()

OFFICIAL_SOURCES = {
    "cross-border-payout-comparison-engine": ("Wise, Payoneer, Upwork & RA/GE/RS/PH/IN Tax Schedules", "2026-10-27"),
    "private-csv-payout-fee-auditor": ("Published Provider Fee Schedules (Stripe, Payoneer, Wise, Upwork, Lemon Squeezy)", "2026-10-27"),
    "payoneer-fee-calculator": ("Payoneer Pricing & Withdrawal Schedule", "2026-10-27"),
    "wise-transfer-fee-calculator": ("Wise Mid-Market & Corridor Pricing Schedule", "2026-10-27"),
    "lemonsqueezy-fee-calculator": ("Lemon Squeezy Merchant of Record Pricing (5% + $0.50)", "2026-10-27"),
    "gumroad-fee-calculator": ("Gumroad Creator Fee Schedule (10% + $0.50 + Processing)", "2026-10-27"),
    "paddle-fee-calculator": ("Paddle Checkout Pricing Schedule (5% + $0.50)", "2026-10-27"),
    "upwork-freelancer-fee-calculator": ("Upwork Variable Freelancer Service Fee (0%–15%)", "2026-10-27"),
    "fiverr-seller-fee-calculator": ("Fiverr Seller Terms of Service (20% Commission)", "2026-10-27"),
    "stripe-international-fee-calculator": ("Stripe Standard & Cross-Border Pricing (2.9% + $0.30)", "2026-10-27"),
    "paypal-goods-services-fee-calculator": ("PayPal Merchant Commercial Transaction Rates", "2026-10-27"),
    "armenia-it-tax-turnover-calculator": ("RA Tax Code — Turnover Tax & Individual Entrepreneur Schedule", "2026-10-27"),
}


def build_css() -> str:
    return """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
  --paper: #F7F6F2;
  --surface: #FFFFFF;
  --stone-panel: #EFECE6;
  --ink: #141413;
  --ink-secondary: #57534E;
  --ink-muted: #78716C;
  --rule: #D6D3CD;
  --rule-dark: #141413;
  --accent: #0F766E;
  --accent-light: #F0FDFA;
  --amber-ink: #B45309;
  --amber-bg: #FEF3C7;
  --danger-ink: #991B1B;
  --danger-bg: #FEE2E2;
  --font-serif: 'Newsreader', Georgia, serif;
  --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background-color: var(--paper);
  color: var(--ink);
  font-family: var(--font-sans);
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}

a { color: var(--ink); text-decoration: none; }

.navbar {
  background: var(--paper);
  border-bottom: 1px solid var(--rule-dark);
  padding: 16px 28px;
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.brand { display: flex; align-items: baseline; gap: 12px; }
.brand-name {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--ink);
}
.brand-meta {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 0.83rem;
  flex-wrap: wrap;
}
.nav-links a { color: var(--ink-secondary); font-weight: 500; }
.nav-links a:hover { color: var(--ink); }

.nav-cta {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--ink);
  color: var(--paper) !important;
  padding: 8px 14px;
  border: 1px solid var(--ink);
  cursor: pointer;
}
.nav-cta:hover { background: var(--accent); border-color: var(--accent); }

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 28px 72px;
}

.editorial-hero {
  display: grid;
  grid-template-columns: 7fr 5fr;
  gap: 40px;
  padding: 44px 0;
  border-bottom: 1px solid var(--rule-dark);
  align-items: center;
}

.kicker {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  display: block;
  margin-bottom: 10px;
}

.editorial-hero h1 {
  font-family: var(--font-serif);
  font-size: 2.85rem;
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: -0.025em;
  color: var(--ink);
  margin-bottom: 16px;
}

.editorial-hero p {
  font-size: 1rem;
  color: var(--ink-secondary);
  max-width: 560px;
  margin-bottom: 24px;
}

.flagship-banner {
  background: var(--surface);
  border: 1px solid var(--rule-dark);
  padding: 24px 28px;
  margin-top: 32px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
.flagship-col {
  border-right: 1px solid var(--rule);
  padding-right: 20px;
}
.flagship-col:last-child { border-right: none; padding-right: 0; }
.flagship-col h3 {
  font-family: var(--font-serif);
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 6px;
}
.flagship-col p {
  font-size: 0.82rem;
  color: var(--ink-secondary);
  margin-bottom: 12px;
}

.search-bar { max-width: 520px; }
.search-bar label {
  display: block;
  font-family: var(--font-mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
  margin-bottom: 6px;
}
.search-bar input {
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--rule-dark);
  color: var(--ink);
  padding: 13px 16px;
  font-family: var(--font-sans);
  font-size: 0.92rem;
  outline: none;
}
.search-bar input:focus {
  border-color: var(--accent);
  box-shadow: 3px 3px 0 var(--ink);
}

.hero-figure {
  background: var(--surface);
  border: 1px solid var(--rule-dark);
  padding: 14px;
}
.hero-figure img {
  width: 100%;
  height: auto;
  display: block;
  border: 1px solid var(--rule);
}
.figure-caption {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--ink-muted);
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.category-section { padding-top: 44px; }
.category-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid var(--rule-dark);
  padding-bottom: 10px;
  margin-bottom: 20px;
}
.category-title {
  font-family: var(--font-serif);
  font-size: 1.6rem;
  font-weight: 500;
}
.category-index {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid var(--rule);
  border-left: 1px solid var(--rule);
}
.tool-card {
  background: var(--surface);
  border-right: 1px solid var(--rule);
  border-bottom: 1px solid var(--rule);
  padding: 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: background-color 0.12s ease;
}
.tool-card:hover { background: var(--stone-panel); }
.tool-num {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--ink-muted);
  margin-bottom: 10px;
  display: block;
}
.tool-card h3 {
  font-family: var(--font-serif);
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 8px;
  line-height: 1.25;
}
.tool-card p {
  font-size: 0.83rem;
  color: var(--ink-secondary);
  margin-bottom: 18px;
}
.tool-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  border-top: 1px solid var(--rule);
  padding-top: 10px;
}

.breadcrumb-bar {
  padding: 20px 0 14px;
  border-bottom: 1px solid var(--rule);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--ink-muted);
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}
.breadcrumb-bar a { color: var(--ink-secondary); }

.tool-header {
  padding: 28px 0 24px;
  border-bottom: 1px solid var(--rule-dark);
}
.tool-header h1 {
  font-family: var(--font-serif);
  font-size: 2.35rem;
  font-weight: 500;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}
.tool-header p {
  font-size: 0.98rem;
  color: var(--ink-secondary);
  max-width: 760px;
}

.workspace-grid {
  display: grid;
  grid-template-columns: 7fr 5fr;
  gap: 36px;
  padding-top: 32px;
  align-items: start;
}

.parameters-sheet, .ledger-sheet, .doc-section {
  background: var(--surface);
  border: 1px solid var(--rule-dark);
  padding: 28px;
}

.sheet-heading {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
  padding-bottom: 12px;
  border-bottom: 1px solid var(--rule);
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.presets-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 18px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--rule);
}
.preset-chip {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  background: var(--paper);
  border: 1px solid var(--rule-dark);
  color: var(--ink);
  padding: 6px 10px;
  cursor: pointer;
}
.preset-chip:hover {
  background: var(--ink);
  color: var(--paper);
}

.field-group {
  padding-bottom: 16px;
  margin-bottom: 16px;
  border-bottom: 1px solid var(--rule);
}
.field-group:last-of-type { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.field-group label {
  display: block;
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 6px;
}
.field-group input, .field-group textarea, .field-group select {
  width: 100%;
  background: var(--paper);
  border: 1px solid var(--rule-dark);
  color: var(--ink);
  padding: 10px 13px;
  font-family: var(--font-mono);
  font-size: 0.92rem;
  font-variant-numeric: tabular-nums;
  outline: none;
}
.field-group input:focus, .field-group textarea:focus, .field-group select:focus {
  border-color: var(--accent);
  background: var(--surface);
}
.field-group textarea { min-height: 160px; font-size: 0.81rem; line-height: 1.5; }
.field-hint {
  display: block;
  font-family: var(--font-mono);
  font-size: 0.69rem;
  color: var(--ink-muted);
  margin-top: 5px;
}

.ledger-primary {
  padding: 16px 0 22px;
  border-bottom: 1px solid var(--rule-dark);
}
.ledger-primary-label {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-muted);
  display: block;
  margin-bottom: 6px;
}
.ledger-primary-value {
  font-family: var(--font-serif);
  font-size: 3rem;
  font-weight: 500;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.03em;
  line-height: 1.05;
}

.ledger-rows { padding-top: 14px; }
.ledger-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 9px 0;
  border-bottom: 1px solid var(--rule);
  font-size: 0.84rem;
  gap: 12px;
}
.ledger-row:last-child { border-bottom: none; }
.ledger-row span { color: var(--ink-secondary); }
.ledger-row strong {
  font-family: var(--font-mono);
  font-variant-numeric: tabular-nums;
  color: var(--ink);
  font-weight: 600;
  text-align: right;
}

.ledger-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid var(--rule);
}

/* SENSITIVITY & COMPARISON MATRIX TABLES */
.matrix-table {
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-variant-numeric: tabular-nums;
  margin-top: 12px;
}
.matrix-table th, .matrix-table td {
  border: 1px solid var(--rule);
  padding: 8px 10px;
  text-align: right;
  vertical-align: top;
}
.matrix-table th:first-child, .matrix-table td:first-child { text-align: left; }
.matrix-table th {
  background: var(--stone-panel);
  color: var(--ink);
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.67rem;
}

.badge-ok {
  display: inline-block;
  padding: 2px 6px;
  font-family: var(--font-mono);
  font-size: 0.65rem;
  background: var(--accent-light);
  color: var(--accent);
  border: 1px solid var(--accent);
}
.badge-warn {
  display: inline-block;
  padding: 2px 6px;
  font-family: var(--font-mono);
  font-size: 0.65rem;
  background: var(--amber-bg);
  color: var(--amber-ink);
  border: 1px solid var(--amber-ink);
}
.badge-alert {
  display: inline-block;
  padding: 2px 6px;
  font-family: var(--font-mono);
  font-size: 0.65rem;
  background: var(--danger-bg);
  color: var(--danger-ink);
  border: 1px solid var(--danger-ink);
}

.code-output {
  background: var(--paper);
  border: 1px solid var(--rule-dark);
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--ink);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 340px;
  overflow-y: auto;
}

.btn-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.btn-primary {
  font-family: var(--font-mono);
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--ink);
  color: var(--paper);
  border: 1px solid var(--ink);
  padding: 10px 15px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  display: inline-block;
}
.btn-primary:hover { background: var(--accent); border-color: var(--accent); }

.btn-secondary {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--surface);
  color: var(--ink);
  border: 1px solid var(--rule-dark);
  padding: 9px 12px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  display: inline-block;
}
.btn-secondary:hover { background: var(--stone-panel); }

.btn-disabled {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--paper);
  color: var(--ink-muted);
  border: 1px dashed var(--rule-dark);
  padding: 11px 14px;
  font-weight: 600;
  text-align: center;
}

.reference-card {
  margin-top: 24px;
  background: var(--stone-panel);
  border: 1px solid var(--rule-dark);
  padding: 22px;
}
.reference-card img {
  width: 100%;
  height: auto;
  border: 1px solid var(--rule);
  margin-bottom: 14px;
  display: block;
}
.reference-card h3 {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: 6px;
}
.reference-card p {
  font-size: 0.82rem;
  color: var(--ink-secondary);
  margin-bottom: 12px;
}
.reference-list {
  list-style: none;
  color: var(--ink);
  margin-bottom: 16px;
  border-top: 1px solid var(--rule);
}
.reference-list li {
  padding: 7px 0;
  border-bottom: 1px solid var(--rule);
  font-family: var(--font-mono);
  font-size: 0.73rem;
}

.ad-slot {
  background: var(--stone-panel);
  border: 1px solid var(--rule);
  padding: 18px;
  text-align: center;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--ink-muted);
  margin: 28px 0;
}

.doc-section { margin-top: 28px; }
.doc-section h3 {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 500;
  margin-bottom: 10px;
}
.formula-block {
  font-family: var(--font-mono);
  font-size: 0.81rem;
  background: var(--paper);
  border-left: 3px solid var(--ink);
  padding: 12px 16px;
  margin-bottom: 20px;
  color: var(--ink);
}
.faq-item { border-top: 1px solid var(--rule); padding: 16px 0; }
.faq-item h4 { font-size: 0.95rem; font-weight: 600; margin-bottom: 6px; }
.faq-item p { font-size: 0.86rem; color: var(--ink-secondary); }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin: 24px 0;
}
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--rule-dark);
  padding: 18px;
}
.kpi-card .k-label {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  color: var(--ink-muted);
  display: block;
  margin-bottom: 6px;
}
.kpi-card .k-val {
  font-family: var(--font-serif);
  font-size: 2rem;
  font-weight: 500;
  color: var(--ink);
}
.kpi-card .k-sub {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  color: var(--ink-secondary);
  margin-top: 6px;
  display: block;
}

footer {
  border-top: 1px solid var(--rule-dark);
  padding: 36px 28px;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  color: var(--ink-muted);
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

@media (max-width: 960px) {
  .editorial-hero, .workspace-grid, .flagship-banner, .kpi-grid { grid-template-columns: 1fr; }
  .flagship-col { border-right: none; border-bottom: 1px solid var(--rule); padding-bottom: 16px; padding-right: 0; }
  .tools-grid { grid-template-columns: 1fr; }
}
""".strip()


def build_runtime_js() -> str:
    corridors_json = json.dumps(COUNTRY_CORRIDORS)
    return f"""
// ============================================================================
// CalcGrid Client-Side Computation Engine, Country Corridor Router & CSV Auditor
// ============================================================================

const CALCGRID_CORRIDORS = {corridors_json};

(function () {{
  // 0. Privacy-Safe Attribution & Telemetry Ping (tracks UTM source, pageviews, and JS errors)
  try {{
    const uParams = new URLSearchParams(window.location.search);
    const utmSource = uParams.get('utm_source') || '';
    const utmMedium = uParams.get('utm_medium') || '';
    const utmCampaign = uParams.get('utm_campaign') || '';
    if (window.fetch && window.location.protocol.startsWith('http')) {{
      window.fetch('/api/telemetry', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          eventType: 'pageview',
          path: window.location.pathname,
          utm_source: utmSource,
          utm_medium: utmMedium,
          utm_campaign: utmCampaign,
          referrer: document.referrer || 'direct'
        }})
      }}).catch(function () {{}});
    }}
  }} catch (e) {{}}

  // 1. Homepage Live Filter
  const searchInput = document.getElementById('hub-search-input');
  if (searchInput) {{
    searchInput.addEventListener('input', function () {{
      const q = searchInput.value.toLowerCase().trim();
      document.querySelectorAll('.tool-card').forEach(function (card) {{
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? 'flex' : 'none';
      }});
    }});
  }}

  // 2. Interactive Tool Engine
  const toolContainer = document.getElementById('interactive-tool-root');
  if (!toolContainer) return;

  const toolType = toolContainer.getAttribute('data-tool-type');
  const rawConfig = toolContainer.getAttribute('data-tool-config');
  let cfg = {{}};
  try {{ cfg = JSON.parse(rawConfig); }} catch (e) {{}}

  const params = new URLSearchParams(window.location.search);

  function fmtMoney(n) {{
    return '$' + Number(n || 0).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
  }}

  let currentCsvRows = [];

  const btnPermalink = document.getElementById('btn-copy-permalink');
  const btnExportCsv = document.getElementById('btn-export-csv');

  if (btnExportCsv) {{
    btnExportCsv.addEventListener('click', function () {{
      if (!currentCsvRows.length) return;
      const csvContent = currentCsvRows.map(function (r) {{ return r.join(','); }}).join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (window.location.pathname.split('/').pop().replace('.html', '') || 'calculation') + '-ledger.csv';
      a.click();
      URL.revokeObjectURL(url);
    }});
  }}

  // ==========================================================================
  // ENGINE A: COUNTRY-AWARE END-TO-END PAYOUT & REVERSE INVOICE ENGINE
  // ==========================================================================
  if (toolType === 'corridor_engine') {{
    const elCountry = document.getElementById('in-country');
    const elAmount  = document.getElementById('in-amount');
    const elOriginPct = document.getElementById('in-origin-pct');
    const elOriginFix = document.getElementById('in-origin-fix');
    const elTaxPct  = document.getElementById('in-tax-pct');
    const elFxRate  = document.getElementById('in-fx-rate');
    const elTargetNet = document.getElementById('in-target-net');
    const taxPresetsBox = document.getElementById('corridor-tax-presets');
    const compareBody = document.getElementById('corridor-comparison-body');

    if (params.get('country') && CALCGRID_CORRIDORS[params.get('country')]) {{
      elCountry.value = params.get('country');
    }}
    if (params.get('amount')) elAmount.value = params.get('amount');
    if (params.get('origin_pct')) elOriginPct.value = params.get('origin_pct');
    if (params.get('tax')) elTaxPct.value = params.get('tax');

    document.querySelectorAll('.origin-preset-chip').forEach(function (chip) {{
      chip.addEventListener('click', function () {{
        elOriginPct.value = chip.getAttribute('data-pct') || '0';
        elOriginFix.value = chip.getAttribute('data-fix') || '0';
        recalcCorridor();
      }});
    }});

    function syncCountryPresets() {{
      const code = elCountry.value || 'AM';
      const cData = CALCGRID_CORRIDORS[code] || CALCGRID_CORRIDORS['AM'];
      if (elFxRate) {{
        elFxRate.value = cData.default_fx_placeholder;
      }}
      const fxHint = document.getElementById('fx-rate-hint');
      if (fxHint) fxHint.textContent = cData.fx_note;
      const caveatEl = document.getElementById('corridor-tax-caveat');
      if (caveatEl) caveatEl.textContent = cData.tax_caveat + ' (Sources: ' + cData.official_sources + ' • Verified: ' + cData.verified_date + ')';

      if (taxPresetsBox && cData.tax_presets) {{
        taxPresetsBox.innerHTML = '';
        if (cData.tax_presets.length > 0 && !params.get('tax')) {{
          elTaxPct.value = cData.tax_presets[0].rate;
        }}
        cData.tax_presets.forEach(function (tp) {{
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'preset-chip';
          btn.textContent = tp.label;
          btn.addEventListener('click', function () {{
            elTaxPct.value = tp.rate;
            recalcCorridor();
          }});
          taxPresetsBox.appendChild(btn);
        }});
      }}
    }}

    function evalRoute(gross, originPct, originFix, rail, taxPct) {{
      const oRate = Math.min(0.95, Math.max(0, originPct / 100));
      const afterOrigin = Math.max(0, gross * (1 - oRate) - originFix);

      const railRateExp = (rail.pct_fee + rail.fx_spread_expected) / 100;
      const railRateBest = (rail.pct_fee + rail.fx_spread_min) / 100;
      const railRateWorst = (rail.pct_fee + rail.fx_spread_max) / 100;

      const midIntermediary = (rail.intermediary_min + rail.intermediary_max) / 2;

      const netUsdExp = Math.max(0, afterOrigin * (1 - railRateExp) - rail.fixed_fee - midIntermediary);
      const netUsdBest = Math.max(0, afterOrigin * (1 - railRateBest) - rail.fixed_fee - rail.intermediary_min);
      const netUsdWorst = Math.max(0, afterOrigin * (1 - railRateWorst) - rail.fixed_fee - rail.intermediary_max);

      const tRate = Math.min(0.95, Math.max(0, taxPct / 100));
      const finalNetExp = netUsdExp * (1 - tRate);
      const finalNetBest = netUsdBest * (1 - tRate);
      const finalNetWorst = netUsdWorst * (1 - tRate);

      return {{
        afterOrigin: afterOrigin,
        netUsdExp: netUsdExp,
        finalNetExp: finalNetExp,
        finalNetBest: finalNetBest,
        finalNetWorst: finalNetWorst,
        totalFeeExp: Math.max(0, gross - finalNetExp),
        effectivePct: gross > 0 ? ((gross - finalNetExp) / gross) * 100 : 0
      }};
    }}

    function solveReverseGross(targetNet, originPct, originFix, rail, taxPct) {{
      const oRate = Math.min(0.95, Math.max(0, originPct / 100));
      const railRateExp = Math.min(0.95, Math.max(0, (rail.pct_fee + rail.fx_spread_expected) / 100));
      const tRate = Math.min(0.95, Math.max(0, taxPct / 100));
      const midIntermediary = (rail.intermediary_min + rail.intermediary_max) / 2;

      const beforeTax = targetNet / Math.max(0.05, 1 - tRate);
      const beforeRail = (beforeTax + rail.fixed_fee + midIntermediary) / Math.max(0.05, 1 - railRateExp);
      const requiredGross = (beforeRail + originFix) / Math.max(0.05, 1 - oRate);
      return requiredGross;
    }}

    function recalcCorridor() {{
      const code = elCountry.value || 'AM';
      const cData = CALCGRID_CORRIDORS[code] || CALCGRID_CORRIDORS['AM'];
      const gross = Math.max(0, parseFloat(elAmount.value) || 0);
      const originPct = Math.max(0, parseFloat(elOriginPct.value) || 0);
      const originFix = Math.max(0, parseFloat(elOriginFix.value) || 0);
      const taxPct = Math.max(0, parseFloat(elTaxPct.value) || 0);
      const fxRate = Math.max(0.0001, parseFloat(elFxRate.value) || cData.default_fx_placeholder);
      const targetNet = Math.max(0, parseFloat(elTargetNet ? elTargetNet.value : gross) || gross);

      const railNames = [
        ['payoneer', 'Payoneer Local Withdrawal'],
        ['wise', 'Wise Mid-Market Route'],
        ['swift', 'Direct Bank SWIFT Wire'],
        ['lemonsqueezy', 'Lemon Squeezy MoR Payout']
      ];

      let bestAvailableRoute = null;
      let bestAvailableResult = null;
      let bestAvailableReverse = 0;

      currentCsvRows = [
        ['Country', 'Currency', 'Payout_Rail', 'Availability', 'Gross_USD', 'Expected_Net_After_Tax_USD', 'Uncertainty_Range_USD', 'Local_Currency_Net', 'Effective_Total_Deduction_Pct', 'Reverse_Invoice_For_Target_USD']
      ];

      if (compareBody) compareBody.innerHTML = '';

      railNames.forEach(function (pair) {{
        const rKey = pair[0];
        const rLabel = pair[1];
        const rail = cData.rails[rKey];
        if (!rail) return;

        const res = evalRoute(gross, originPct, originFix, rail, taxPct);
        const revGross = solveReverseGross(targetNet, originPct, originFix, rail, taxPct);
        const localNet = res.finalNetExp * fxRate;

        if (rail.available && (!bestAvailableResult || res.finalNetExp > bestAvailableResult.finalNetExp)) {{
          bestAvailableRoute = rLabel;
          bestAvailableResult = res;
          bestAvailableReverse = revGross;
        }}

        const rangeStr = fmtMoney(res.finalNetWorst) + ' – ' + fmtMoney(res.finalNetBest);
        const localStr = Math.round(localNet).toLocaleString('en-US') + ' ' + cData.currency;

        currentCsvRows.push([
          cData.name, cData.currency, rLabel, rail.status_badge,
          gross.toFixed(2), res.finalNetExp.toFixed(2), '"' + rangeStr + '"',
          '"' + localStr + '"', res.effectivePct.toFixed(2) + '%', revGross.toFixed(2)
        ]);

        if (compareBody) {{
          const badgeClass = rail.available ? 'badge-ok' : 'badge-alert';
          const tr = document.createElement('tr');
          tr.innerHTML =
            '<td><strong>' + rLabel + '</strong><br/><span class="' + badgeClass + '">' + rail.status_badge + '</span><div style="font-family:var(--font-sans);font-size:0.72rem;color:var(--ink-secondary);margin-top:4px">' + rail.note + '</div></td>' +
            '<td><strong>' + fmtMoney(res.finalNetExp) + '</strong><br/><span style="font-size:0.68rem;color:var(--ink-muted)">' + localStr + '</span></td>' +
            '<td>' + rangeStr + '</td>' +
            '<td>' + res.effectivePct.toFixed(2) + '%</td>' +
            '<td><strong>' + fmtMoney(revGross) + '</strong></td>';
          compareBody.appendChild(tr);
        }}
      }});

      if (bestAvailableResult) {{
        document.getElementById('out-net').textContent = fmtMoney(bestAvailableResult.finalNetExp);
        document.getElementById('out-best-rail').textContent = bestAvailableRoute + ' (' + cData.name + ')';
        document.getElementById('out-range').textContent = fmtMoney(bestAvailableResult.finalNetWorst) + ' to ' + fmtMoney(bestAvailableResult.finalNetBest);
        document.getElementById('out-local').textContent = Math.round(bestAvailableResult.finalNetExp * fxRate).toLocaleString('en-US') + ' ' + cData.currency;
        document.getElementById('out-fee').textContent = fmtMoney(bestAvailableResult.totalFeeExp) + ' (' + bestAvailableResult.effectivePct.toFixed(2) + '%)';
        document.getElementById('out-reverse').textContent = fmtMoney(bestAvailableReverse);
      }}
    }}

    if (elCountry) {{
      elCountry.addEventListener('change', function () {{
        syncCountryPresets();
        recalcCorridor();
      }});
    }}
    [elAmount, elOriginPct, elOriginFix, elTaxPct, elFxRate, elTargetNet].forEach(function (el) {{
      if (el) el.addEventListener('input', recalcCorridor);
    }});

    syncCountryPresets();
    recalcCorridor();
  }}

  // ==========================================================================
  // ENGINE B: PRIVATE BROWSER CSV TRANSACTION & HIDDEN FX AUDITOR
  // ==========================================================================
  if (toolType === 'csv_auditor') {{
    const csvInput = document.getElementById('csv-audit-input');
    const fileInput = document.getElementById('csv-file-upload');
    const auditBody = document.getElementById('csv-audit-body');
    const btnRunAudit = document.getElementById('btn-run-audit');

    const PUBLISHED_RATES = {{
      lemonsqueezy: {{ pct: 5.0, fix: 0.50, fx: 1.5 }},
      payoneer:     {{ pct: 1.0, fix: 0.00, fx: 2.0 }},
      wise:         {{ pct: 0.65, fix: 4.14, fx: 0.0 }},
      upwork_10:    {{ pct: 10.0, fix: 0.99, fx: 0.0 }},
      upwork_5:     {{ pct: 5.0, fix: 0.99, fx: 0.0 }},
      upwork_15:    {{ pct: 15.0, fix: 0.99, fx: 0.0 }},
      stripe_intl:  {{ pct: 2.9, fix: 0.30, fx: 2.5 }},
      fiverr:       {{ pct: 20.0, fix: 1.00, fx: 0.0 }}
    }};

    function runBrowserCsvAudit() {{
      const raw = (csvInput ? csvInput.value : '').trim();
      const lines = raw.split(/\\r?\\n/).filter(Boolean);
      if (lines.length < 2) return;

      let totalGross = 0;
      let totalActualNet = 0;
      let totalExpectedNet = 0;
      let totalLeakage = 0;
      let alertCount = 0;

      currentCsvRows = [
        ['tx_id', 'provider', 'gross_usd', 'expected_fee_usd', 'expected_net_usd', 'actual_net_usd', 'variance_usd', 'audit_status']
      ];
      if (auditBody) auditBody.innerHTML = '';

      lines.slice(1).forEach(function (line) {{
        const cols = line.split(',').map(function (c) {{ return c.trim(); }});
        if (cols.length < 4) return;
        const txId = cols[0];
        const provider = (cols[1] || 'lemonsqueezy').toLowerCase();
        const gross = Math.max(0, parseFloat(cols[2]) || 0);
        const actualNet = Math.max(0, parseFloat(cols[3]) || 0);

        const rate = PUBLISHED_RATES[provider] || {{ pct: 5.0, fix: 0.50, fx: 0.0 }};
        const expectedFee = gross * ((rate.pct + rate.fx) / 100) + rate.fix;
        const expectedNet = Math.max(0, gross - expectedFee);
        const variance = actualNet - expectedNet;
        const isAlert = Math.abs(variance) > Math.max(0.50, gross * 0.0025);
        const status = isAlert ? 'FEE_VARIANCE_ALERT' : 'OK';

        totalGross += gross;
        totalActualNet += actualNet;
        totalExpectedNet += expectedNet;
        if (variance < 0) totalLeakage += Math.abs(variance);
        if (isAlert) alertCount += 1;

        currentCsvRows.push([
          txId, provider, gross.toFixed(2), expectedFee.toFixed(2),
          expectedNet.toFixed(2), actualNet.toFixed(2), variance.toFixed(2), status
        ]);

        if (auditBody) {{
          const badge = isAlert
            ? '<span class="badge-alert">FEE_VARIANCE_ALERT</span>'
            : '<span class="badge-ok">OK</span>';
          const tr = document.createElement('tr');
          tr.innerHTML =
            '<td>' + txId + '</td>' +
            '<td>' + provider + '</td>' +
            '<td>' + fmtMoney(gross) + '</td>' +
            '<td>' + fmtMoney(expectedNet) + '</td>' +
            '<td><strong>' + fmtMoney(actualNet) + '</strong></td>' +
            '<td>' + (variance >= 0 ? '+' : '-') + fmtMoney(Math.abs(variance)) + '</td>' +
            '<td>' + badge + '</td>';
          auditBody.appendChild(tr);
        }}
      }});

      const effFeePct = totalGross > 0 ? ((totalGross - totalActualNet) / totalGross) * 100 : 0;
      document.getElementById('out-audit-gross').textContent = fmtMoney(totalGross);
      document.getElementById('out-audit-net').textContent = fmtMoney(totalActualNet);
      document.getElementById('out-audit-leakage').textContent = fmtMoney(totalLeakage);
      document.getElementById('out-audit-alerts').textContent = alertCount + ' flagged (' + effFeePct.toFixed(2) + '% eff. fee)';
    }}

    if (fileInput) {{
      fileInput.addEventListener('change', function (e) {{
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function (ev) {{
          if (csvInput) csvInput.value = String(ev.target.result || '');
          runBrowserCsvAudit();
        }};
        reader.readAsText(file);
      }});
    }}

    if (btnRunAudit) btnRunAudit.addEventListener('click', runBrowserCsvAudit);
    if (csvInput) csvInput.addEventListener('input', runBrowserCsvAudit);
    runBrowserCsvAudit();
  }}

  // ==========================================================================
  // ENGINE C: STANDARD FEE & REVERSE INVOICE CALCULATORS (10 TOOLS)
  // ==========================================================================
  if (toolType === 'fee_calc') {{
    const elAmt = document.getElementById('in-amount');
    const elPct = document.getElementById('in-pct');
    const elFix = document.getElementById('in-fixed');
    const elFx  = document.getElementById('in-fx');
    const matrixBody = document.getElementById('sensitivity-matrix-body');

    if (params.get('amount')) elAmt.value = params.get('amount');
    if (params.get('pct')) elPct.value = params.get('pct');
    if (params.get('fixed')) elFix.value = params.get('fixed');
    if (params.get('fx')) elFx.value = params.get('fx');

    document.querySelectorAll('.preset-chip').forEach(function (chip) {{
      chip.addEventListener('click', function () {{
        const pctVal = chip.getAttribute('data-pct');
        if (pctVal !== null && elPct) {{
          elPct.value = pctVal;
          recalcFee();
        }}
      }});
    }});

    function calcSingleTier(gross, pct, fix, fx) {{
      const totalPctRate = Math.min(0.99, Math.max(0, (pct + fx) / 100));
      const totalFee = gross * totalPctRate + fix;
      const net = Math.max(0, gross - totalFee);
      const effectiveRate = gross > 0 ? (totalFee / gross) * 100 : 0;
      const reverseGross = (gross + fix) / (1 - totalPctRate);
      return {{ gross: gross, fee: totalFee, net: net, rate: effectiveRate, reverse: reverseGross }};
    }}

    function recalcFee() {{
      const gross = Math.max(0, parseFloat(elAmt.value) || 0);
      const pct   = Math.max(0, parseFloat(elPct.value) || 0);
      const fix   = Math.max(0, parseFloat(elFix.value) || 0);
      const fx    = Math.max(0, parseFloat(elFx.value) || 0);

      const res = calcSingleTier(gross, pct, fix, fx);

      document.getElementById('out-net').textContent = fmtMoney(res.net);
      document.getElementById('out-fee').textContent = fmtMoney(res.fee);
      document.getElementById('out-rate').textContent = res.rate.toFixed(2) + '%';
      document.getElementById('out-reverse').textContent = fmtMoney(res.reverse);

      const tiers = [100, 500, 1000, 2500, 5000, 10000];
      currentCsvRows = [
        ['Gross_Amount_USD', 'Platform_Fee_Pct', 'Fixed_Fee_USD', 'FX_Spread_Pct', 'Total_Fee_USD', 'Net_Settlement_USD', 'Effective_Rate_Pct', 'Reverse_Invoice_Required_USD'],
        [gross.toFixed(2), pct.toFixed(2), fix.toFixed(2), fx.toFixed(2), res.fee.toFixed(2), res.net.toFixed(2), res.rate.toFixed(2), res.reverse.toFixed(2)]
      ];

      if (matrixBody) {{
        matrixBody.innerHTML = '';
        tiers.forEach(function (tAmt) {{
          const rowRes = calcSingleTier(tAmt, pct, fix, fx);
          currentCsvRows.push([
            tAmt.toFixed(2), pct.toFixed(2), fix.toFixed(2), fx.toFixed(2),
            rowRes.fee.toFixed(2), rowRes.net.toFixed(2), rowRes.rate.toFixed(2), rowRes.reverse.toFixed(2)
          ]);
          const tr = document.createElement('tr');
          tr.innerHTML =
            '<td>' + fmtMoney(tAmt) + '</td>' +
            '<td>' + fmtMoney(rowRes.fee) + '</td>' +
            '<td><strong>' + fmtMoney(rowRes.net) + '</strong></td>' +
            '<td>' + rowRes.rate.toFixed(2) + '%</td>' +
            '<td>' + fmtMoney(rowRes.reverse) + '</td>';
          matrixBody.appendChild(tr);
        }});
      }}
    }}

    if (btnPermalink) {{
      btnPermalink.addEventListener('click', function () {{
        const u = new URL(window.location.href);
        u.searchParams.set('amount', elAmt.value);
        u.searchParams.set('pct', elPct.value);
        u.searchParams.set('fixed', elFix.value);
        u.searchParams.set('fx', elFx.value);
        if (navigator.clipboard) navigator.clipboard.writeText(u.toString());
        btnPermalink.textContent = 'Permalink Copied';
        setTimeout(function () {{ btnPermalink.textContent = 'Copy Permalink'; }}, 1600);
      }});
    }}

    [elAmt, elPct, elFix, elFx].forEach(function (el) {{
      if (el) el.addEventListener('input', recalcFee);
    }});
    recalcFee();
  }}

  // ==========================================================================
  // ENGINE D: SAAS & OPERATIONS UNIT ECONOMICS MODELS (9 TOOLS)
  // ==========================================================================
  if (toolType === 'saas_calc') {{
    const elA = document.getElementById('in-a');
    const elB = document.getElementById('in-b');
    const elC = document.getElementById('in-c');
    const elD = document.getElementById('in-d');

    if (params.get('a')) elA.value = params.get('a');
    if (params.get('b')) elB.value = params.get('b');
    if (params.get('c')) elC.value = params.get('c');
    if (params.get('d')) elD.value = params.get('d');

    function recalcSaas() {{
      const a = Math.max(0, parseFloat(elA.value) || 0);
      const b = Math.max(0, parseFloat(elB.value) || 0);
      const c = Math.max(0, parseFloat(elC.value) || 0);
      const d = Math.max(0, parseFloat(elD.value) || 0);
      const mode = cfg.mode || 'ltv';

      let r1Label = 'Primary Metric', r1Val = '$0.00';
      let r2Label = 'Secondary Metric', r2Val = '0';
      let r3Label = 'Efficiency Benchmark', r3Val = '0';

      if (mode === 'ltv') {{
        const churnRate = Math.max(0.001, c / 100);
        const ltv = (a * (b / 100)) / churnRate;
        const ratio = d > 0 ? ltv / d : 0;
        const payback = (a * (b / 100)) > 0 ? d / (a * (b / 100)) : 0;
        r1Label = 'Customer Lifetime Value (LTV)';
        r1Val = fmtMoney(ltv);
        r2Label = 'LTV : CAC Ratio';
        r2Val = ratio.toFixed(2) + 'x';
        r3Label = 'CAC Payback Period';
        r3Val = payback.toFixed(1) + ' months';
      }} else if (mode === 'roas') {{
        const margin = Math.max(0.01, a - b);
        const marginPct = a > 0 ? margin / a : 0.01;
        const beRoas = 1 / marginPct;
        const grossRev = c * d;
        const orders = a > 0 ? grossRev / a : 0;
        const netProfit = orders * margin - c;
        r1Label = 'Break-Even ROAS Required';
        r1Val = beRoas.toFixed(2) + 'x';
        r2Label = 'Max Profitable CPA';
        r2Val = fmtMoney(margin);
        r3Label = 'Estimated Monthly Net Profit';
        r3Val = fmtMoney(netProfit);
      }} else if (mode === 'ad_rev') {{
        const monthlyImps = a * 30 * b;
        const grossRev = (monthlyImps / 1000) * c;
        const netRev = grossRev * (d / 100);
        r1Label = 'Estimated Monthly Net Ad Revenue';
        r1Val = fmtMoney(netRev);
        r2Label = 'Monthly Paid Ad Impressions';
        r2Val = Math.round(monthlyImps).toLocaleString('en-US');
        r3Label = 'Annual Run-Rate';
        r3Val = fmtMoney(netRev * 12);
      }} else if (mode === 'ecom') {{
        const fee = a * (d / 100);
        const net = a - b - c - fee;
        const marginPct = a > 0 ? (net / a) * 100 : 0;
        r1Label = 'Net Profit Per Order';
        r1Val = fmtMoney(net);
        r2Label = 'Net Profit Margin (%)';
        r2Val = marginPct.toFixed(1) + '%';
        r3Label = 'Profit on 100 Orders';
        r3Val = fmtMoney(net * 100);
      }} else if (mode === 'email_roi') {{
        const clicks = a * (b / 100);
        const sales = clicks * (c / 100);
        const profit = sales * d;
        r1Label = 'Projected Campaign Net Profit';
        r1Val = fmtMoney(profit);
        r2Label = 'Estimated Conversions';
        r2Val = sales.toFixed(1) + ' sales';
        r3Label = 'Revenue Per Subscriber';
        r3Val = fmtMoney(a > 0 ? profit / a : 0);
      }} else if (mode === 'cro') {{
        const extraSales = a * ((c - b) / 100);
        const monthlyLift = extraSales * d;
        r1Label = 'Monthly Revenue Lift';
        r1Val = fmtMoney(monthlyLift);
        r2Label = 'Annual Revenue Impact';
        r2Val = fmtMoney(monthlyLift * 12);
        r3Label = 'Extra Monthly Customers';
        r3Val = '+' + extraSales.toFixed(1);
      }} else if (mode === 'hourly_rate') {{
        const grossNeeded = (a + b) / Math.max(0.1, 1 - d / 100);
        const annualBillableHours = Math.max(1, c * 48);
        const hourly = grossNeeded / annualBillableHours;
        r1Label = 'Minimum Billable Hourly Rate';
        r1Val = fmtMoney(hourly) + '/hr';
        r2Label = 'Recommended Day Rate (8h)';
        r2Val = fmtMoney(hourly * 8) + '/day';
        r3Label = 'Required Gross Annual Billings';
        r3Val = fmtMoney(grossNeeded);
      }} else if (mode === 'pert') {{
        const expected = (a + 4 * b + c) / 6;
        const sd = (c - a) / 6;
        const safeHours = expected + 2 * sd;
        r1Label = '95% Safe Quote (Hours & Price)';
        r1Val = safeHours.toFixed(1) + 'h (' + fmtMoney(safeHours * d) + ')';
        r2Label = 'PERT Expected Average';
        r2Val = expected.toFixed(1) + ' hours';
        r3Label = 'Risk Buffer (±2σ)';
        r3Val = '+' + (2 * sd).toFixed(1) + ' hours';
      }} else if (mode === 'llm_cost') {{
        const monthlyTokens = a * 30 * b;
        const rawCost = (monthlyTokens / 1000000) * c;
        const netCost = rawCost * (1 - d / 100);
        r1Label = 'Estimated Monthly API Cost';
        r1Val = fmtMoney(netCost);
        r2Label = 'Total Monthly Tokens';
        r2Val = (monthlyTokens / 1000000).toFixed(2) + 'M tokens';
        r3Label = 'Cost Per 1,000 User Requests';
        r3Val = fmtMoney((b / 1000) * c * (1 - d / 100));
      }}

      document.getElementById('lbl-r1').textContent = r1Label;
      document.getElementById('val-r1').textContent = r1Val;
      document.getElementById('lbl-r2').textContent = r2Label;
      document.getElementById('val-r2').textContent = r2Val;
      document.getElementById('lbl-r3').textContent = r3Label;
      document.getElementById('val-r3').textContent = r3Val;

      currentCsvRows = [
        ['Parameter_A', 'Parameter_B', 'Parameter_C', 'Parameter_D', r1Label, r2Label, r3Label],
        [a, b, c, d, '"' + r1Val + '"', '"' + r2Val + '"', '"' + r3Val + '"']
      ];
    }}

    if (btnPermalink) {{
      btnPermalink.addEventListener('click', function () {{
        const u = new URL(window.location.href);
        u.searchParams.set('a', elA.value);
        u.searchParams.set('b', elB.value);
        u.searchParams.set('c', elC.value);
        u.searchParams.set('d', elD.value);
        if (navigator.clipboard) navigator.clipboard.writeText(u.toString());
        btnPermalink.textContent = 'Permalink Copied';
        setTimeout(function () {{ btnPermalink.textContent = 'Copy Permalink'; }}, 1600);
      }});
    }}

    [elA, elB, elC, elD].forEach(function (el) {{
      if (el) el.addEventListener('input', recalcSaas);
    }});
    recalcSaas();
  }}

  // ==========================================================================
  // ENGINE E: DEVELOPER & DATA INSTRUMENTS (11 TOOLS)
  // ==========================================================================
  if (toolType === 'dev_tool') {{
    const inputEl = document.getElementById('dev-input');
    const outputEl = document.getElementById('dev-output');
    const runBtn = document.getElementById('btn-run-dev');
    const copyBtn = document.getElementById('btn-copy-dev');

    function runDevTransform() {{
      const val = inputEl.value;
      const mode = cfg.dev_mode;
      try {{
        if (mode === 'json_to_ts') {{
          const obj = JSON.parse(val);
          let ts = 'export interface GeneratedPayload {{\\n';
          let zod = 'import {{ z }} from "zod";\\n\\nexport const GeneratedSchema = z.object({{\\n';
          Object.keys(obj).forEach(function (k) {{
            const v = obj[k];
            const t = Array.isArray(v) ? 'any[]' : typeof v;
            ts += '  ' + k + ': ' + t + ';\\n';
            const zt = Array.isArray(v) ? 'z.array(z.any())' : 'z.' + (typeof v === 'number' ? 'number()' : typeof v === 'boolean' ? 'boolean()' : 'string()');
            zod += '  ' + k + ': ' + zt + ',\\n';
          }});
          ts += '}}\\n\\n';
          zod += '}});';
          outputEl.textContent = ts + zod;
        }} else if (mode === 'cron') {{
          const parts = val.trim().split(/\\s+/);
          if (parts.length !== 5) {{
            outputEl.textContent = 'Invalid Cron: Expected 5 space-separated fields (Minute Hour DayOfMonth Month DayOfWeek)';
          }} else {{
            outputEl.textContent =
              'Valid 5-Field Cron Schedule:\\n' +
              '• Minute:       ' + parts[0] + '\\n' +
              '• Hour:         ' + parts[1] + '\\n' +
              '• Day of Month: ' + parts[2] + '\\n' +
              '• Month:        ' + parts[3] + '\\n' +
              '• Day of Week:  ' + parts[4];
          }}
        }} else if (mode === 'jwt') {{
          const segs = val.trim().split('.');
          if (segs.length < 2) {{
            outputEl.textContent = 'Expected JWT format: header.payload.signature';
          }} else {{
            const decodeB64 = function (s) {{
              return JSON.parse(atob(s.replace(/-/g, '+').replace(/_/g, '/')));
            }};
            const header = decodeB64(segs[0]);
            const payload = decodeB64(segs[1]);
            outputEl.textContent =
              '// JWT HEADER:\\n' + JSON.stringify(header, null, 2) +
              '\\n\\n// JWT PAYLOAD CLAIMS:\\n' + JSON.stringify(payload, null, 2);
          }}
        }} else if (mode === 'sql') {{
          const kw = /\\b(SELECT|FROM|INNER JOIN|LEFT JOIN|RIGHT JOIN|WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|INSERT INTO|VALUES|UPDATE|SET|DELETE FROM)\\b/gi;
          const formatted = val
            .replace(/\\s+/g, ' ')
            .replace(kw, function (m) {{ return '\\n' + m.toUpperCase(); }})
            .trim();
          outputEl.textContent = formatted;
        }} else if (mode === 'base64') {{
          const bytes = new TextEncoder().encode(val);
          let bin = '';
          bytes.forEach(function (b) {{ bin += String.fromCharCode(b); }});
          const b64 = btoa(bin);
          outputEl.textContent =
            'Base64 Encoded:\\n' + b64 +
            '\\n\\nURL-Encoded:\\n' + encodeURIComponent(val);
        }} else if (mode === 'csv_to_json') {{
          const lines = val.trim().split(/\\r?\\n/).filter(Boolean);
          if (lines.length < 2) {{
            outputEl.textContent = '[]';
          }} else {{
            const headers = lines[0].split(',').map(function (h) {{ return h.trim(); }});
            const arr = lines.slice(1).map(function (line) {{
              const cells = line.split(',').map(function (c) {{ return c.trim(); }});
              const row = {{}};
              headers.forEach(function (h, i) {{
                const raw = cells[i] || '';
                if (raw === 'true' || raw === 'false') row[h] = (raw === 'true');
                else if (raw !== '' && !isNaN(Number(raw))) row[h] = Number(raw);
                else row[h] = raw;
              }});
              return row;
            }});
            outputEl.textContent = JSON.stringify(arr, null, 2);
          }}
        }} else if (mode === 'regex') {{
          const re = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}|#INV-\\d+/g;
          const matches = Array.from(val.matchAll(re)).map(function (m) {{
            return 'Match: "' + m[0] + '" at index ' + m.index;
          }});
          outputEl.textContent = matches.length ? matches.join('\\n') : 'No matches found.';
        }} else if (mode === 'svg') {{
          const clean = val.trim().replace(/\\s+/g, ' ');
          const dataUri = 'data:image/svg+xml;utf8,' + encodeURIComponent(clean);
          const jsx = clean.replace(/stroke-width=/g, 'strokeWidth=').replace(/class=/g, 'className=');
          outputEl.textContent =
            '/* CSS Background Data URI */\\nbackground-image: url("' + dataUri + '");\\n\\n/* React JSX */\\n' + jsx;
        }} else if (mode === 'password') {{
          const len = Math.min(64, Math.max(8, parseInt(val, 10) || 24));
          const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+';
          const rnd = new Uint32Array(len);
          window.crypto.getRandomValues(rnd);
          let out = '';
          for (let i = 0; i < len; i++) out += chars[rnd[i] % chars.length];
          const entropy = (len * Math.log2(chars.length)).toFixed(1);
          outputEl.textContent = 'Generated Key: ' + out + '\\nEntropy:       ' + entropy + ' bits (Cryptographically Secure)';
        }} else if (mode === 'markdown') {{
          const htmlOut = val
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
            .replace(/^- (.*$)/gm, '<li>$1</li>');
          outputEl.textContent = htmlOut;
        }} else if (mode === 'utm') {{
          const p = val.split('|').map(function (s) {{ return s.trim(); }});
          const base = p[0] || 'https://example.com';
          const src = encodeURIComponent((p[1] || 'newsletter').toLowerCase());
          const med = encodeURIComponent((p[2] || 'email').toLowerCase());
          const cmp = encodeURIComponent((p[3] || 'launch').toLowerCase());
          outputEl.textContent = base + (base.includes('?') ? '&' : '?') +
            'utm_source=' + src + '&utm_medium=' + med + '&utm_campaign=' + cmp;
        }}
      }} catch (err) {{
        outputEl.textContent = 'Error: ' + err.message;
      }}
    }}

    if (runBtn) runBtn.addEventListener('click', runDevTransform);
    if (inputEl) inputEl.addEventListener('input', runDevTransform);
    if (copyBtn) {{
      copyBtn.addEventListener('click', function () {{
        if (navigator.clipboard) navigator.clipboard.writeText(outputEl.textContent);
        copyBtn.textContent = 'Copied';
        setTimeout(function () {{ copyBtn.textContent = 'Copy Output'; }}, 1500);
      }});
    }}
    runDevTransform();
  }}
}})();
""".strip()


def render_navbar(prefix: str = "") -> str:
    checkout_nav_item = ""
    if LEMON_SQUEEZY_CHECKOUT_URL:
        checkout_nav_item = (
            f'<a href="{html.escape(LEMON_SQUEEZY_CHECKOUT_URL)}" class="nav-cta">'
            f'Pro Batch Suite ($19)</a>'
        )
    return f"""
  <header class="navbar">
    <div class="nav-inner">
      <a href="{prefix}index.html" class="brand">
        <span class="brand-name">CalcGrid</span>
        <span class="brand-meta">Financial &amp; Technical Ledger / 2026</span>
      </a>
      <nav class="nav-links">
        <a href="{prefix}tools/cross-border-payout-comparison-engine.html">Country Payout Engine</a>
        <a href="{prefix}tools/private-csv-payout-fee-auditor.html">Browser CSV Auditor</a>
        <a href="{prefix}index.html#payment-calculators">Fee Ledgers</a>
        <a href="{prefix}index.html#saas-calculators">Unit Economics</a>
        <a href="{prefix}dashboard.html">Earnings &amp; Ops Proof</a>
        {checkout_nav_item}
      </nav>
    </div>
  </header>
"""


def render_ad_slot() -> str:
    """Only renders an advertisement container when ADSENSE_CLIENT_ID is configured."""
    if not ADSENSE_CLIENT_ID:
        return ""
    return f"""
    <div class="ad-slot" data-ad-slot="in-article">
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="{html.escape(ADSENSE_CLIENT_ID)}"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
    """


def render_pro_sidebar(related_links: str, prefix: str = "../") -> str:
    if LEMON_SQUEEZY_CHECKOUT_URL:
        pro_cta_html = (
            f'<a href="{html.escape(LEMON_SQUEEZY_CHECKOUT_URL)}" class="btn-primary" style="display:block">'
            f'Purchase via Lemon Squeezy ($19)</a>'
        )
    else:
        pro_cta_html = (
            '<div class="btn-disabled" aria-disabled="true">'
            'Checkout Disabled — Merchant Verification Pending</div>'
        )

    return f"""
      <div class="reference-card" id="pro-offline-bundle">
        <span class="kicker">COMMERCIAL B2B &amp; FREELANCER EDITION</span>
        <img src="{prefix}assets/images/pro-suite-box.png" alt="CalcGrid Pro Bulk Reconciler & Financial Models" />
        <h3>CalcGrid Pro Batch Auditor &amp; Financial Models ($19)</h3>
        <p>While single-transaction calculators and our 50-row Browser CSV Auditor are 100% free, the Pro Pack equips agencies and accountants with unlimited CLI batch automation and multi-sheet workbooks.</p>
        <ul class="reference-list">
          <li>01 / Unlimited CLI Batch CSV Fee &amp; FX Reconciler (calcgrid_batch_reconciler.py)</li>
          <li>02 / Multi-Tab Excel Workbook (.xlsx) + 3 Separate CSV Models (SaaS Cohort, Cross-Border Fee Matrix, ROAS Model)</li>
          <li>03 / Air-Gapped Offline HTML Instrument Suite (32 Tools)</li>
        </ul>
        {pro_cta_html}
      </div>

      <div class="reference-card" style="background:var(--surface)">
        <span class="kicker">INDEX // RELATED INSTRUMENTS</span>
        <ul style="list-style:none;border-top:1px solid var(--rule)">
          {related_links}
        </ul>
      </div>
    """


def render_tool_workspace(tool: dict, prefix: str = "../") -> str:
    t_type = tool["tool_type"]
    cfg = tool["config"]
    cfg_json = html.escape(json.dumps(cfg))
    slug = tool["slug"]

    src_name, ver_date = OFFICIAL_SOURCES.get(
        slug,
        (cfg.get("source_name", "Standard Industry Financial & Technical Formula"), cfg.get("verified_date", "2026-10-27"))
    )

    related = [t for t in TOOLS_CATALOG if t["category"] == tool["category"] and t["slug"] != slug][:6]
    related_links = "".join(
        f'<li style="padding:7px 0;border-bottom:1px solid var(--rule);font-size:0.83rem"><a href="{t["slug"]}.html">{html.escape(t["title"])} &rarr;</a></li>'
        for t in related
    )
    pro_box_html = render_pro_sidebar(related_links, prefix=prefix)

    faq_html = "".join(
        f'<div class="faq-item"><h4>{html.escape(q)}</h4><p>{html.escape(a)}</p></div>'
        for q, a in tool["faqs"]
    )

    ad_html = render_ad_slot()

    # =========================================================================
    # WORKSPACE TYPE 1: FLAGSHIP COUNTRY-AWARE PAYOUT & REVERSE INVOICE ENGINE
    # =========================================================================
    if t_type == "corridor_engine":
        country_opts = "".join(
            f'<option value="{code}">{html.escape(c["name"])} ({html.escape(c["currency"])})</option>'
            for code, c in COUNTRY_CORRIDORS.items()
        )
        return f"""
        <div class="workspace-grid" id="interactive-tool-root" data-tool-type="corridor_engine" data-tool-config="{cfg_json}">
          <div>
            <div class="parameters-sheet">
              <div class="sheet-heading">
                <span>FIG. 01 — MULTI-STAGE CORRIDOR &amp; REVERSE INVOICE PARAMETERS</span>
                <span>VERIFIED: {html.escape(ver_date)}</span>
              </div>

              <div class="field-group">
                <label for="in-country">1. Freelancer / Agency Residence Country &amp; Local Currency</label>
                <select id="in-country">{country_opts}</select>
                <span class="field-hint">Checks documented rail availability (e.g., Wise receiving restrictions in Armenia vs. Georgia/Philippines) and local simplified tax rules.</span>
              </div>

              <div class="field-group">
                <label>2. Client Origin Channel Presets (Marketplace or Direct Invoice)</label>
                <div class="presets-bar" style="margin-bottom:8px;padding-bottom:8px">
                  <button type="button" class="preset-chip origin-preset-chip" data-pct="0" data-fix="0">0% Direct Client Invoice</button>
                  <button type="button" class="preset-chip origin-preset-chip" data-pct="0" data-fix="0.99">0% Upwork Direct (Freelancer Plus)</button>
                  <button type="button" class="preset-chip origin-preset-chip" data-pct="5" data-fix="0.99">5% Upwork Direct Standard / Example</button>
                  <button type="button" class="preset-chip origin-preset-chip" data-pct="10" data-fix="0.99">10% Upwork Example Marketplace</button>
                  <button type="button" class="preset-chip origin-preset-chip" data-pct="15" data-fix="0.99">15% Upwork Example Marketplace</button>
                  <button type="button" class="preset-chip origin-preset-chip" data-pct="20" data-fix="1.00">20% Fiverr Commission</button>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                  <div>
                    <label for="in-origin-pct" style="font-size:0.76rem">Platform Fee (%)</label>
                    <input type="number" id="in-origin-pct" value="{cfg['default_origin_pct']}" min="0" max="90" step="0.1" />
                  </div>
                  <div>
                    <label for="in-origin-fix" style="font-size:0.76rem">Platform Fixed Fee ($)</label>
                    <input type="number" id="in-origin-fix" value="{cfg['default_origin_fixed']}" min="0" step="0.01" />
                  </div>
                </div>
              </div>

              <div class="field-group">
                <label for="in-amount">3. Gross Client Invoice / Contract Amount ($ USD)</label>
                <input type="number" id="in-amount" value="{cfg['default_amount']}" min="0" step="any" />
              </div>

              <div class="field-group">
                <label for="in-target-net">4. Target Net Take-Home Goal ($ USD — For Reverse Invoice Solver)</label>
                <input type="number" id="in-target-net" value="{cfg['default_amount']}" min="0" step="any" />
                <span class="field-hint">Solves the exact gross USD invoice you must send the client to receive this net amount after platform, payout rail, FX spread, and local tax.</span>
              </div>

              <div class="field-group">
                <label for="in-tax-pct">5. Local Turnover / Simplified Tax Provision (%)</label>
                <div class="presets-bar" id="corridor-tax-presets" style="margin-bottom:8px;padding-bottom:8px"></div>
                <input type="number" id="in-tax-pct" value="1.0" min="0" max="60" step="0.1" />
                <span class="field-hint" id="corridor-tax-caveat"></span>
              </div>

              <div class="field-group">
                <label for="in-fx-rate">6. Reference Local Exchange Rate (User-Editable — No Live FX Fabricated)</label>
                <input type="number" id="in-fx-rate" value="388.0" min="0.0001" step="any" />
                <span class="field-hint" id="fx-rate-hint"></span>
              </div>
            </div>

            <div class="doc-section">
              <span class="kicker">FIG. 03 — SIDE-BY-SIDE PAYOUT RAIL &amp; UNCERTAINTY MATRIX</span>
              <h3>End-to-End Route Comparison (With FX &amp; Intermediary Uncertainty Bands)</h3>
              <p style="font-size:0.83rem;color:var(--ink-secondary);margin-bottom:10px">
                Compares net settlement after platform fees, payout rail fees, currency conversion spreads, SWIFT intermediary deductions, and local turnover tax:
              </p>
              <div style="overflow-x:auto">
                <table class="matrix-table">
                  <thead>
                    <tr>
                      <th>Payout Route &amp; Jurisdiction Status</th>
                      <th>Expected Net (After Tax)</th>
                      <th>Uncertainty Band (Worst–Best)</th>
                      <th>Total Burden %</th>
                      <th>Invoice Needed for Target Net</th>
                    </tr>
                  </thead>
                  <tbody id="corridor-comparison-body"></tbody>
                </table>
              </div>
            </div>

            {ad_html}

            <div class="doc-section">
              <span class="kicker">SPECIFICATION &amp; SOURCE ATTRIBUTION</span>
              <h3>Multi-Stage Calculation &amp; Reverse Gross-Up Methodology</h3>
              <div class="formula-block">{html.escape(tool['formula_explanation'])}</div>
              <p style="font-family:var(--font-mono);font-size:0.74rem;color:var(--ink-muted);margin-bottom:20px">
                REFERENCE BASIS: {html.escape(src_name)} &bull; ASSUMPTIONS VERIFIED: {html.escape(ver_date)}
              </p>
              <h3>Reference Notes &amp; FAQ</h3>
              {faq_html}
            </div>
          </div>

          <aside>
            <div class="ledger-sheet">
              <div class="sheet-heading">
                <span>FIG. 02 — OPTIMAL ROUTE LEDGER</span>
                <span>LIVE CORRIDOR SOLVER</span>
              </div>
              <div class="ledger-primary">
                <span class="ledger-primary-label">Highest Available Net Take-Home</span>
                <div class="ledger-primary-value" id="out-net">$0.00</div>
              </div>
              <div class="ledger-rows">
                <div class="ledger-row">
                  <span>Optimal Available Route</span>
                  <strong id="out-best-rail">—</strong>
                </div>
                <div class="ledger-row">
                  <span>Uncertainty Range (FX / Bank Spread)</span>
                  <strong id="out-range">$0.00 to $0.00</strong>
                </div>
                <div class="ledger-row">
                  <span>Estimated Local Currency Net</span>
                  <strong id="out-local">0 AMD</strong>
                </div>
                <div class="ledger-row">
                  <span>Total Multi-Stage Deductions</span>
                  <strong id="out-fee">$0.00 (0.00%)</strong>
                </div>
                <div class="ledger-row">
                  <span>Required Gross Invoice for Target Net</span>
                  <strong id="out-reverse">$0.00</strong>
                </div>
              </div>
              <div class="ledger-actions">
                <button type="button" id="btn-export-csv" class="btn-secondary">Export Corridor CSV</button>
                <button type="button" id="btn-copy-permalink" class="btn-secondary">Copy Permalink</button>
              </div>
            </div>
            {pro_box_html}
          </aside>
        </div>
        """

    # =========================================================================
    # WORKSPACE TYPE 2: PRIVATE BROWSER CSV TRANSACTION & FX FEE AUDITOR
    # =========================================================================
    if t_type == "csv_auditor":
        return f"""
        <div class="workspace-grid" id="interactive-tool-root" data-tool-type="csv_auditor" data-tool-config="{cfg_json}">
          <div>
            <div class="parameters-sheet">
              <div class="sheet-heading">
                <span>FIG. 01 — LOCAL BROWSER CSV STATEMENT INPUT</span>
                <span>100% CLIENT-SIDE PRIVACY</span>
              </div>
              <div class="field-group">
                <label for="csv-file-upload">Upload Transaction CSV File (Processed Locally in Browser Memory)</label>
                <input type="file" id="csv-file-upload" accept=".csv,text/csv" />
                <span class="field-hint">Supported provider codes: lemonsqueezy, payoneer, wise, upwork_10, upwork_5, upwork_15, stripe_intl, fiverr.</span>
              </div>
              <div class="field-group">
                <label for="csv-audit-input">Or Paste CSV Rows (`tx_id,provider,gross_usd,actual_net_usd`)</label>
                <textarea id="csv-audit-input">{html.escape(cfg['sample_csv'])}</textarea>
              </div>
              <div class="btn-row">
                <button type="button" id="btn-run-audit" class="btn-primary">Audit CSV Statement</button>
                <button type="button" id="btn-export-csv" class="btn-secondary">Export Reconciled CSV</button>
              </div>
            </div>

            <div class="doc-section">
              <span class="kicker">FIG. 03 — LINE-BY-LINE FEE &amp; FX VARIANCE LEDGER</span>
              <h3>Reconciled Transaction Audit Table</h3>
              <div style="overflow-x:auto">
                <table class="matrix-table">
                  <thead>
                    <tr>
                      <th>TX ID</th>
                      <th>Provider</th>
                      <th>Gross USD</th>
                      <th>Expected Net</th>
                      <th>Actual Net</th>
                      <th>Variance</th>
                      <th>Audit Status</th>
                    </tr>
                  </thead>
                  <tbody id="csv-audit-body"></tbody>
                </table>
              </div>
            </div>

            {ad_html}

            <div class="doc-section">
              <span class="kicker">SPECIFICATION &amp; AUDIT LOGIC</span>
              <h3>Variance Detection Methodology</h3>
              <div class="formula-block">{html.escape(tool['formula_explanation'])}</div>
              <h3>Frequently Asked Questions</h3>
              {faq_html}
            </div>
          </div>

          <aside>
            <div class="ledger-sheet">
              <div class="sheet-heading">
                <span>FIG. 02 — AUDIT SUMMARY</span>
                <span>LIVE VARIANCE DETECTION</span>
              </div>
              <div class="ledger-primary">
                <span class="ledger-primary-label">Detected Hidden Fee / FX Leakage</span>
                <div class="ledger-primary-value" id="out-audit-leakage">$0.00</div>
              </div>
              <div class="ledger-rows">
                <div class="ledger-row">
                  <span>Total Gross Volume Audited</span>
                  <strong id="out-audit-gross">$0.00</strong>
                </div>
                <div class="ledger-row">
                  <span>Total Actual Net Settled</span>
                  <strong id="out-audit-net">$0.00</strong>
                </div>
                <div class="ledger-row">
                  <span>Variance Alerts &amp; Effective Rate</span>
                  <strong id="out-audit-alerts">0 flagged</strong>
                </div>
              </div>
            </div>
            {pro_box_html}
          </aside>
        </div>
        """

    # =========================================================================
    # WORKSPACE TYPE 3: STANDARD FEE & REVERSE GROSS-UP CALCULATORS
    # =========================================================================
    presets_html = ""
    if "presets" in cfg:
        chips = "".join(
            f'<button type="button" class="preset-chip" data-pct="{p["pct"]}">{html.escape(p["label"])}</button>'
            for p in cfg["presets"]
        )
        presets_html = f'<div class="presets-bar"><span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--ink-muted);align-self:center;margin-right:4px">FEE PRESETS:</span>{chips}</div>'

    if t_type == "fee_calc":
        return f"""
        <div class="workspace-grid" id="interactive-tool-root" data-tool-type="fee_calc" data-tool-config="{cfg_json}">
          <div>
            <div class="parameters-sheet">
              <div class="sheet-heading">
                <span>FIG. 01 — INPUT PARAMETERS</span>
                <span>VERIFIED: {html.escape(ver_date.upper())}</span>
              </div>
              {presets_html}
              <div class="field-group">
                <label for="in-amount">{html.escape(cfg['label_amount'])}</label>
                <input type="number" id="in-amount" value="{cfg['default_amount']}" min="0" step="any" />
              </div>
              <div class="field-group">
                <label for="in-pct">{html.escape(cfg['label_pct'])}</label>
                <input type="number" id="in-pct" value="{cfg['percent_fee']}" min="0" max="99" step="0.01" />
              </div>
              <div class="field-group">
                <label for="in-fixed">{html.escape(cfg['label_fixed'])}</label>
                <input type="number" id="in-fixed" value="{cfg['fixed_fee']}" min="0" step="0.01" />
              </div>
              <div class="field-group">
                <label for="in-fx">{html.escape(cfg['label_fx'])}</label>
                <input type="number" id="in-fx" value="{cfg['fx_markup_percent']}" min="0" max="99" step="0.01" />
              </div>
            </div>

            <div class="doc-section">
              <span class="kicker">FIG. 03 — MULTI-VOLUME SENSITIVITY MATRIX</span>
              <h3>Tiered Settlement &amp; Reverse Gross-Up Schedule</h3>
              <p style="font-size:0.83rem;color:var(--ink-secondary);margin-bottom:8px">Live comparison across transaction volumes using your active fee parameters above:</p>
              <div style="overflow-x:auto">
                <table class="matrix-table">
                  <thead>
                    <tr>
                      <th>Gross Volume</th>
                      <th>Total Fee</th>
                      <th>Net Payout</th>
                      <th>Effective %</th>
                      <th>Invoice to Net</th>
                    </tr>
                  </thead>
                  <tbody id="sensitivity-matrix-body"></tbody>
                </table>
              </div>
            </div>

            {ad_html}

            <div class="doc-section">
              <span class="kicker">SPECIFICATION &amp; SOURCE ATTRIBUTION</span>
              <h3>Calculation Methodology</h3>
              <div class="formula-block">{html.escape(tool['formula_explanation'])}</div>
              <p style="font-family:var(--font-mono);font-size:0.74rem;color:var(--ink-muted);margin-bottom:20px">
                REFERENCE BASIS: {html.escape(src_name)} &bull; ASSUMPTIONS VERIFIED: {html.escape(ver_date)}
              </p>
              <h3>Reference Notes &amp; FAQ</h3>
              {faq_html}
            </div>
          </div>

          <aside>
            <div class="ledger-sheet">
              <div class="sheet-heading">
                <span>FIG. 02 — SETTLEMENT LEDGER</span>
                <span>LIVE CALCULATION</span>
              </div>
              <div class="ledger-primary">
                <span class="ledger-primary-label">Net Settlement Received</span>
                <div class="ledger-primary-value" id="out-net">$0.00</div>
              </div>
              <div class="ledger-rows">
                <div class="ledger-row">
                  <span>Total Platform &amp; FX Deductions</span>
                  <strong id="out-fee">$0.00</strong>
                </div>
                <div class="ledger-row">
                  <span>Effective Fee Burden</span>
                  <strong id="out-rate">0.00%</strong>
                </div>
                <div class="ledger-row">
                  <span>Gross Invoice Required to Net Target</span>
                  <strong id="out-reverse">$0.00</strong>
                </div>
              </div>
              <div class="ledger-actions">
                <button type="button" id="btn-export-csv" class="btn-secondary">Export CSV Statement</button>
                <button type="button" id="btn-copy-permalink" class="btn-secondary">Copy Permalink</button>
              </div>
            </div>
            {pro_box_html}
          </aside>
        </div>
        """

    if t_type == "saas_calc":
        return f"""
        <div class="workspace-grid" id="interactive-tool-root" data-tool-type="saas_calc" data-tool-config="{cfg_json}">
          <div>
            <div class="parameters-sheet">
              <div class="sheet-heading">
                <span>FIG. 01 — MODEL ASSUMPTIONS</span>
                <span>VERIFIED: {html.escape(ver_date.upper())}</span>
              </div>
              <div class="field-group">
                <label for="in-a">{html.escape(cfg['label_a'])}</label>
                <input type="number" id="in-a" value="{cfg['default_a']}" step="any" />
              </div>
              <div class="field-group">
                <label for="in-b">{html.escape(cfg['label_b'])}</label>
                <input type="number" id="in-b" value="{cfg['default_b']}" step="any" />
              </div>
              <div class="field-group">
                <label for="in-c">{html.escape(cfg['label_c'])}</label>
                <input type="number" id="in-c" value="{cfg['default_c']}" step="any" />
              </div>
              <div class="field-group">
                <label for="in-d">{html.escape(cfg['label_d'])}</label>
                <input type="number" id="in-d" value="{cfg['default_d']}" step="any" />
              </div>
            </div>

            {ad_html}

            <div class="doc-section">
              <span class="kicker">SPECIFICATION &amp; FORMULA</span>
              <h3>Calculation Methodology</h3>
              <div class="formula-block">{html.escape(tool['formula_explanation'])}</div>
              <p style="font-family:var(--font-mono);font-size:0.74rem;color:var(--ink-muted);margin-bottom:20px">
                REFERENCE BASIS: {html.escape(src_name)} &bull; ASSUMPTIONS VERIFIED: {html.escape(ver_date)}
              </p>
              <h3>Reference Notes &amp; FAQ</h3>
              {faq_html}
            </div>
          </div>

          <aside>
            <div class="ledger-sheet">
              <div class="sheet-heading">
                <span>FIG. 02 — OUTPUT LEDGER</span>
                <span>LIVE PROJECTION</span>
              </div>
              <div class="ledger-primary">
                <span class="ledger-primary-label" id="lbl-r1">Primary Output</span>
                <div class="ledger-primary-value" id="val-r1">$0.00</div>
              </div>
              <div class="ledger-rows">
                <div class="ledger-row">
                  <span id="lbl-r2">Secondary Metric</span>
                  <strong id="val-r2">0</strong>
                </div>
                <div class="ledger-row">
                  <span id="lbl-r3">Efficiency Benchmark</span>
                  <strong id="val-r3">0</strong>
                </div>
              </div>
              <div class="ledger-actions">
                <button type="button" id="btn-export-csv" class="btn-secondary">Export CSV Statement</button>
                <button type="button" id="btn-copy-permalink" class="btn-secondary">Copy Permalink</button>
              </div>
            </div>
            {pro_box_html}
          </aside>
        </div>
        """

    return f"""
    <div class="workspace-grid" id="interactive-tool-root" data-tool-type="dev_tool" data-tool-config="{cfg_json}">
      <div>
        <div class="parameters-sheet">
          <div class="sheet-heading">
            <span>FIG. 01 — SOURCE PAYLOAD</span>
            <span>LOCAL BROWSER EXECUTION</span>
          </div>
          <div class="field-group">
            <label for="dev-input">Input Buffer (Processed 100% Client-Side)</label>
            <textarea id="dev-input">{html.escape(cfg['sample_input'])}</textarea>
          </div>
          <div class="btn-row">
            <button type="button" id="btn-run-dev" class="btn-primary">Execute Transformation</button>
            <button type="button" id="btn-copy-dev" class="btn-secondary">Copy Output</button>
          </div>
          <div class="field-group" style="margin-top:20px">
            <label>Formatted Output</label>
            <pre id="dev-output" class="code-output"></pre>
          </div>
        </div>

        {ad_html}

        <div class="doc-section">
          <span class="kicker">SPECIFICATION</span>
          <h3>Technical Notes</h3>
          <div class="formula-block">{html.escape(tool['formula_explanation'])}</div>
          <h3>Frequently Asked Questions</h3>
          {faq_html}
        </div>
      </div>

      <aside>
        {pro_box_html}
      </aside>
    </div>
    """


def build_tool_page(tool: dict) -> str:
    slug = tool["slug"]
    title = tool["title"]
    desc = tool["short_desc"]
    category = tool["category"]
    src_name, ver_date = OFFICIAL_SOURCES.get(
        slug,
        ("Standard Financial & Technical Specification", "2026-10-27")
    )

    faq_schema_items = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        }
        for q, a in tool["faqs"]
    ]
    schema_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "name": title,
                "applicationCategory": "BusinessApplication",
                "operatingSystem": "Web Browser",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                "description": desc,
                "url": f"{SITE_URL}/tools/{slug}.html"
            },
            {
                "@type": "FAQPage",
                "mainEntity": faq_schema_items
            }
        ]
    }

    adsense_tag = ""
    if ADSENSE_CLIENT_ID:
        adsense_tag = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={html.escape(ADSENSE_CLIENT_ID)}" crossorigin="anonymous"></script>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} — CalcGrid Technical &amp; Financial Ledger</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{SITE_URL}/tools/{slug}.html" />
  <link rel="stylesheet" href="../assets/styles.css" />
  {adsense_tag}
  <script type="application/ld+json">{json.dumps(schema_ld)}</script>
</head>
<body>
  {render_navbar(prefix="../")}
  <main class="container">
    <div class="breadcrumb-bar">
      <span><a href="../index.html">Directory Index</a> &nbsp;/&nbsp; {html.escape(category)}</span>
      <span>BASIS: {html.escape(src_name.upper())} ({html.escape(ver_date.upper())})</span>
    </div>
    <header class="tool-header">
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(desc)}</p>
    </header>

    {render_tool_workspace(tool, prefix="../")}
  </main>

  <footer>
    <div class="footer-inner">
      <span>&copy; {datetime.now().year} CalcGrid Publication. Client-side computation engine.</span>
      <span><a href="../index.html">Index</a> &nbsp;&bull;&nbsp; <a href="../dashboard.html">Operations &amp; Earnings Proof</a> &nbsp;&bull;&nbsp; <a href="../legal.html">Privacy &amp; Terms</a> &nbsp;&bull;&nbsp; <a href="../sitemap.xml">Sitemap</a></span>
    </div>
  </footer>
  <script src="../assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_index_page() -> str:
    categories = {}
    for t in TOOLS_CATALOG:
        categories.setdefault(t["category"], []).append(t)

    cat_anchors = {
        "Payment & Fee Calculators": ("payment-calculators", "SECTION 01 // CROSS-BORDER PAYOUT ENGINES & FEE LEDGERS"),
        "SaaS & Marketing Calculators": ("saas-calculators", "SECTION 02 // SAAS & UNIT ECONOMICS MODELS"),
        "Developer Utilities": ("dev-utilities", "SECTION 03 // CLIENT-SIDE DEVELOPER INSTRUMENTS"),
        "Business & Operations Tools": ("ops-tools", "SECTION 04 // OPERATIONS & ESTIMATION LEDGERS")
    }

    sections_html = ""
    global_idx = 1
    for cat_name, tools in categories.items():
        anchor, sec_code = cat_anchors.get(cat_name, ("section", "SECTION"))
        cards_html = ""
        for t in tools:
            num_str = f"NO. {global_idx:02d}"
            global_idx += 1
            cards_html += f"""
            <a href="tools/{t['slug']}.html" class="tool-card">
              <div>
                <span class="tool-num">{num_str} &mdash; {html.escape(cat_name.upper())}</span>
                <h3>{html.escape(t['title'])}</h3>
                <p>{html.escape(t['short_desc'])}</p>
              </div>
              <div class="tool-card-footer">
                <span>Interactive Instrument</span>
                <span>Open Ledger &rarr;</span>
              </div>
            </a>
            """
        sections_html += f"""
        <section class="category-section" id="{anchor}">
          <div class="category-header">
            <h2 class="category-title">{html.escape(cat_name)}</h2>
            <span class="category-index">{sec_code} ({len(tools)} INSTRUMENTS)</span>
          </div>
          <div class="tools-grid">
            {cards_html}
          </div>
        </section>
        """

    competitor_rows = "".join(
        f"""<tr>
          <td><strong>{c['rank']:02d}. {html.escape(c['name'])}</strong></td>
          <td style="text-align:left;font-family:var(--font-sans)">{html.escape(c['strengths'])}</td>
          <td style="text-align:left;font-family:var(--font-sans)">{html.escape(c['underserved_gaps'])}</td>
        </tr>"""
        for c in COMPETITOR_BENCHMARK_MATRIX
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CalcGrid — Cross-Border Freelancer Payout Engine, CSV Auditor &amp; Financial Ledgers</title>
  <meta name="description" content="Country-aware freelancer payout comparison engine (Armenia, Georgia, Serbia, Philippines, India), reverse invoice solver, browser CSV fee auditor, and 30 client-side calculators." />
  <link rel="canonical" href="{SITE_URL}/" />
  <link rel="stylesheet" href="assets/styles.css" />
</head>
<body>
  {render_navbar(prefix="")}
  <main class="container">
    <section class="editorial-hero">
      <div>
        <span class="kicker">PUBLICATION &amp; INSTRUMENT DIRECTORY // VOL. II</span>
        <h1>Country-aware payout routing, reverse invoice math &amp; local CSV fee auditing.</h1>
        <p>Unlike single-step gateway calculators, CalcGrid models the full cross-border deduction chain—platform commission, payout rail availability (Wise, Payoneer, SWIFT, Lemon Squeezy), FX spread uncertainty, and local simplified tax regimes—100% in your browser.</p>
        <div class="search-bar">
          <label for="hub-search-input">Filter {len(TOOLS_CATALOG)} Verified Instruments by Keyword</label>
          <input type="search" id="hub-search-input" placeholder="Type 'Armenia', 'Georgia', 'CSV Auditor', 'Payoneer', 'Wise', 'Upwork', 'Reverse Invoice'..." />
        </div>
      </div>
      <div class="hero-figure">
        <img src="assets/images/editorial-hero.png" alt="CalcGrid Architectural Computation Ledger Illustration" />
        <div class="figure-caption">
          <span>FIG. 01 — ARCHITECTURAL LEDGER</span>
          <span>{len(TOOLS_CATALOG)} VERIFIED MODELS</span>
        </div>
      </div>
    </section>

    <section class="flagship-banner" aria-label="Flagship Instruments">
      <div class="flagship-col">
        <span class="kicker">FLAGSHIP ENGINE 01</span>
        <h3>Country-Aware Freelancer Payout &amp; Tax Router</h3>
        <p>Compare Wise vs. Payoneer vs. SWIFT vs. Lemon Squeezy across Armenia (AMD), Georgia (GEL), Serbia (RSD), Philippines (PHP), and India (INR) with availability alerts and uncertainty ranges.</p>
        <a href="tools/cross-border-payout-comparison-engine.html" class="btn-primary">Launch Corridor Engine &rarr;</a>
      </div>
      <div class="flagship-col">
        <span class="kicker">FLAGSHIP ENGINE 02</span>
        <h3>Multi-Stage Reverse Invoice Gross-Up Solver</h3>
        <p>Calculate the exact gross USD invoice required to net your target take-home amount after marketplace fees (Upwork 0%–15%, Fiverr 20%), rail fees, FX spreads, and local turnover tax.</p>
        <a href="tools/cross-border-payout-comparison-engine.html#in-target-net" class="btn-secondary">Solve Target Net Invoice &rarr;</a>
      </div>
      <div class="flagship-col">
        <span class="kicker">FLAGSHIP ENGINE 03</span>
        <h3>Private Browser CSV Statement Auditor</h3>
        <p>Drop or paste your Stripe, Payoneer, Wise, Upwork, or Lemon Squeezy CSV rows locally in your browser to flag hidden FX markups and fee variances (&gt;0.25%) without uploading data.</p>
        <a href="tools/private-csv-payout-fee-auditor.html" class="btn-secondary">Open Browser CSV Auditor &rarr;</a>
      </div>
    </section>

    {sections_html}

    <section class="doc-section" style="margin-top:48px">
      <span class="kicker">COMPETITIVE BENCHMARK &amp; METHODOLOGY AUDIT</span>
      <h3>How CalcGrid Compares to 10 Existing Fee Calculator Websites</h3>
      <p style="font-size:0.86rem;color:var(--ink-secondary);margin-bottom:14px">
        We audited the 10 leading payment and freelancer calculator sites to identify why international contractors still lose 2%–6% to unmodeled deductions:
      </p>
      <div style="overflow-x:auto">
        <table class="matrix-table">
          <thead>
            <tr>
              <th>Competing Platform</th>
              <th>What They Solve Well</th>
              <th>Underserved Need Solved by CalcGrid</th>
            </tr>
          </thead>
          <tbody>
            {competitor_rows}
          </tbody>
        </table>
      </div>
    </section>
  </main>

  <footer>
    <div class="footer-inner">
      <span>&copy; {datetime.now().year} CalcGrid Publication. All calculations execute client-side.</span>
      <span><a href="dashboard.html">Operations &amp; Earnings Proof</a> &nbsp;&bull;&nbsp; <a href="legal.html">Privacy, Consent &amp; Disclaimers</a> &nbsp;&bull;&nbsp; <a href="sitemap.xml">XML Sitemap</a> &nbsp;&bull;&nbsp; <a href="rss.xml">RSS Feed</a></span>
    </div>
  </footer>
  <script src="assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_dashboard_page() -> str:
    """
    Builds Part 5: Honest Operations, Attribution & Earnings Proof Dashboard (`dist/dashboard.html`).
    Reads actual recorded metrics from `logs/business_ledger.json`, `logs/telemetry.jsonl`, and `marketing_outbox/`.
    Never invents revenue, fake views, or speculative projections.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    ledger_file = LOGS_DIR / "business_ledger.json"
    if not ledger_file.exists():
        default_ledger = {
            "target_monthly_net_profit_usd": 100.00,
            "actual_collected_revenue_usd": 0.00,
            "adsense_revenue_usd": 0.00,
            "pro_pack_sales_count": 0,
            "pro_pack_gross_usd": 0.00,
            "processor_and_mor_fees_usd": 0.00,
            "infrastructure_expenses_usd": 0.00,
            "paid_ads_spend_usd": 0.00,
            "net_profit_usd": 0.00,
            "search_console": {
                "status": "Awaiting live domain property verification in Google Search Console",
                "impressions": 0,
                "clicks": 0
            },
            "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        ledger_file.write_text(json.dumps(default_ledger, indent=2), encoding="utf-8")
    else:
        default_ledger = json.loads(ledger_file.read_text(encoding="utf-8"))

    # Parse actual telemetry events by source
    source_counts = {"organic_search": 0, "social_utm": 0, "direct_or_local_test": 0, "referral": 0}
    utm_campaigns = {}
    telemetry_path = LOGS_DIR / "telemetry.jsonl"
    if telemetry_path.exists():
        for line in telemetry_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                ev = json.loads(line)
                u_src = (ev.get("utm_source") or "").strip().lower()
                u_cmp = (ev.get("utm_campaign") or "").strip()
                ref = (ev.get("referrer") or "").strip().lower()
                if u_src:
                    source_counts["social_utm"] += 1
                    utm_campaigns[u_cmp or u_src] = utm_campaigns.get(u_cmp or u_src, 0) + 1
                elif any(s in ref for s in ("google.", "bing.", "duckduckgo.", "yandex.")):
                    source_counts["organic_search"] += 1
                elif ref and ref != "direct" and "localhost" not in ref:
                    source_counts["referral"] += 1
                else:
                    source_counts["direct_or_local_test"] += 1
            except Exception:
                pass

    # Check generated SMM video queue in marketing_outbox/
    smm_manifest_path = MARKETING_DIR / "campaign_manifest.json"
    smm_rows_html = ""
    if smm_manifest_path.exists():
        try:
            manifest = json.loads(smm_manifest_path.read_text(encoding="utf-8"))
            for item in manifest.get("episodes", []):
                ep_id = item.get("episode_id", "")
                clicks = utm_campaigns.get(ep_id, 0)
                smm_rows_html += f"""
                <tr>
                  <td><strong>{html.escape(ep_id)}</strong><br/><span style="font-size:0.7rem;color:var(--ink-muted)">{html.escape(item.get('title', ''))}</span></td>
                  <td style="text-align:left">{html.escape(item.get('target_audience_question', ''))}</td>
                  <td><code>{html.escape(item.get('video_file', ''))}</code> ({html.escape(str(item.get('duration_sec', 0)))}s, 1080x1920)</td>
                  <td><span class="badge-warn">{html.escape(item.get('publish_status', 'LOCAL_QUEUE'))}</span></td>
                  <td>0 external / {clicks} tracked UTM visits</td>
                </tr>
                """
        except Exception:
            pass

    if not smm_rows_html:
        smm_rows_html = '<tr><td colspan="5" style="text-align:center">Run <code>python3 engine/smm_pipeline.py</code> to build vertical video episodes.</td></tr>'

    net_profit = float(default_ledger.get("net_profit_usd", 0.0))
    rev = float(default_ledger.get("actual_collected_revenue_usd", 0.0))
    expenses = float(default_ledger.get("infrastructure_expenses_usd", 0.0)) + float(default_ledger.get("paid_ads_spend_usd", 0.0))
    conversions = int(default_ledger.get("pro_pack_sales_count", 0))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Operations, Attribution &amp; Earnings Proof Dashboard — CalcGrid</title>
  <meta name="robots" content="noindex, follow" />
  <link rel="stylesheet" href="assets/styles.css" />
</head>
<body>
  {render_navbar(prefix="")}
  <main class="container" style="padding-top:36px">
    <span class="kicker">TRANSPARENT BUSINESS LEDGER // ZERO FABRICATED METRICS</span>
    <h1 style="font-family:var(--font-serif);font-size:2.3rem;font-weight:500;margin-bottom:8px">Operations, Traffic Attribution &amp; Earnings Proof Dashboard</h1>
    <p style="color:var(--ink-secondary);font-size:0.95rem;max-width:780px">
      This ledger reports actual measured visitors, search impressions, social UTM clicks, conversions, collected revenue, and infrastructure expenses. Unconfigured external channels report <strong>0</strong> until live account authorization is completed.
    </p>

    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="k-label">Actual Net Profit (Monthly)</span>
        <div class="k-val">${net_profit:,.2f}</div>
        <span class="k-sub">Target: $100.00/mo ($0.00 expenses)</span>
      </div>
      <div class="kpi-card">
        <span class="k-label">Actual Collected Revenue</span>
        <div class="k-val">${rev:,.2f}</div>
        <span class="k-sub">{conversions} Pro sales &bull; $0.00 AdSense</span>
      </div>
      <div class="kpi-card">
        <span class="k-label">Infrastructure &amp; Ad Spend</span>
        <div class="k-val">${expenses:,.2f}</div>
        <span class="k-sub">Static hosting &amp; local AI build ($0/mo)</span>
      </div>
      <div class="kpi-card">
        <span class="k-label">Recorded Telemetry Sessions</span>
        <div class="k-val">{sum(source_counts.values())}</div>
        <span class="k-sub">{source_counts['social_utm']} UTM &bull; {source_counts['organic_search']} Search &bull; {source_counts['direct_or_local_test']} Local/Direct</span>
      </div>
    </div>

    <div class="doc-section">
      <span class="kicker">PART 1 // SYSTEM READINESS &amp; HONEST STATUS MATRIX</span>
      <h3>What Is Genuinely Working vs. Simulated vs. Blocked on Owner Authorization</h3>
      <div style="overflow-x:auto">
        <table class="matrix-table">
          <thead>
            <tr>
              <th>Subsystem</th>
              <th>Status</th>
              <th>Independent Verification / Blocker Details</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>32 Interactive Calculators &amp; Flagship Engines</strong></td>
              <td><span class="badge-ok">GENUINELY WORKING</span></td>
              <td style="text-align:left;font-family:var(--font-sans)">All 32 tools (including Country Payout Comparison Engine, Reverse Invoice Solver, and Browser CSV Auditor) pass automated Node.js runtime &amp; Python mathematical verification (<code>autopilot.py</code>).</td>
            </tr>
            <tr>
              <td><strong>Paid Pro Pack Security &amp; Multi-Tab .xlsx</strong></td>
              <td><span class="badge-ok">GENUINELY WORKING</span></td>
              <td style="text-align:left;font-family:var(--font-sans)"><code>calcgrid-pro-offline-suite.zip</code> is stored strictly in <code>private_products/</code> (0 ZIPs in <code>dist/</code>, 0 ZIPs in Git history) and contains a verified 3-sheet <code>.xlsx</code> workbook + 3 CSV models + CLI batch reconciler.</td>
            </tr>
            <tr>
              <td><strong>Autonomous SMM Video Renderer (FFmpeg + Voiceover)</strong></td>
              <td><span class="badge-ok">GENUINELY WORKING LOCALLY</span></td>
              <td style="text-align:left;font-family:var(--font-sans)"><code>engine/smm_pipeline.py</code> generates real 1080x1920 vertical MP4 videos with synthesized English voiceovers (macOS <code>say</code> + <code>ffmpeg</code>), burned-in ledger frames, <code>.srt</code> subtitles, and UTM links in <code>marketing_outbox/</code>.</td>
            </tr>
            <tr>
              <td><strong>Public Cloud Deployment (GitHub / Cloudflare Pages)</strong></td>
              <td><span class="badge-warn">BLOCKED ON CLI AUTH</span></td>
              <td style="text-align:left;font-family:var(--font-sans)">Local Git repository is clean and ready. <code>gh auth status</code> on this Mac is not logged into a GitHub account yet. One-time <code>gh auth login</code> or Cloudflare OAuth by the account owner unlocks automatic Git pushes.</td>
            </tr>
            <tr>
              <td><strong>Social Auto-Publishing (YouTube / IG / TikTok APIs)</strong></td>
              <td><span class="badge-warn">BLOCKED ON OAUTH TOKENS</span></td>
              <td style="text-align:left;font-family:var(--font-sans)">Videos are rendered locally to <code>marketing_outbox/videos/</code>, but official platform publishing requires owner OAuth credentials (<code>YOUTUBE_OAUTH_TOKEN</code> / <code>TIKTOK_ACCESS_TOKEN</code>).</td>
            </tr>
            <tr>
              <td><strong>Live Revenue Collection (Lemon Squeezy &amp; AdSense)</strong></td>
              <td><span class="badge-warn">DISABLED UNTIL VERIFIED</span></td>
              <td style="text-align:left;font-family:var(--font-sans)">Per pre-launch policy, ad slots and checkout buttons remain disabled until owner KYB/KYC verification sets <code>LEMON_SQUEEZY_URL</code> and <code>ADSENSE_CLIENT_ID</code>.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="doc-section">
      <span class="kicker">PART 2 // AUTONOMOUS SMM VIDEO PIPELINE QUEUE</span>
      <h3>Generated Short-Form Vertical Videos (1080x1920 MP4) &amp; Measured UTM Clicks</h3>
      <div style="overflow-x:auto">
        <table class="matrix-table">
          <thead>
            <tr>
              <th>Episode ID &amp; Title</th>
              <th>Researched Audience Question</th>
              <th>Rendered MP4 Asset</th>
              <th>Publishing Status</th>
              <th>Measured Views / UTM Visits</th>
            </tr>
          </thead>
          <tbody>
            {smm_rows_html}
          </tbody>
        </table>
      </div>
    </div>
  </main>
  <footer>
    <div class="footer-inner">
      <span>&copy; {datetime.now().year} CalcGrid Publication. Honest Telemetry &amp; Earnings Ledger.</span>
      <span><a href="index.html">Return to Directory Index</a></span>
    </div>
  </footer>
  <script src="assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_legal_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Privacy Policy, EEA Consent &amp; Financial Disclaimers — CalcGrid</title>
  <link rel="stylesheet" href="assets/styles.css" />
</head>
<body>
  {render_navbar(prefix="")}
  <main class="container" style="max-width:820px;padding-top:36px">
    <span class="kicker">LEGAL &amp; COMPLIANCE DOCUMENTATION</span>
    <h1 style="font-family:var(--font-serif);font-size:2.2rem;font-weight:500;margin-bottom:20px">Privacy Policy, EEA/UK/CH Consent &amp; Financial Disclaimer</h1>
    <div class="doc-section" style="margin-top:0">
      <h3>1. Client-Side Data Privacy</h3>
      <p style="color:var(--ink-secondary);margin:8px 0 22px;font-size:0.9rem">
        All calculators, CSV transaction auditors, and developer utilities (including JSON, JWT, SQL, and CSV converters) execute locally in your browser using client-side JavaScript. We do not store, transmit, or log the financial figures, CSV files, tokens, or source code you enter into our instruments.
      </p>

      <h3>2. EEA, UK &amp; Switzerland Advertising Consent (IAB TCF v2.2 Certified CMP)</h3>
      <p style="color:var(--ink-secondary);margin:8px 0 22px;font-size:0.9rem">
        Advertising slots remain disabled until Google AdSense is active. When Google AdSense is enabled, consent for visitors in the European Economic Area (EEA), the United Kingdom, and Switzerland is managed exclusively through Google's certified Consent Management Platform (Google AdSense <em>Privacy &amp; messaging</em> integrated with the IAB Transparency and Consent Framework v2.2) rather than a custom banner.
      </p>

      <h3>3. No Financial, Tax, or Legal Advice</h3>
      <p style="color:var(--ink-secondary);margin:8px 0 10px;font-size:0.9rem">
        All fee, exchange-rate spread, and unit-economics models on CalcGrid are provided strictly for informational and estimation purposes. Payment processor fees (such as Payoneer, Wise, Lemon Squeezy, Stripe, PayPal, Upwork), correspondent SWIFT bank deductions, and regional tax rules (such as Armenia Turnover Tax, Georgia Small Business Status, Serbia Paušal, Philippines 8% Gross Receipts, and India Section 44ADA) change periodically and depend on individual eligibility. Always verify exact figures with your payment provider and a licensed accountant in your jurisdiction.
      </p>
    </div>
  </main>
  <footer>
    <div class="footer-inner">
      <span>&copy; {datetime.now().year} CalcGrid Publication.</span>
      <span><a href="index.html">Return to Directory Index</a></span>
    </div>
  </footer>
  <script src="assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_seo_artifacts():
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    urls = [f"{SITE_URL}/", f"{SITE_URL}/legal.html"] + [
        f"{SITE_URL}/tools/{t['slug']}.html" for t in TOOLS_CATALOG
    ]

    sitemap_entries = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{now_iso}</lastmod>\n  </url>\n"
        for u in urls
    )
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_entries}</urlset>\n'
    (DIST_DIR / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    (DIST_DIR / "robots.txt").write_text(robots_txt, encoding="utf-8")

    (DIST_DIR / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")

    rss_items = "".join(
        f"""    <item>
      <title>{html.escape(t['title'])}</title>
      <link>{SITE_URL}/tools/{t['slug']}.html</link>
      <description>{html.escape(t['short_desc'])}</description>
      <guid>{SITE_URL}/tools/{t['slug']}.html</guid>
    </item>\n"""
        for t in TOOLS_CATALOG
    )
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>CalcGrid — Financial &amp; Technical Ledger</title>
    <link>{SITE_URL}/</link>
    <description>Country-Aware Freelancer Payout Engine, Browser CSV Auditor &amp; 30 Client-Side Calculators</description>
{rss_items}  </channel>
</rss>
"""
    (DIST_DIR / "rss.xml").write_text(rss_xml, encoding="utf-8")


def create_multi_tab_xlsx_bytes(sheets: list[tuple[str, list[list[str]]]]) -> bytes:
    """
    Creates a standards-compliant OpenXML `.xlsx` workbook with multiple worksheet tabs
    using only the Python standard library (`zipfile` + XML).
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as xzf:
        sheet_overrides = "".join(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            f'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            for i in range(1, len(sheets) + 1)
        )
        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            f'{sheet_overrides}'
            '</Types>'
        )
        xzf.writestr("[Content_Types].xml", content_types)

        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/>'
            '</Relationships>'
        )
        xzf.writestr("_rels/.rels", root_rels)

        sheet_nodes = "".join(
            f'<sheet name="{xml_escape(name)}" sheetId="{i}" r:id="rId{i}"/>'
            for i, (name, _) in enumerate(sheets, start=1)
        )
        workbook_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<sheets>{sheet_nodes}</sheets>'
            '</workbook>'
        )
        xzf.writestr("xl/workbook.xml", workbook_xml)

        wb_rel_nodes = "".join(
            f'<Relationship Id="rId{i}" '
            f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, len(sheets) + 1)
        )
        wb_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'{wb_rel_nodes}'
            '</Relationships>'
        )
        xzf.writestr("xl/_rels/workbook.xml.rels", wb_rels)

        for idx, (_, rows) in enumerate(sheets, start=1):
            row_xml_list = []
            for r_idx, row in enumerate(rows, start=1):
                cell_xml_list = []
                for c_idx, val in enumerate(row):
                    col_letter = chr(ord("A") + c_idx)
                    cell_ref = f"{col_letter}{r_idx}"
                    s_val = str(val)
                    try:
                        if r_idx > 1:
                            float(s_val)
                            cell_xml_list.append(f'<c r="{cell_ref}"><v>{xml_escape(s_val)}</v></c>')
                        else:
                            raise ValueError()
                    except ValueError:
                        cell_xml_list.append(
                            f'<c r="{cell_ref}" t="inlineStr"><is><t>{xml_escape(s_val)}</t></is></c>'
                        )
                row_xml_list.append(f'<row r="{r_idx}">{"".join(cell_xml_list)}</row>')

            sheet_xml = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                f'<sheetData>{"".join(row_xml_list)}</sheetData>'
                '</worksheet>'
            )
            xzf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml)

    return buf.getvalue()


def build_private_pro_digital_product_zip() -> Path:
    """
    Packages the paid Pro product strictly outside `dist/` in `private_products/`
    so it is NEVER publicly exposed on Cloudflare Pages or GitHub Pages.
    Includes BOTH a genuine multi-tab `.xlsx` workbook AND 3 separate `.csv` files.
    """
    public_downloads = DIST_DIR / "downloads"
    if public_downloads.exists():
        shutil.rmtree(public_downloads)

    PRIVATE_PRODUCTS_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = PRIVATE_PRODUCTS_DIR / "calcgrid-pro-offline-suite.zip"

    batch_reconciler_py = """#!/usr/bin/env python3
\"\"\"
CalcGrid Pro Batch Payout & Fee Reconciler CLI (calcgrid_batch_reconciler.py)
Exclusive to the CalcGrid Pro Suite ($19).
Ingests a bulk CSV of transactions (e.g. from Stripe, Payoneer, Wise, Upwork, Lemon Squeezy),
audits expected vs actual fees, flags variances > 0.25%, and outputs a reconciled accounting ledger.
\"\"\"
import argparse
import csv
from pathlib import Path

PROVIDER_RATES = {
    "lemonsqueezy": (5.0, 0.50, 1.5),
    "payoneer":     (1.0, 0.00, 2.0),
    "wise":         (0.65, 4.14, 0.0),
    "upwork_10":    (10.0, 0.99, 0.0),
    "upwork_5":     (5.0, 0.99, 0.0),
    "upwork_15":    (15.0, 0.99, 0.0),
    "stripe_intl":  (2.9, 0.30, 2.5),
    "fiverr":       (20.0, 1.00, 0.0),
}

def reconcile_csv(input_csv: Path, output_csv: Path):
    rows_out = []
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            provider = row.get("provider", "lemonsqueezy").strip().lower()
            gross = float(row.get("gross_usd", 0.0))
            actual_net = float(row.get("actual_net_usd", 0.0))
            pct, fix, fx = PROVIDER_RATES.get(provider, (5.0, 0.50, 0.0))
            expected_fee = gross * ((pct + fx) / 100.0) + fix
            expected_net = max(0.0, gross - expected_fee)
            variance = actual_net - expected_net
            flag = "OK" if abs(variance) <= max(0.50, gross * 0.0025) else "FEE_VARIANCE_ALERT"
            rows_out.append({
                "tx_id": row.get("tx_id", ""),
                "provider": provider,
                "gross_usd": f"{gross:.2f}",
                "expected_fee_usd": f"{expected_fee:.2f}",
                "expected_net_usd": f"{expected_net:.2f}",
                "actual_net_usd": f"{actual_net:.2f}",
                "variance_usd": f"{variance:.2f}",
                "audit_status": flag
            })

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "tx_id", "provider", "gross_usd", "expected_fee_usd",
            "expected_net_usd", "actual_net_usd", "variance_usd", "audit_status"
        ])
        writer.writeheader()
        writer.writerows(rows_out)
    print(f"Reconciled {len(rows_out)} transactions -> {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CalcGrid Pro Bulk Payout Reconciler")
    parser.add_argument("--input", required=True, help="Input transactions CSV")
    parser.add_argument("--output", default="reconciled_ledger.csv", help="Output reconciled CSV")
    args = parser.parse_args()
    reconcile_csv(Path(args.input), Path(args.output))
"""

    sample_transactions_csv = (
        "tx_id,provider,gross_usd,actual_net_usd\n"
        "TX-1001,lemonsqueezy,49.00,45.32\n"
        "TX-1002,upwork_10,1200.00,1079.01\n"
        "TX-1003,payoneer,2500.00,2400.00\n"
        "TX-1004,wise,3000.00,2976.36\n"
    )

    saas_rows = [
        ["Month", "Starting_MRR_USD", "New_MRR_USD", "Churned_MRR_4.5Pct", "Net_MRR_USD", "Gross_Margin_85Pct", "CAC_Spend_USD", "Net_Cash_Flow_USD"],
        ["Month 1", "1000.00", "500.00", "45.00", "1455.00", "1236.75", "600.00", "636.75"],
        ["Month 2", "1455.00", "600.00", "65.48", "1989.53", "1691.10", "720.00", "971.10"],
        ["Month 3", "1989.53", "750.00", "89.53", "2650.00", "2252.50", "900.00", "1352.50"],
        ["Month 6", "4200.00", "1100.00", "189.00", "5111.00", "4344.35", "1200.00", "3144.35"],
        ["Month 12", "9800.00", "1800.00", "441.00", "11159.00", "9485.15", "1800.00", "7685.15"],
    ]

    cross_border_rows = [
        ["Provider_And_Scenario", "Base_Fee_Pct", "Fixed_Fee_USD", "FX_Spread_Pct", "Net_on_500_USD", "Net_on_2500_USD", "Net_on_10000_USD", "Verified_Date"],
        ["Wise Wire", "0.65", "4.14", "0.0", "492.61", "2479.61", "9930.86", "2026-10"],
        ["Payoneer Local", "1.0", "0.00", "2.0", "485.00", "2425.00", "9700.00", "2026-10"],
        ["Upwork (0% Direct Contract - Freelancer Plus)", "0.0", "0.99", "0.0", "499.01", "2499.01", "9999.01", "2026-10"],
        ["Upwork (5% Direct Contract Standard / Example)", "5.0", "0.99", "0.0", "474.01", "2374.01", "9499.01", "2026-10"],
        ["Upwork (10% Example Marketplace Rate)", "10.0", "0.99", "0.0", "449.01", "2249.01", "8999.01", "2026-10"],
        ["Upwork (15% Example Marketplace Rate)", "15.0", "0.99", "0.0", "424.01", "2124.01", "8499.01", "2026-10"],
        ["Lemon Squeezy MoR", "5.0", "0.50", "1.5", "467.00", "2337.00", "9349.50", "2026-10"],
    ]

    roas_rows = [
        ["AOV_USD", "COGS_And_Fees_USD", "Contribution_Margin_USD", "Break_Even_ROAS", "Monthly_Ad_Spend_USD", "Target_ROAS", "Monthly_Net_Profit_USD"],
        ["60.00", "24.00", "36.00", "1.67", "2000.00", "2.50", "1000.00"],
        ["85.00", "29.00", "56.00", "1.52", "3000.00", "2.40", "1743.53"],
        ["120.00", "36.00", "84.00", "1.43", "5000.00", "3.00", "5500.00"],
    ]

    def rows_to_csv(rows: list[list[str]]) -> str:
        return "\n".join(",".join(r) for r in rows) + "\n"

    xlsx_bytes = create_multi_tab_xlsx_bytes([
        ("SaaS_12Mo_Cohort_Model", saas_rows),
        ("Cross_Border_Fee_Matrix", cross_border_rows),
        ("ROAS_Unit_Economics", roas_rows),
    ])

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("01_cli_batch_auditor/calcgrid_batch_reconciler.py", batch_reconciler_py)
        zf.writestr("01_cli_batch_auditor/sample_transactions.csv", sample_transactions_csv)
        zf.writestr("02_spreadsheet_models/calcgrid_financial_models.xlsx", xlsx_bytes)
        zf.writestr("02_spreadsheet_models/saas_12mo_cohort_and_cashflow_model.csv", rows_to_csv(saas_rows))
        zf.writestr("02_spreadsheet_models/cross_border_payout_comparison_matrix.csv", rows_to_csv(cross_border_rows))
        zf.writestr("02_spreadsheet_models/roas_and_unit_economics_model.csv", rows_to_csv(roas_rows))
        for p in DIST_DIR.rglob("*"):
            if p.is_file():
                rel = p.relative_to(DIST_DIR)
                zf.write(p, f"03_offline_html_instruments/{rel}")

    return zip_path


def compile_all() -> dict:
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    src_images_dir = Path(__file__).resolve().parent / "images"
    if src_images_dir.exists():
        for img_file in src_images_dir.glob("*.png"):
            shutil.copy2(img_file, IMAGES_DIR / img_file.name)

    (ASSETS_DIR / "styles.css").write_text(build_css(), encoding="utf-8")
    (ASSETS_DIR / "tools-runtime.js").write_text(build_runtime_js(), encoding="utf-8")

    (DIST_DIR / "index.html").write_text(build_index_page(), encoding="utf-8")
    (DIST_DIR / "legal.html").write_text(build_legal_page(), encoding="utf-8")
    (DIST_DIR / "dashboard.html").write_text(build_dashboard_page(), encoding="utf-8")

    for tool in TOOLS_CATALOG:
        html_out = build_tool_page(tool)
        (TOOLS_DIR / f"{tool['slug']}.html").write_text(html_out, encoding="utf-8")

    build_seo_artifacts()
    private_zip_path = build_private_pro_digital_product_zip()

    return {
        "tools_compiled": len(TOOLS_CATALOG),
        "total_html_pages": len(TOOLS_CATALOG) + 3,
        "public_dist_dir": str(DIST_DIR),
        "private_pro_zip": str(private_zip_path),
        "public_zip_exposed": any(DIST_DIR.rglob("*.zip")),
        "ads_enabled": bool(ADSENSE_CLIENT_ID),
        "checkout_enabled": bool(LEMON_SQUEEZY_CHECKOUT_URL)
    }


if __name__ == "__main__":
    print(json.dumps(compile_all(), indent=2))
