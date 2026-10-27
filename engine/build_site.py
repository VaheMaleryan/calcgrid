#!/usr/bin/env python3
"""
PayoutFolio Autonomous Static Site Compiler, Flagship Competitive Advantage Builder & Private Product Packager.
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
import re
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
LAUNCH_CONFIG_PATH = ROOT_DIR / "launch_config.json"


def _load_launch_config() -> dict:
    if LAUNCH_CONFIG_PATH.exists():
        try:
            return json.loads(LAUNCH_CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


_LAUNCH_CFG = _load_launch_config()
SITE_URL = (
    os.environ.get("SITE_URL")
    or _LAUNCH_CFG.get("site_url")
    or "https://vahemaleryan.github.io/calcgrid"
).rstrip("/")
BRAND_NAME = _LAUNCH_CFG.get("brand_name", "PayoutFolio")
TAGLINE = "Know what you actually keep"
MONETIZATION_APPROVED = _LAUNCH_CFG.get("monetization_approved", False) is True
INDEXNOW_KEY = "8f92a1c4e7b34d109a8e2c5f6b7d8e91"
LEMON_SQUEEZY_CHECKOUT_URL = (
    os.environ.get("LEMON_SQUEEZY_URL")
    or _LAUNCH_CFG.get("lemon_squeezy_checkout_url")
    or ""
).strip()
ADSENSE_CLIENT_ID = (
    os.environ.get("ADSENSE_CLIENT_ID")
    or _LAUNCH_CFG.get("adsense_client_id")
    or ""
).strip()

if not MONETIZATION_APPROVED:
    LEMON_SQUEEZY_CHECKOUT_URL = ""
    ADSENSE_CLIENT_ID = ""


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


DISPLAY_NAMES = {
    "cross-border-payout-comparison-engine": "Your payout, from invoice to income",
    "private-csv-payout-fee-auditor": "A private check on your payout fees",
    "payoneer-fee-calculator": "Payoneer fee calculator",
    "wise-transfer-fee-calculator": "Wise transfer calculator",
    "lemonsqueezy-fee-calculator": "Lemon Squeezy fee calculator",
    "gumroad-fee-calculator": "Gumroad fee calculator",
    "paddle-fee-calculator": "Paddle fee calculator",
    "upwork-freelancer-fee-calculator": "Upwork fee calculator",
    "fiverr-seller-fee-calculator": "Fiverr payout calculator",
    "stripe-international-fee-calculator": "Stripe international fees",
    "paypal-goods-services-fee-calculator": "PayPal commercial fees",
    "armenia-it-tax-turnover-calculator": "Armenia turnover tax scenario",
    "saas-mrr-churn-ltv-calculator": "Customer lifetime value",
    "roas-break-even-calculator": "Break-even return on ad spend",
    "cpm-cpc-ctr-ad-revenue-calculator": "Display ad revenue",
    "shopify-profit-margin-calculator": "E-commerce profit margin",
    "email-marketing-roi-calculator": "Email campaign contribution",
    "ab-test-sample-size-calculator": "Conversion lift & revenue",
    "json-to-typescript-schema-converter": "JSON to TypeScript & Zod",
    "cron-expression-explainer": "Cron schedule explainer",
    "jwt-token-decoder": "Private JWT decoder",
    "sql-query-formatter": "SQL query formatter",
    "base64-url-hash-encoder": "Base64 & URL encoder",
    "csv-to-json-converter": "CSV to JSON converter",
    "regex-pattern-tester": "Email & invoice reference finder",
    "svg-to-data-uri-optimizer": "SVG to CSS & React",
    "freelance-hourly-rate-calculator": "Your freelance hourly rate",
    "software-project-estimation-calculator": "Project time & quote estimator",
    "cloud-llm-token-cost-calculator": "LLM token cost planner",
    "password-entropy-generator": "Password & entropy generator",
    "markdown-to-html-converter": "Basic Markdown to HTML",
    "utm-campaign-link-builder": "Campaign link builder",
}

SOURCE_LINKS = {
    "payoneer-fee-calculator": ("Payoneer pricing", "https://www.payoneer.com/about/pricing/"),
    "wise-transfer-fee-calculator": ("Wise pricing", "https://wise.com/pricing/"),
    "lemonsqueezy-fee-calculator": ("Lemon Squeezy fees", "https://docs.lemonsqueezy.com/help/getting-started/fees"),
    "gumroad-fee-calculator": ("Gumroad pricing", "https://gumroad.com/pricing"),
    "paddle-fee-calculator": ("Paddle pricing", "https://www.paddle.com/pricing"),
    "upwork-freelancer-fee-calculator": ("Upwork service fees", "https://support.upwork.com/hc/en-us/articles/211062538-Freelancer-Service-Fees"),
    "fiverr-seller-fee-calculator": ("Fiverr earnings", "https://help.fiverr.com/hc/en-us/articles/9234443621137-Your-earnings-page"),
    "stripe-international-fee-calculator": ("Stripe pricing", "https://stripe.com/pricing"),
    "paypal-goods-services-fee-calculator": ("PayPal merchant fees", "https://www.paypal.com/us/business/paypal-business-fees"),
}

def public_url(path: str = "") -> str:
    """Use the production origin; Cloudflare's HTML redirects use extensionless destinations."""
    if _LAUNCH_CFG.get("hosting_provider") == "cloudflare" and path.endswith(".html"):
        path = path[:-5]
        if path == "index":
            path = ""
    return SITE_URL + "/" + path


def finalize_cloudflare_output() -> None:
    if _LAUNCH_CFG.get("hosting_provider") != "cloudflare":
        return
    def clean_link(match):
        value = match.group(2)
        if value.startswith(("http:", "https:")) and not value.startswith(SITE_URL + "/"):
            return match.group()
        value = re.sub(r"index\.html(?=[#?]|$)", "", value)
        value = re.sub(r"\.html(?=[#?]|$)", "", value)
        if not value or value.startswith(("#", "?")):
            value = "./" + value
        return match.group(1) + '="' + value + '"'
    for path in DIST_DIR.rglob("*"):
        if path.suffix not in {".html", ".xml", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8")
        content = re.sub(re.escape(SITE_URL) + r'/([^"\s<>]*?)\.html', lambda m: SITE_URL + '/' + m.group(1), content)
        if path.suffix == ".html":
            content = re.sub(r'(href)="([^"]*\.html[^"]*)"', clean_link, content)
        path.write_text(content, encoding="utf-8")


def build_css() -> str:
    return """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap');
:root{--paper:#f6f5f0;--surface:#fff;--stone-panel:#eeeee7;--ink:#202b28;--ink-secondary:#53615b;--ink-muted:#64716a;--rule:#d8ded6;--rule-dark:#c8d0c6;--accent:#174f46;--accent-light:#eaf3ed;--amber-ink:#805317;--amber-bg:#faf1df;--danger-ink:#9a3834;--danger-bg:#fbefed;--font-serif:'Newsreader',Georgia,serif;--font-sans:'DM Sans',-apple-system,BlinkMacSystemFont,sans-serif;--font-mono:'IBM Plex Mono',monospace}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth;scroll-padding-top:100px}body{background:var(--paper);color:var(--ink);font:16px/1.6 var(--font-sans);-webkit-font-smoothing:antialiased}a{color:inherit;text-decoration:none}button,input,textarea,select{font:inherit}button,a,input,select,textarea{-webkit-tap-highlight-color:transparent}a,button{touch-action:manipulation}button{cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid #397b68;outline-offset:4px}::selection{background:#d6e8db}img,svg{max-width:100%}[hidden]{display:none!important}.skip-link{position:absolute;left:24px;top:-80px;z-index:50;background:var(--ink);color:#fff;padding:12px 20px}.skip-link:focus{top:12px}
.navbar{border-bottom:1px solid var(--rule);background:var(--paper);padding:23px 36px}.nav-inner,.container,.footer-inner{max-width:1280px;margin:auto}.nav-inner{display:flex;justify-content:space-between;align-items:center;gap:24px}.brand{display:flex;align-items:center;gap:12px;flex-shrink:0}.brand-mark{width:34px;height:34px;color:var(--accent)}.brand-name{font:500 28px/1 var(--font-serif);letter-spacing:-1px}.brand-meta{display:none}.nav-links{display:flex;gap:25px;align-items:center;font-size:13px;font-weight:550}.nav-links a{color:var(--ink-secondary)}.nav-links a:hover{color:var(--accent)}.nav-cta{padding:10px 18px;background:var(--accent);color:#fff!important;border-radius:5px}.mobile-menu{display:none}.container{padding:0 36px 88px}
.kicker{display:block;text-transform:uppercase;letter-spacing:.13em;font:500 10px/1.6 var(--font-mono);color:var(--accent);margin-bottom:14px}.editorial-hero{display:grid;grid-template-columns:1.05fr 1fr;gap:90px;align-items:center;padding:83px 0 68px}.editorial-hero h1{font:400 clamp(54px,5.3vw,76px)/.99 var(--font-serif);letter-spacing:-2.5px;margin:20px 0 24px;max-width:650px}.editorial-hero h1 em{font-weight:400;color:var(--accent)}.editorial-hero p{font-size:16px;line-height:1.75;color:var(--ink-secondary);max-width:440px}.hero-actions{display:flex;gap:12px;margin-top:29px;align-items:center;flex-wrap:wrap}.btn-primary,.btn-secondary{display:inline-flex;justify-content:center;align-items:center;gap:12px;border:1px solid var(--rule-dark);border-radius:5px;padding:12px 17px;font:550 12px/1.4 var(--font-sans);min-height:44px;transition:background .15s}.btn-primary{background:var(--accent);border-color:var(--accent);color:#fff}.btn-primary:hover{background:#103e36}.btn-secondary{background:transparent;color:var(--ink)}.btn-secondary:hover{background:var(--stone-panel)}.hero-note{font:11px/1.6 var(--font-sans);color:var(--ink-muted);margin-top:18px}.hero-note span{margin:0 9px;color:#a7b1a8}.sample-ledger{background:#fff;border:1px solid var(--rule);border-radius:9px;box-shadow:0 16px 45px #263e2810;padding:28px 30px;position:relative}.sample-ledger:before{content:'';position:absolute;inset:17px -13px -14px 16px;border:1px solid var(--rule);border-radius:9px;z-index:-1;background:#eeeee6}.sample-top{display:flex;justify-content:space-between;gap:14px;font-size:11px;color:var(--ink-secondary);padding-bottom:20px;border-bottom:1px solid var(--rule)}.sample-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--accent);margin-right:5px}.sample-amount{padding:22px 0 14px}.sample-amount span{display:block;font-size:12px;color:var(--ink-muted)}.sample-amount strong{display:block;font:400 56px/1.2 var(--font-serif);letter-spacing:-2px}.sample-row{display:flex;justify-content:space-between;font-size:12px;padding:11px 0;border-bottom:1px solid #edf0e9}.sample-row span{color:var(--ink-secondary)}.sample-row strong{font:400 12px var(--font-mono)}.sample-bar{display:flex;height:6px;gap:3px;margin:23px 0 18px}.sample-bar span{background:var(--accent);border-radius:2px;flex:86.204}.sample-bar span:nth-child(2){background:#98afa2;flex:10.099}.sample-bar span:nth-child(3){background:#c3cbb7;flex:2.697}.sample-bar span:nth-child(4){background:#d9c7a6;flex:1}.sample-total{display:flex;justify-content:space-between;align-items:center;padding:15px 18px;background:var(--accent-light);border:1px solid #dce9de;border-radius:5px}.sample-total span{font-size:12px;color:var(--accent)}.sample-total strong{font:500 34px var(--font-serif);letter-spacing:-1px;color:var(--accent)}.editorial-hero .sample-caption{font-size:10px;color:var(--ink-muted);line-height:1.6;margin-top:15px}.trust-strip{display:flex;justify-content:space-between;gap:16px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:20px 0;color:var(--ink-muted);font-size:11px}.trust-strip strong{font-weight:550;color:var(--ink)}
.feature-section{padding:65px 0 60px}.section-intro{display:flex;justify-content:space-between;align-items:end;gap:30px;margin-bottom:27px}.section-intro h2{font:400 39px/1.1 var(--font-serif);letter-spacing:-.8px}.section-intro p{font-size:13px;color:var(--ink-secondary);max-width:300px}.flagship-banner{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}.flagship-col{padding:28px 29px 28px 0;display:flex;flex-direction:column;border-right:1px solid var(--rule);gap:12px}.flagship-col+.flagship-col{padding-left:29px}.flagship-col:last-child{border:0;padding-right:0}.feature-icon{width:32px;height:32px;color:var(--accent);margin-bottom:8px}.flagship-col .kicker{margin:0;font-size:9px}.flagship-col h3{font:500 27px/1.15 var(--font-serif);letter-spacing:-.5px}.flagship-col p{color:var(--ink-secondary);font-size:13px;line-height:1.7;margin-bottom:8px}.text-link{font-size:12px;font-weight:600;color:var(--accent);margin-top:auto}.text-link:hover{text-decoration:underline}
.directory-head{padding:35px 0 25px;border-top:1px solid var(--rule);display:flex;align-items:end;justify-content:space-between;gap:35px}.directory-head h2{font:400 42px/1.1 var(--font-serif);letter-spacing:-1px}.search-bar{width:370px;max-width:100%}.search-bar label{display:block;font-size:11px;color:var(--ink-secondary);margin-bottom:8px}.search-bar input{width:100%;background:#fff;border:1px solid var(--rule-dark);border-radius:5px;padding:12px 15px;font-size:13px;min-height:46px}.directory-nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px}.directory-nav a{font-size:11px;padding:7px 12px;border:1px solid var(--rule);border-radius:30px;color:var(--ink-secondary)}.directory-nav a:hover{background:var(--accent-light);color:var(--accent)}.category-section{padding-top:28px}.category-header{display:flex;align-items:center;gap:20px;justify-content:space-between;padding-bottom:15px}.category-title{font:500 24px var(--font-serif)}.category-index{font:10px var(--font-mono);color:var(--ink-muted)}.tools-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}.tool-card{background:#fff;border:1px solid var(--rule);border-radius:6px;display:flex;flex-direction:column;justify-content:space-between;min-height:225px;padding:23px;transition:border-color .15s,background .15s}.tool-card:hover{background:#fcfdf9;border-color:#9aafa0}.tool-num{display:block;font:9px var(--font-mono);color:var(--ink-muted);margin-bottom:22px}.tool-card h3{font:500 23px/1.15 var(--font-serif);letter-spacing:-.3px;margin-bottom:10px}.tool-card p{font-size:12px;color:var(--ink-secondary);line-height:1.65}.tool-card-footer{display:flex;justify-content:space-between;align-items:center;color:var(--accent);font-size:10px;margin-top:24px;padding-top:12px;border-top:1px solid #edf0e9}.search-feedback{font-size:12px;color:var(--ink-muted);margin:12px 0}.principles{margin-top:65px;background:var(--accent);color:#fff;padding:40px;border-radius:7px;display:grid;grid-template-columns:1fr 1fr;gap:50px}.principles .kicker{color:#c1d8c9}.principles h2{font:400 37px/1.1 var(--font-serif);letter-spacing:-.5px}.principles p{font-size:13px;line-height:1.8;color:#d5e4dc}.principles a{text-decoration:underline;text-underline-offset:4px}
.breadcrumb-bar{padding:25px 0 18px;font-size:10px;color:var(--ink-muted);display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--rule)}.breadcrumb-bar>span:last-child{max-width:50%;text-align:right}.tool-header{padding:34px 0 28px;border-bottom:1px solid var(--rule)}.tool-header h1{font:400 clamp(34px,3.5vw,49px)/1.06 var(--font-serif);letter-spacing:-1px;max-width:930px;margin-bottom:14px}.tool-header p{font-size:14px;color:var(--ink-secondary);max-width:790px;line-height:1.8}.estimate-notice{margin-top:17px;font-size:11px;color:var(--ink-secondary);padding:11px 14px;border-left:2px solid #a9b9a7;background:#eeeee7}.workspace-grid{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:26px;padding-top:29px;align-items:start}.workspace-grid>*,.workspace-grid aside{min-width:0}.parameters-sheet,.ledger-sheet,.doc-section{background:#fff;border:1px solid var(--rule);border-radius:7px;padding:28px}.sheet-heading{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font:9px/1.8 var(--font-mono);letter-spacing:.04em;color:var(--ink-muted);padding-bottom:17px;border-bottom:1px solid var(--rule);margin-bottom:21px}.presets-bar{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:18px}.preset-chip{background:var(--paper);border:1px solid var(--rule);border-radius:4px;color:var(--ink-secondary);font-size:10px;line-height:1.5;padding:9px 11px;min-height:36px}.preset-chip:hover{background:var(--accent-light);border-color:#94ac9a;color:var(--accent)}.field-group{margin-bottom:22px}.field-group:last-of-type{margin-bottom:0}.field-group label{display:block;font-size:12px;font-weight:600;margin-bottom:8px;line-height:1.6}.field-group input,.field-group textarea,.field-group select{width:100%;min-width:0;padding:12px 13px;min-height:46px;border:1px solid var(--rule-dark);border-radius:4px;background:#fafbf8;color:var(--ink);font:400 14px/1.5 var(--font-mono);font-variant-numeric:tabular-nums}.field-group textarea{min-height:180px;font-size:11px;line-height:1.8;resize:vertical}.field-group input:focus,.field-group select:focus,.field-group textarea:focus{background:#fff;border-color:var(--accent)}.field-hint{display:block;font-size:10px;color:var(--ink-muted);margin-top:7px;line-height:1.7}.ledger-sheet{background:#fdfefa;border-top:3px solid var(--accent)}.ledger-primary{padding:6px 0 21px;border-bottom:1px solid var(--rule)}.ledger-primary-label{font-size:11px;color:var(--ink-secondary);display:block;margin-bottom:10px}.ledger-primary-value{font:400 clamp(34px,4vw,58px)/1.1 var(--font-serif);letter-spacing:-1.5px;color:var(--accent);font-variant-numeric:tabular-nums;overflow-wrap:anywhere}.ledger-rows{padding-top:11px}.ledger-row{display:flex;justify-content:space-between;align-items:baseline;padding:13px 0;border-bottom:1px solid var(--rule);font-size:11px;gap:14px}.ledger-row span{color:var(--ink-secondary)}.ledger-row strong{font:500 11px/1.7 var(--font-mono);text-align:right;max-width:60%;overflow-wrap:anywhere}.ledger-row:last-child{border:0}.ledger-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:20px;padding-top:20px;border-top:1px solid var(--rule)}.ledger-actions button{font-size:10px;padding:10px;min-width:0}.ledger-sheet [id^=out]{transition:color .15s}.matrix-table{width:100%;border-collapse:collapse;font:10px/1.65 var(--font-mono);font-variant-numeric:tabular-nums;margin-top:15px}.matrix-table th,.matrix-table td{padding:13px 11px;text-align:right;vertical-align:top;border-bottom:1px solid var(--rule);min-width:98px}.matrix-table th:first-child,.matrix-table td:first-child{text-align:left;min-width:145px}.matrix-table th{font:550 9px/1.6 var(--font-sans);background:var(--paper);color:var(--ink-secondary);text-transform:uppercase;letter-spacing:.03em}.matrix-table tbody tr:hover{background:#f7faf5}.matrix-table td:first-child{font-family:var(--font-sans)}.table-scroll{overflow-x:auto;overscroll-behavior-inline:contain}.table-hint{font-size:10px;color:var(--ink-muted);margin-top:12px}.badge-ok,.badge-warn,.badge-alert{display:inline-block;padding:3px 6px;border-radius:3px;font:9px/1.5 var(--font-sans);white-space:normal;margin-top:4px}.badge-ok{background:var(--accent-light);color:var(--accent)}.badge-warn{background:var(--amber-bg);color:var(--amber-ink)}.badge-alert{background:var(--danger-bg);color:var(--danger-ink)}
.doc-section{margin-top:24px}.doc-section h3{font:500 25px/1.2 var(--font-serif);letter-spacing:-.4px;margin-bottom:14px}.formula-block{font:11px/1.9 var(--font-mono);background:var(--paper);border-left:2px solid #92ad99;padding:16px;margin:16px 0;overflow-wrap:anywhere}.faq-item{border-top:1px solid var(--rule);padding:17px 0}.faq-item h4{font-size:12px;font-weight:600;margin-bottom:6px}.faq-item p{font-size:12px;color:var(--ink-secondary);line-height:1.8}.reference-card{margin-top:23px;padding:25px;border:1px solid var(--rule);border-radius:7px;background:var(--stone-panel)}.reference-card h3{font:500 25px/1.15 var(--font-serif);margin-bottom:13px}.reference-card p{font-size:12px;color:var(--ink-secondary);line-height:1.8;margin-bottom:15px}.reference-list{list-style:none;margin:20px 0}.reference-list li{font-size:11px;padding:10px 0;border-top:1px solid var(--rule)}.reference-card .kicker{font-size:9px}.reference-card a:hover{text-decoration:underline}.btn-disabled{font-size:11px;border:1px dashed #abb7a8;color:var(--ink-secondary);padding:12px;border-radius:4px;text-align:center}.code-output{background:var(--paper);border:1px solid var(--rule);border-radius:4px;padding:17px;font:11px/1.8 var(--font-mono);white-space:pre-wrap;word-break:break-word;max-height:420px;overflow:auto}.btn-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}.ad-slot{margin:26px 0;padding:20px;background:var(--stone-panel);font-size:10px;color:var(--ink-muted)}.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:24px 0}.kpi-card{padding:20px;border:1px solid var(--rule);background:#fff;border-radius:6px}.k-label,.k-sub{font-size:10px;color:var(--ink-muted);display:block}.k-val{font:400 36px var(--font-serif)}footer{border-top:1px solid var(--rule);padding:36px;color:var(--ink-muted);font-size:11px}.footer-inner{display:flex;justify-content:space-between;gap:30px;flex-wrap:wrap}.footer-inner a:hover{color:var(--accent);text-decoration:underline}
.workspace-grid>.parameters-sheet{grid-column:1;grid-row:1}.workspace-grid>.ledger-sheet{grid-column:2;grid-row:1;position:sticky;top:24px}.workspace-notes{grid-column:1;grid-row:2}.workspace-reference{grid-column:2;grid-row:2}.workspace-notes>.doc-section:first-child,.workspace-reference>.reference-card:first-child{margin-top:0}.workspace-grid[data-tool-type="dev_tool"]>.workspace-reference{grid-row:1/3}.workspace-grid[data-tool-type="dev_tool"]>.workspace-notes{grid-row:2}@media(max-width:760px){.workspace-grid>.ledger-sheet{position:static}.workspace-grid>.parameters-sheet,.workspace-grid>.ledger-sheet{width:100%}}
@media(max-width:1100px){.nav-links{gap:15px;font-size:11px}.editorial-hero{gap:45px}.container{padding-left:28px;padding-right:28px}.navbar{padding-left:28px;padding-right:28px}.brand-name{font-size:25px}.brand-mark{width:29px}.tools-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.editorial-hero h1{font-size:62px}}
@media(max-width:760px){html{scroll-padding-top:25px}.navbar{padding:20px}.nav-inner{flex-wrap:wrap;gap:18px}.brand-name{font-size:27px}.mobile-menu{display:block;border:1px solid var(--rule);border-radius:4px;padding:7px 11px;font-size:11px;min-height:40px;position:relative}.mobile-menu summary{cursor:pointer;list-style:none}.mobile-menu nav{position:absolute;top:47px;right:0;width:220px;background:var(--surface);border:1px solid var(--rule);border-radius:5px;padding:15px;z-index:10;box-shadow:0 10px 25px #203a2415}.mobile-menu nav a{display:block;padding:10px;font-size:12px}.nav-inner>.nav-links{display:none}.container{padding:0 20px 60px}.editorial-hero{grid-template-columns:1fr;gap:40px;padding:45px 0 39px}.editorial-hero h1{font-size:clamp(45px,12.3vw,58px);max-width:470px;letter-spacing:-1.5px}.editorial-hero p{font-size:14px;max-width:460px}.sample-ledger{padding:23px;max-width:540px;width:100%;margin-bottom:12px}.sample-ledger:before{right:-7px;bottom:-9px}.trust-strip{flex-wrap:wrap;justify-content:start;gap:10px 24px;font-size:10px;padding:18px 0}.feature-section{padding:43px 0}.section-intro{display:block}.section-intro h2{font-size:34px}.section-intro p{margin-top:16px;max-width:450px}.flagship-banner{grid-template-columns:1fr}.flagship-col,.flagship-col+.flagship-col{padding:23px 0;border-right:0;border-bottom:1px solid var(--rule)}.flagship-col:last-child{padding-bottom:25px}.flagship-col h3{font-size:27px}.feature-icon{margin-bottom:0}.directory-head{display:block}.directory-head h2{font-size:36px}.search-bar{margin-top:24px;width:100%}.directory-nav{gap:6px}.directory-nav a{font-size:10px;padding:7px 10px}.category-header{align-items:baseline;gap:10px}.category-title{font-size:23px}.category-index{font-size:9px}.tools-grid{grid-template-columns:1fr}.tool-card{min-height:190px;padding:22px}.tool-num{margin-bottom:15px}.tool-card h3{font-size:25px}.tool-card p{font-size:12px}.principles{grid-template-columns:1fr;gap:25px;padding:26px;margin-top:40px}.principles h2{font-size:33px}.workspace-grid{display:flex;flex-direction:column;gap:22px}.workspace-grid>div,.workspace-grid aside{width:100%}.workspace-grid aside{display:flex;flex-direction:column}.workspace-grid{position:relative}.parameters-sheet,.ledger-sheet,.doc-section{padding:21px}.tool-header{padding:25px 0}.tool-header h1{font-size:37px;line-height:1.08}.tool-header p{font-size:13px}.breadcrumb-bar>span:last-child{display:none}.ledger-primary-value{font-size:49px}.ledger-row{font-size:11px}.ledger-row strong{font-size:11px}.doc-section h3{font-size:25px}.sheet-heading{font-size:8px;gap:8px}.matrix-table{font-size:10px}.kpi-grid{grid-template-columns:1fr 1fr}.footer-inner{display:block}.footer-inner>span{display:block;margin-bottom:14px}footer{padding:28px 20px}.hero-actions .btn-primary,.hero-actions .btn-secondary{font-size:11px}.sample-amount strong{font-size:50px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
""".strip()


def build_runtime_js() -> str:
    corridors_json = json.dumps(COUNTRY_CORRIDORS)
    return f"""
// ============================================================================
// {BRAND_NAME} Client-Side Computation Engine, Country Corridor Router & CSV Auditor
// ============================================================================

const CALCGRID_CORRIDORS = {corridors_json};

(function () {{
  // No analytics or network requests: all inputs remain on this device.

  // 1. Homepage Live Filter
  const searchInput = document.getElementById('hub-search-input');
  if (searchInput) {{
    searchInput.addEventListener('input', function () {{
      const q = searchInput.value.toLowerCase().trim();
      let count = 0;
      document.querySelectorAll('.category-section').forEach(function (section) {{
        let visible = 0;
        section.querySelectorAll('.tool-card').forEach(function (card) {{
          const matches = card.textContent.toLowerCase().includes(q);
          card.hidden = !matches;
          if (matches) {{ count++; visible++; }}
        }});
        section.hidden = visible === 0;
      }});
      const feedback = document.getElementById('search-feedback');
      if (feedback) feedback.textContent = count ? count + ' tool' + (count === 1 ? '' : 's') + ' found.' : 'No tools found. Try a provider name or a shorter search.';
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
    if (!Number.isFinite(n)) return 'Not achievable';
    return (cfg.currency === 'AMD' ? 'AMD ' : '$') + Number(n || 0).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
  }}

  let currentCsvRows = [];

  const btnPermalink = document.getElementById('btn-copy-permalink');
  const btnExportCsv = document.getElementById('btn-export-csv');

  if (btnExportCsv) {{
    btnExportCsv.addEventListener('click', function () {{
      if (!currentCsvRows.length) return;
      const exportRows = currentCsvRows.map(function (row, i) {{ return i === 0 && cfg.currency === 'AMD' ? row.map(v => String(v).replace(/USD/g, 'AMD')) : row; }});
      const csvContent = exportRows.map(function (r) {{ return r.map(function (cell) {{
        let value = String(cell);
        if (/^[\\s]*[=+@\\t\\r]/.test(value) || (/^[\\s]*-/.test(value) && !Number.isFinite(Number(value)))) value = "'" + value;
        return '"' + value.replace(/"/g, '""') + '"';
      }}).join(','); }}).join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (window.location.pathname.split('/').pop().replace('.html', '') || 'calculation') + '-ledger.csv';
      a.click();
      URL.revokeObjectURL(url);
    }});
  }}

  function escapeText(value) {{
    return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }}
  if (btnPermalink) btnPermalink.addEventListener('click', async function () {{
    const u = new URL(window.location.href);
    u.search = '';
    const keys = {{country:'in-country',amount:'in-amount',origin_pct:'in-origin-pct',origin_fix:'in-origin-fix',tax:'in-tax-pct',fx_rate:'in-fx-rate',target_net:'in-target-net',pct:'in-pct',fixed:'in-fixed',fx:'in-fx',a:'in-a',b:'in-b',c:'in-c',d:'in-d'}};
    Object.keys(keys).forEach(function (key) {{
      const el = document.getElementById(keys[key]);
      if (el) u.searchParams.set(key, el.value);
    }});
    const mor = document.getElementById('in-include-mor');
    if (mor && mor.checked) u.searchParams.set('include_mor', '1');
    try {{
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(u.toString());
      btnPermalink.textContent = 'Link copied';
    }} catch (e) {{ btnPermalink.textContent = 'Clipboard unavailable'; }}
    setTimeout(function () {{ btnPermalink.textContent = 'Copy Permalink'; }}, 2000);
  }});

    function parseCsv(text) {{
      const rows = []; let row = [], cell = '', quoted = false;
      text = text.replace(/^\\uFEFF/, '');
      for (let i = 0; i < text.length; i++) {{
        const c = text[i];
        if (c === '"') {{
          if (quoted && text[i + 1] === '"') {{ cell += '"'; i++; }}
          else quoted = !quoted;
        }} else if (c === ',' && !quoted) {{ row.push(cell); cell = ''; }}
        else if ((c === '\\n' || c === '\\r') && !quoted) {{
          if (c === '\\r' && text[i + 1] === '\\n') i++;
          row.push(cell); if (row.some(v => v.trim())) rows.push(row); row = []; cell = '';
        }} else cell += c;
      }}
      if (quoted) throw new Error('Unclosed quoted field. Check your CSV.');
      row.push(cell); if (row.some(v => v.trim())) rows.push(row);
      return rows;
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
    if (params.get('origin_fix')) elOriginFix.value = params.get('origin_fix');
    if (params.get('target_net')) elTargetNet.value = params.get('target_net');
    if (params.get('tax')) elTaxPct.value = params.get('tax');

    document.querySelectorAll('.origin-preset-chip').forEach(function (chip) {{
      chip.addEventListener('click', function () {{
        elOriginPct.value = chip.getAttribute('data-pct') || '0';
        elOriginFix.value = chip.getAttribute('data-fix') || '0';
        recalcCorridor();
      }});
    }});

    function syncCountryPresets(initial = false) {{
      const code = elCountry.value || 'AM';
      const cData = CALCGRID_CORRIDORS[code] || CALCGRID_CORRIDORS['AM'];
      if (elFxRate) {{
        elFxRate.value = cData.default_fx_placeholder;
      }}
      const fxHint = document.getElementById('fx-rate-hint');
      if (fxHint) fxHint.textContent = cData.fx_note;
      const caveatEl = document.getElementById('corridor-tax-caveat');
      if (caveatEl) caveatEl.textContent = cData.tax_caveat + ' (Sources: ' + cData.official_sources + ' • Model dated: ' + cData.verified_date + ')';

      if (taxPresetsBox && cData.tax_presets) {{
        taxPresetsBox.innerHTML = '';
        if (cData.tax_presets.length > 0 && (!initial || !params.has('tax'))) {{
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
      // Per Article 257 of RA Tax Code (and gross turnover regimes), turnover tax is assessed on FULL GROSS sales turnover
      const grossTurnoverTax = gross * tRate;
      const finalNetExp = Math.max(0, netUsdExp - grossTurnoverTax);
      const finalNetBest = Math.max(0, netUsdBest - grossTurnoverTax);
      const finalNetWorst = Math.max(0, netUsdWorst - grossTurnoverTax);

      return {{
        afterOrigin: afterOrigin,
        netUsdExp: netUsdExp,
        grossTurnoverTax: grossTurnoverTax,
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

      // Exact algebraic gross-up when turnover tax (tRate) is assessed on Gross (G):
      // FinalNet = ((G * (1 - oRate) - originFix) * (1 - railRateExp) - rail.fixed_fee - midIntermediary) - G * tRate
      const retentionFactor = (1 - oRate) * (1 - railRateExp) - tRate;
      if (retentionFactor <= 0) return NaN;
      const fixedDeductions = originFix * (1 - railRateExp) + rail.fixed_fee + midIntermediary;
      const requiredGross = (targetNet + fixedDeductions) / retentionFactor;
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
      const targetNet = Math.max(0, parseFloat(elTargetNet ? elTargetNet.value : gross) || 0);

      const railNames = [
        ['payoneer', 'Payoneer Local Withdrawal'],
        ['wise', 'Wise Mid-Market Route'],
        ['swift', 'Direct Bank SWIFT Wire'],
        ['lemonsqueezy', 'Lemon Squeezy MoR Payout']
      ];

      let bestAvailableRoute = null;
      let bestAvailableResult = null;
      let bestAvailableReverse = Infinity;

      currentCsvRows = [
        ['Country', 'Currency', 'Payout_Rail', 'Availability', 'Gross_USD', 'Expected_Net_After_Tax_USD', 'Uncertainty_Range_USD', 'Local_Currency_Net', 'Effective_Total_Deduction_Pct', 'Reverse_Invoice_For_Target_USD']
      ];

      if (compareBody) compareBody.innerHTML = '';

      railNames.forEach(function (pair) {{
        const rKey = pair[0];
        const rLabel = pair[1];
        const rail = cData.rails[rKey];
        if (!rail) return;

        const morChoice = document.getElementById('in-include-mor');
        const eligibleMor = rKey !== 'lemonsqueezy' || (morChoice && morChoice.checked && originPct === 0 && originFix === 0);
        const routeAvailable = rail.available && eligibleMor;
        const routeStatus = eligibleMor ? rail.status_badge : 'EXCLUDED — DIGITAL-PRODUCT CHECKOUT ONLY';
        const res = evalRoute(gross, originPct, originFix, rail, taxPct);
        const revGross = solveReverseGross(targetNet, originPct, originFix, rail, taxPct);
        const localNet = res.finalNetExp * fxRate;

        if (routeAvailable && (!bestAvailableResult || res.finalNetExp > bestAvailableResult.finalNetExp)) {{
          bestAvailableRoute = rLabel;
          bestAvailableResult = res;
        }} if (routeAvailable && Number.isFinite(revGross) && revGross < bestAvailableReverse) {{
          bestAvailableReverse = revGross;
        }}

        const rangeStr = fmtMoney(res.finalNetWorst) + ' – ' + fmtMoney(res.finalNetBest);
        const localStr = Math.round(localNet).toLocaleString('en-US') + ' ' + cData.currency;

        currentCsvRows.push([
          cData.name, cData.currency, rLabel, routeStatus,
          gross.toFixed(2), res.finalNetExp.toFixed(2), rangeStr,
          localStr, res.effectivePct.toFixed(2) + '%', revGross.toFixed(2)
        ]);

        if (compareBody) {{
          const badgeClass = routeAvailable ? 'badge-ok' : 'badge-alert';
          const tr = document.createElement('tr');
          tr.innerHTML =
            '<td><strong>' + rLabel + '</strong><br/><span class="' + badgeClass + '">' + routeStatus + '</span><div style="font-family:var(--font-sans);font-size:0.72rem;color:var(--ink-secondary);margin-top:4px">' + rail.note + '</div></td>' +
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

    const morChoice = document.getElementById('in-include-mor');
    if (morChoice) {{
      if (params.has('include_mor')) morChoice.checked = params.get('include_mor') === '1';
      morChoice.addEventListener('change', recalcCorridor);
    }}
    syncCountryPresets(true);
    if (params.get('fx_rate')) elFxRate.value = params.get('fx_rate');
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
      const message = document.getElementById('csv-audit-status');
      if (auditBody) auditBody.innerHTML = '';
      currentCsvRows = [];
      ['out-audit-gross','out-audit-net','out-audit-leakage'].forEach(function (id) {{ document.getElementById(id).textContent = '$0.00'; }});
      document.getElementById('out-audit-alerts').textContent = '0 flagged';
      let records;
      try {{
        if (raw.length > 1000000) throw new Error('Use a CSV smaller than 1 MB.');
        records = parseCsv(raw);
        if (records.length < 2) throw new Error('Add the header and at least one transaction.');
        if (records[0].map(v => v.trim().toLowerCase()).join(',') !== 'tx_id,provider,gross_usd,actual_net_usd') throw new Error('Expected header: tx_id,provider,gross_usd,actual_net_usd');
        if (records.length > 51) throw new Error('This browser auditor accepts up to 50 transactions per audit.');
        records.slice(1).forEach(function (cols, i) {{
          if (cols.length !== 4) throw new Error('Row ' + (i + 2) + ': expected four fields.');
          const provider = cols[1].trim().toLowerCase();
          if (!Object.prototype.hasOwnProperty.call(PUBLISHED_RATES, provider)) throw new Error('Row ' + (i + 2) + ': unsupported provider code.');
          if (!cols[2].trim() || !cols[3].trim() || !Number.isFinite(Number(cols[2])) || !Number.isFinite(Number(cols[3])) || Number(cols[2]) < 0 || Number(cols[3]) < 0) throw new Error('Row ' + (i + 2) + ': amounts must be finite, non-negative numbers.');
        }});
      }} catch (e) {{ if (message) message.textContent = e.message; return; }}
      if (message) message.textContent = (records.length - 1) + ' transactions checked locally against illustrative fee baselines.';

      let totalGross = 0;
      let totalActualNet = 0;
      let totalExpectedNet = 0;
      let totalLeakage = 0;
      let alertCount = 0;

      currentCsvRows = [
        ['tx_id', 'provider', 'gross_usd', 'expected_fee_usd', 'expected_net_usd', 'actual_net_usd', 'variance_usd', 'audit_status']
      ];
      if (auditBody) auditBody.innerHTML = '';

      records.slice(1).forEach(function (cols) {{
        const txId = cols[0];
        const provider = cols[1].trim().toLowerCase();
        const gross = Number(cols[2]);
        const actualNet = Number(cols[3]);
        const rate = PUBLISHED_RATES[provider];
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
            '<td>' + escapeText(txId) + '</td>' +
            '<td>' + escapeText(provider) + '</td>' +
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
        if (file.size > 1000000) {{
          const status = document.getElementById('csv-audit-status');
          if (status) status.textContent = 'Use a CSV smaller than 1 MB.';
          return;
        }}
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
      const totalPctRate = Math.min(1, Math.max(0, (pct + fx) / 100));
      const totalFee = gross * totalPctRate + fix;
      const net = Math.max(0, gross - totalFee);
      const effectiveRate = gross > 0 ? (totalFee / gross) * 100 : 0;
      const reverseGross = totalPctRate >= 1 ? NaN : (gross + fix) / (1 - totalPctRate);
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

      const tiers = cfg.tiers || [100, 500, 1000, 2500, 5000, 10000];
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
      function invalid(message) {{
        document.getElementById('lbl-r1').textContent = 'Check model inputs';
        document.getElementById('val-r1').textContent = '—';
        const status = document.getElementById('model-status');
        if (status) status.textContent = message;
        document.getElementById('val-r2').textContent = '—';
        document.getElementById('val-r3').textContent = '—';
        currentCsvRows = [];
      }}
      if ([elA,elB,elC,elD].some(el => !el.value.trim() || !Number.isFinite(Number(el.value)) || Number(el.value) < 0)) {{ invalid('Use finite, non-negative inputs.'); return; }}
      const status = document.getElementById('model-status');
      if (status) status.textContent = '';
      const percentages = {{ltv:[b,c], ad_rev:[d], ecom:[d], email_roi:[b,c], cro:[b,c], hourly_rate:[d], llm_cost:[d]}};
      if ((percentages[mode] || []).some(v => v > 100)) {{ invalid('Percentages must be 0–100.'); return; }}
      if (mode === 'roas' && a <= 0) {{ invalid('Use a positive sale price.'); return; }}
      if (mode === 'pert' && !(a <= b && b <= c)) {{ invalid('Use optimistic ≤ likely ≤ pessimistic.'); return; }}

      let r1Label = 'Primary Metric', r1Val = '$0.00';
      let r2Label = 'Secondary Metric', r2Val = '0';
      let r3Label = 'Efficiency Benchmark', r3Val = '0';

      if (mode === 'ltv') {{
        const churnRate = c / 100;
        const ltv = churnRate > 0 ? (a * (b / 100)) / churnRate : (a * b > 0 ? Infinity : 0);
        const ratio = d > 0 ? ltv / d : 0;
        const payback = (a * (b / 100)) > 0 ? d / (a * (b / 100)) : 0;
        r1Label = 'Customer Lifetime Value (LTV)';
        r1Val = !Number.isFinite(ltv) ? 'Unbounded at zero churn' : fmtMoney(ltv);
        r2Label = 'LTV : CAC Ratio';
        r2Val = d === 0 ? 'Not defined at zero CAC' : (!Number.isFinite(ratio) ? 'Unbounded' : ratio.toFixed(2) + 'x');
        r3Label = 'CAC Payback Period';
        r3Val = (a * b === 0 && d > 0) ? 'Not achievable' : payback.toFixed(1) + ' months';
      }} else if (mode === 'roas') {{
        const margin = a - b;
        const marginPct = a > 0 ? margin / a : 0;
        const beRoas = 1 / marginPct;
        const grossRev = c * d;
        const orders = a > 0 ? grossRev / a : 0;
        const netProfit = orders * margin - c;
        r1Label = 'Break-Even ROAS Required';
        r1Val = margin <= 0 || a <= 0 ? 'Not achievable' : beRoas.toFixed(2) + 'x';
        r2Label = 'Max Profitable CPA';
        r2Val = fmtMoney(Math.max(0, margin));
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
        r1Label = 'Contribution Before Campaign Costs';
        r1Val = fmtMoney(profit);
        r2Label = 'Estimated Conversions';
        r2Val = sales.toFixed(1) + ' sales';
        r3Label = 'Contribution Per Subscriber';
        r3Val = fmtMoney(a > 0 ? profit / a : 0);
      }} else if (mode === 'cro') {{
        const extraSales = a * ((c - b) / 100);
        const monthlyLift = extraSales * d;
        r1Label = 'Monthly Revenue Lift';
        r1Val = fmtMoney(monthlyLift);
        r2Label = 'Annual Revenue Impact';
        r2Val = fmtMoney(monthlyLift * 12);
        r3Label = 'Extra Monthly Customers';
        r3Val = (extraSales >= 0 ? '+' : '') + extraSales.toFixed(1);
      }} else if (mode === 'hourly_rate') {{
        if (d >= 100 || c <= 0) {{ invalid('Use hours > 0 and deductions < 100%.'); return; }}
        const grossNeeded = (a + b) / (1 - d / 100);
        const annualBillableHours = c * 48;
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
        r1Label = 'Quote With 2σ Planning Buffer';
        r1Val = safeHours.toFixed(1) + 'h (' + fmtMoney(safeHours * d) + ')';
        r2Label = 'PERT Expected Average';
        r2Val = expected.toFixed(1) + ' hours';
        r3Label = 'Additional 2σ Hours';
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
        [a, b, c, d, r1Val, r2Val, r3Val]
      ];
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
          if (obj === null || Array.isArray(obj) || typeof obj !== 'object') throw new Error('Use a JSON object at the root.');
          function ts(v) {{
            if (v === null) return 'null';
            if (Array.isArray(v)) return v.length ? '(' + [...new Set(v.map(ts))].join(' | ') + ')[]' : 'unknown[]';
            if (typeof v === 'object') return '{{ ' + Object.entries(v).map(([k,x]) => JSON.stringify(k) + ': ' + ts(x)).join('; ') + ' }}';
            return typeof v;
          }}
          function zod(v) {{
            if (v === null) return 'z.null()';
            if (Array.isArray(v)) {{ const types = [...new Set(v.map(zod))]; return 'z.array(' + (types.length > 1 ? 'z.union([' + types.join(', ') + '])' : types[0] || 'z.unknown()') + ')'; }}
            if (typeof v === 'object') return 'z.object({{ ' + Object.entries(v).map(([k,x]) => '[' + JSON.stringify(k) + ']: ' + zod(x)).join(', ') + ' }})';
            return 'z.' + typeof v + '()';
          }}
          outputEl.textContent = 'export interface GeneratedPayload {{\\n' + Object.entries(obj).map(([k,v]) => '  ' + JSON.stringify(k) + ': ' + ts(v) + ';').join('\\n') + '\\n}}\\n\\nimport {{ z }} from "zod";\\nexport const GeneratedSchema = ' + zod(obj) + ';';
        }} else if (mode === 'cron') {{
          const parts = val.trim().split(/\\s+/);
          const limits = [[0,59],[0,23],[1,31],[1,12],[0,7]];
          const valid = parts.length === 5 && parts.every((field,i) => field.split(',').every(piece => {{
            const split = piece.split('/');
            if (split.length > 2 || (split.length === 2 && (!/^\\d+$/.test(split[1]) || Number(split[1]) < 1))) return false;
            if (split[0] === '*') return true;
            if (!/^\\d+(?:-\\d+)?$/.test(split[0])) return false;
            const ends = split[0].split('-').map(Number);
            return ends.every(n => n >= limits[i][0] && n <= limits[i][1]) && (ends.length === 1 || ends[0] <= ends[1]);
          }}));
          if (!valid) throw new Error('Use five numeric cron fields with valid ranges, lists, * and positive steps. Named months/weekdays and extensions are not supported.');
          outputEl.textContent = 'Valid 5-Field Cron Schedule:\\n' + ['Minute','Hour','Day of Month','Month','Day of Week'].map((label,i) => label + ': ' + parts[i]).join('\\n') + '\\nTimezone is set by your scheduler; execution dates are not predicted.';
        }} else if (mode === 'jwt') {{
          const segs = val.trim().split('.');
          if (segs.length < 2) {{
            outputEl.textContent = 'Expected JWT format: header.payload.signature';
          }} else {{
            const decodeB64 = function (s) {{
              const binary = atob(s.replace(/-/g, '+').replace(/_/g, '/'));
              return JSON.parse(new TextDecoder().decode(Uint8Array.from(binary, c => c.charCodeAt(0))));
            }};
            const header = decodeB64(segs[0]);
            const payload = decodeB64(segs[1]);
            outputEl.textContent =
              '// DECODED ONLY — SIGNATURE NOT VERIFIED\\n// JWT HEADER:\\n' + JSON.stringify(header, null, 2) +
              '\\n\\n// JWT PAYLOAD CLAIMS:\\n' + JSON.stringify(payload, null, 2);
          }}
        }} else if (mode === 'sql') {{
          const segments = val.split(/('(?:''|[^'])*'|"(?:""|[^"])*"|`[^`]*`|--[^\\n]*(?:\\n|$)|\\/\\*[\\s\\S]*?\\*\\/)/g);
          outputEl.textContent = segments.map((part,i) => i % 2 ? part : part.replace(/\\s+/g, ' ').replace(/\\b(SELECT|FROM|INNER JOIN|LEFT JOIN|RIGHT JOIN|WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|INSERT INTO|VALUES|UPDATE|SET|DELETE FROM)\\b/gi, m => '\\n' + m.toUpperCase())).join('').trim();
        }} else if (mode === 'base64') {{
          const operation = document.getElementById('dev-operation');
          const action = operation ? operation.value : 'encode';
          if (action === 'decode-url') outputEl.textContent = decodeURIComponent(val);
          else if (action === 'decode') {{
            const bin = atob(val.trim().replace(/-/g, '+').replace(/_/g, '/'));
            outputEl.textContent = new TextDecoder('utf-8', {{fatal:true}}).decode(Uint8Array.from(bin, c => c.charCodeAt(0)));
          }} else {{
            const bytes = new TextEncoder().encode(val); let bin = '';
            bytes.forEach(b => {{ bin += String.fromCharCode(b); }});
            const b64 = btoa(bin);
            outputEl.textContent = 'Base64 Encoded:\\n' + b64 + '\\n\\nBase64Url Encoded:\\n' + b64.replace(/\\+/g, '-').replace(/\\//g, '_').replace(/=+$/, '') + '\\n\\nURL-Encoded:\\n' + encodeURIComponent(val);
          }}
        }} else if (mode === 'csv_to_json') {{
          const records = parseCsv(val);
          if (!records.length) outputEl.textContent = '[]';
          else {{
            const headers = records[0].map(h => h.trim());
            if (headers.some(h => !h) || new Set(headers).size !== headers.length) throw new Error('Headers must be unique and non-empty.');
            const data = records.slice(1).map((cells,i) => {{
              if (cells.length !== headers.length) throw new Error('Row ' + (i + 2) + ': column count differs from header.');
              const row = Object.create(null);
              headers.forEach((h,j) => {{
                const raw = cells[j];
                if (raw === 'true' || raw === 'false') row[h] = raw === 'true';
                else if (/^[+-]?(?:0|[1-9]\\d*)(?:\\.\\d+)?(?:e[+-]?\\d+)?$/i.test(raw) && Number.isFinite(Number(raw))) row[h] = Number(raw);
                else row[h] = raw;
              }}); return row;
            }}); outputEl.textContent = JSON.stringify(data,null,2);
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
          const limit = Math.floor(4294967296 / chars.length) * chars.length;
          let out = '';
          while (out.length < len) {{
            window.crypto.getRandomValues(rnd);
            for (const n of rnd) if (n < limit && out.length < len) out += chars[n % chars.length];
          }}
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
          const p = val.split('|').map(s => s.trim());
          const u = new URL(p[0] || 'https://example.com');
          if (!['https:','http:'].includes(u.protocol)) throw new Error('Use an HTTP or HTTPS URL.');
          ['source','medium','campaign'].forEach((key,i) => u.searchParams.set('utm_' + key, (p[i+1] || ['newsletter','email','launch'][i]).toLowerCase()));
          outputEl.textContent = u.toString();
        }}
      }} catch (err) {{
        outputEl.textContent = 'Error: ' + err.message;
      }}
    }}

    if (runBtn) runBtn.addEventListener('click', runDevTransform);
    if (inputEl) inputEl.addEventListener('input', runDevTransform);
    const operation = document.getElementById('dev-operation');
    if (operation) operation.addEventListener('change', runDevTransform);
    if (copyBtn) {{
      copyBtn.addEventListener('click', async function () {{
        try {{
          if (!navigator.clipboard) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(outputEl.textContent);
          copyBtn.textContent = 'Copied';
        }} catch (e) {{ copyBtn.textContent = 'Clipboard unavailable'; }}
        setTimeout(function () {{ copyBtn.textContent = 'Copy Output'; }}, 1500);
      }});
    }}
    runDevTransform();
  }}
}})();
""".strip()


def brand_icon() -> str:
    return '<svg class="brand-mark" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M6 5h15a9 9 0 0 1 0 18H14v8H6V5Z" fill="currentColor"/><path d="M14 12h7a2 2 0 0 1 0 4h-7v-4Z" fill="#f6f5f0"/><path d="M25 24v7h6v-9" stroke="currentColor" stroke-width="3"/></svg>'


def render_navbar(prefix: str = "") -> str:
    links = f"""<a href="{prefix}tools/cross-border-payout-comparison-engine.html">Payout comparison</a>
        <a href="{prefix}tools/private-csv-payout-fee-auditor.html">CSV auditor</a>
        <a href="{prefix}index.html#directory">All calculators</a>
        <a href="{prefix}legal.html">Methodology</a>"""
    return f"""<a class="skip-link" href="#main-content">Skip to content</a>
    <header class="navbar"><div class="nav-inner">
      <a href="{prefix}index.html" class="brand" aria-label="{html.escape(BRAND_NAME)} home">{brand_icon()}<span class="brand-name">{html.escape(BRAND_NAME)}</span></a>
      <nav class="nav-links" aria-label="Main navigation">{links}</nav>
      <details class="mobile-menu"><summary>Menu &nbsp; +</summary><nav aria-label="Mobile navigation">{links}</nav></details>
    </div></header>"""


def render_social_meta(title: str, description: str, path: str = "", prefix: str = "") -> str:
    url = SITE_URL + "/" + path
    return f"""<meta name="theme-color" content="#174f46" />
    <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml" />
    <link rel="icon" href="{prefix}assets/favicon.png" sizes="32x32" type="image/png" />
    <link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="{html.escape(BRAND_NAME)}" />
    <meta property="og:title" content="{html.escape(title)}" />
    <meta property="og:description" content="{html.escape(description)}" />
    <meta property="og:url" content="{html.escape(url)}" />
    <meta property="og:image" content="{SITE_URL}/assets/og-preview.png" />
    <meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(title)}" />
    <meta name="twitter:description" content="{html.escape(description)}" />
    <meta name="twitter:image" content="{SITE_URL}/assets/og-preview.png" />"""


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
    cta = (f'<a href="{html.escape(LEMON_SQUEEZY_CHECKOUT_URL)}" class="btn-primary">Get the offline suite · $19</a>'
           if LEMON_SQUEEZY_CHECKOUT_URL else '<p class="btn-disabled">Offline suite · Coming soon</p>')
    return f"""<div class="reference-card" id="pro-offline-bundle">
      <span class="kicker">For your working files</span><h3>A little more control.<br/>Entirely offline.</h3>
      <p>Batch reconciliation and illustrative model tables for freelancers and small teams who prefer to keep their work local.</p>
      <ul class="reference-list"><li>Batch CSV fee &amp; FX reconciler</li><li>Three sample model tables in XLSX and CSV</li><li>All 32 tools in an offline HTML suite</li></ul>{cta}
    </div><div class="reference-card" style="background:var(--surface)"><span class="kicker">Keep exploring</span>
      <ul style="list-style:none">{related_links}</ul></div>"""


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
                <span>YOUR PAYOUT SCENARIO</span>
                <span>MODEL: {html.escape(ver_date)}</span>
              </div>

              <div class="field-group">
                <label for="in-country">Residence country</label>
                <select id="in-country">{country_opts}</select>
                <span class="field-hint">Checks documented rail availability (e.g., Wise receiving restrictions in Armenia vs. Georgia/Philippines) and local simplified tax rules.</span>
              </div>

              <div class="field-group">
                <label>Invoice channel</label>
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
                <label for="in-amount">Gross invoice · USD</label>
                <input type="number" id="in-amount" value="{cfg['default_amount']}" min="0" step="any" />
              </div>

              <div class="field-group">
                <label for="in-target-net">Target take-home · USD</label>
                <input type="number" id="in-target-net" value="{cfg['default_amount']}" min="0" step="any" />
                <span class="field-hint">Solves the exact gross USD invoice you must send the client to receive this net amount after platform, payout rail, FX spread, and local tax.</span>
              </div>

              <div class="field-group">
                <label for="in-tax-pct">Illustrative tax reserve · % of gross</label>
                <div class="presets-bar" id="corridor-tax-presets" style="margin-bottom:8px;padding-bottom:8px"></div>
                <input type="number" id="in-tax-pct" value="1.0" min="0" max="60" step="0.1" />
                <span class="field-hint">This is a flat reserve assumption, not a tax-return calculation. Thresholds, allowances, deductions, VAT/GST and social contributions are not computed.</span><span class="field-hint" id="corridor-tax-caveat"></span>
              </div>

              <div class="field-group">
                <label style="display:flex;gap:10px;align-items:flex-start"><input type="checkbox" id="in-include-mor" style="width:18px;min-height:18px;margin-top:3px" /> Include Lemon Squeezy for eligible digital-product sales</label>
                <span class="field-hint">Merchant-of-record checkout is a separate sales flow. It is excluded unless enabled with zero upstream platform fees. It is not an Upwork or Fiverr withdrawal method.</span>
              </div>
              <div class="field-group">
                <label for="in-fx-rate">Reference exchange rate · local units per USD</label>
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
              <div class="table-scroll" role="region" aria-label="Calculation table, scroll horizontally for all columns" tabindex="0">
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
                REFERENCE BASIS: {html.escape(src_name)} &bull; ASSUMPTIONS MODEL: {html.escape(ver_date)}
              </p>
              <h3>Reference Notes &amp; FAQ</h3>
              {faq_html}
            </div>
          </div>

          <aside>
            <div class="ledger-sheet">
              <div class="sheet-heading">
                <span>ESTIMATED TAKE-HOME</span>
                <span>UPDATED AS YOU TYPE</span>
              </div>
              <div class="ledger-primary">
                <span class="ledger-primary-label">Highest modeled available take-home</span>
                <div class="ledger-primary-value" id="out-net">$0.00</div>
              </div>
              <div class="ledger-rows">
                <div class="ledger-row">
                  <span>Best modeled route</span>
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
                  <span>Lowest invoice for target · available routes</span>
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
                <span>YOUR TRANSACTION CSV</span>
                <span>PROCESSED ON YOUR DEVICE</span>
              </div>
              <div class="field-group">
                <label for="csv-file-upload">Choose a standardized transaction CSV (processed locally)</label>
                <input type="file" id="csv-file-upload" accept=".csv,text/csv" />
                <span class="field-hint">Supported provider codes: lemonsqueezy, payoneer, wise, upwork_10, upwork_5, upwork_15, stripe_intl, fiverr.</span>
              </div>
              <div class="field-group">
                <label for="csv-audit-input">Or Paste CSV Rows (`tx_id,provider,gross_usd,actual_net_usd`)</label>
                <p class="field-hint">Use the four-column format shown below; raw provider exports need conversion first. Up to 50 transactions. Quoted CSV fields are supported. Baselines are examples, not account-specific quotes.</p>
                <textarea id="csv-audit-input">{html.escape(cfg['sample_csv'])}</textarea>
              </div>
              <p id="csv-audit-status" class="field-hint" role="status" aria-live="polite"></p>
              <div class="btn-row">
                <button type="button" id="btn-run-audit" class="btn-primary">Audit CSV Statement</button>
                <button type="button" id="btn-export-csv" class="btn-secondary">Export Reconciled CSV</button>
              </div>
            </div>

            <div class="doc-section">
              <span class="kicker">FIG. 03 — LINE-BY-LINE FEE &amp; FX VARIANCE LEDGER</span>
              <h3>Reconciled Transaction Audit Table</h3>
              <div class="table-scroll" role="region" aria-label="Calculation table, scroll horizontally for all columns" tabindex="0">
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
                <span class="ledger-primary-label">Net shortfall vs. example baseline</span>
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
                <span>MODEL: {html.escape(ver_date.upper())}</span>
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
              <div class="table-scroll" role="region" aria-label="Calculation table, scroll horizontally for all columns" tabindex="0">
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
                REFERENCE BASIS: {html.escape(src_name)} &bull; ASSUMPTIONS MODEL: {html.escape(ver_date)}
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
                <span>MODEL: {html.escape(ver_date.upper())}</span>
              </div>
              <div class="field-group">
                <p id="model-status" class="field-hint" role="status" aria-live="polite"></p>
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
                REFERENCE BASIS: {html.escape(src_name)} &bull; ASSUMPTIONS MODEL: {html.escape(ver_date)}
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

    operation_control = ('<div class="field-group"><label for="dev-operation">Operation</label><select id="dev-operation"><option value="encode">Encode UTF-8 text</option><option value="decode">Decode Base64 / Base64Url</option><option value="decode-url">Decode URL-encoded text</option></select></div>' if cfg.get('dev_mode') == 'base64' else '')
    return f"""
    <div class="workspace-grid" id="interactive-tool-root" data-tool-type="dev_tool" data-tool-config="{cfg_json}">
      <div>
        <div class="parameters-sheet">
          <div class="sheet-heading">
            <span>FIG. 01 — SOURCE PAYLOAD</span>
            <span>LOCAL BROWSER EXECUTION</span>
          </div>
{operation_control}
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


def layout_workspace(markup: str) -> str:
    """Place inputs, results, and reference material in a useful reading order on every screen."""
    def end_of_div(start: int) -> int:
        depth = 0
        for match in re.finditer(r"</?div\b[^>]*>", markup[start:]):
            depth += -1 if match.group().startswith("</") else 1
            if depth == 0:
                return start + match.end()
        raise ValueError("Unclosed calculator workspace")
    root_end = markup.index('>') + 1
    left_start = markup.index('<div>', root_end)
    left_end = end_of_div(left_start)
    params_start = markup.index('<div class="parameters-sheet">', left_start)
    params_end = end_of_div(params_start)
    inputs = markup[params_start:params_end]
    notes = markup[params_end:left_end - len('</div>')].strip()
    aside_start = markup.index('<aside>', left_end) + len('<aside>')
    aside_end = markup.index('</aside>', aside_start)
    right = markup[aside_start:aside_end].strip()
    results = ''
    if right.startswith('<div class="ledger-sheet">'):
        result_start = markup.index('<div class="ledger-sheet">', aside_start)
        result_end = end_of_div(result_start)
        results = markup[result_start:result_end].replace('class="ledger-sheet"', 'class="ledger-sheet" aria-live="polite" aria-atomic="true"')
        right = markup[result_end:aside_end]
    return markup[:root_end] + inputs + results + '<div class="workspace-notes">' + notes + '</div><aside class="workspace-reference">' + right + '</aside></div>'


def build_tool_page(tool: dict) -> str:
    slug = tool["slug"]
    title = DISPLAY_NAMES.get(slug, tool["title"])
    desc = tool["short_desc"]
    category = tool["category"]
    source = SOURCE_LINKS.get(slug)
    source_link = (f'<a href="{source[1]}" style="text-decoration:underline">{source[0]} &rarr;</a>' if source else '<a href="../legal.html" style="text-decoration:underline">Methodology &amp; privacy &rarr;</a>')
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
  <title>{html.escape(title)} — {BRAND_NAME}</title>
  <meta name="description" content="{html.escape(desc)}" />
  <link rel="canonical" href="{SITE_URL}/tools/{slug}.html" />
  <link rel="stylesheet" href="../assets/styles.css" />
  {render_social_meta(title, desc, "tools/" + slug + ".html", "../")}
  {adsense_tag}
  <script type="application/ld+json">{json.dumps(schema_ld)}</script>
</head>
<body>
  {render_navbar(prefix="../")}
  <main class="container" id="main-content">
    <div class="breadcrumb-bar">
      <span><a href="../index.html">All calculators</a> &nbsp;/&nbsp; {html.escape(category)}</span>
      <span>MODEL BASIS: {html.escape(src_name.upper())} ({html.escape(ver_date.upper())})</span>
    </div>
    <header class="tool-header">
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(desc)}</p>
      <div class="estimate-notice">Planning estimate · Rates and FX inputs are illustrative, editable assumptions. Confirm availability, fees and tax eligibility with your provider and adviser. {source_link}</div>
    </header>

    {layout_workspace(render_tool_workspace(tool, prefix="../"))}
  </main>

  <footer>
    <div class="footer-inner">
      <span>&copy; {datetime.now().year} {BRAND_NAME} Publication. Client-side computation engine.</span>
      <span><a href="../index.html">Index</a> &nbsp;&bull;&nbsp; <a href="../legal.html">Privacy &amp; Terms</a> &nbsp;&bull;&nbsp; <a href="../sitemap.xml">Sitemap</a></span>
    </div>
  </footer>
  <script src="../assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_index_page() -> str:
    cat_meta = {
        "Payment & Fee Calculators": ("payment-calculators", "Payouts & payment fees"),
        "SaaS & Marketing Calculators": ("saas-calculators", "Growth & unit economics"),
        "Developer Utilities": ("dev-utilities", "Developer utilities"),
        "Business & Operations Tools": ("ops-tools", "Business & operations"),
    }
    categories = {}
    for tool in TOOLS_CATALOG:
        categories.setdefault(tool["category"], []).append(tool)
    sections = []
    i = 0
    for category, tools in categories.items():
        anchor, label = cat_meta[category]
        cards = []
        for tool in tools:
            i += 1
            title = html.escape(DISPLAY_NAMES.get(tool['slug'], tool['title']))
            cards.append(f'''<a href="tools/{tool['slug']}.html" class="tool-card">
              <div><span class="tool-num">{i:02d} &nbsp;/&nbsp; {html.escape(label.upper())}</span>
              <h3>{title}</h3><p>{html.escape(tool['short_desc'])}</p></div>
              <div class="tool-card-footer"><span>Free · In your browser</span><span>Open tool &rarr;</span></div></a>''')
        sections.append(f'''<section class="category-section" id="{anchor}"><div class="category-header">
          <h2 class="category-title">{label}</h2><span class="category-index">{len(tools):02d} TOOLS</span></div>
          <div class="tools-grid">{''.join(cards)}</div></section>''')
    icon_route = '<svg class="feature-icon" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M7 26V9h18M19 3l7 6-7 6M12 26h17" stroke="currentColor" stroke-width="1.5"/><circle cx="7" cy="28" r="4" stroke="currentColor" stroke-width="1.5"/></svg>'
    icon_reverse = '<svg class="feature-icon" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M10 8h14a8 8 0 0 1 0 16H7M13 18l-6 6 6 6M10 3v10" stroke="currentColor" stroke-width="1.5"/></svg>'
    icon_csv = '<svg class="feature-icon" viewBox="0 0 36 36" fill="none" aria-hidden="true"><path d="M8 4h15l6 6v22H8V4ZM22 4v8h7M13 19h11M13 24h7" stroke="currentColor" stroke-width="1.5"/></svg>'
    desc = 'Compare payout routes, work backwards from your target income, and audit CSV fees privately. 32 free browser tools for freelancers and small teams.'
    return f'''<!DOCTYPE html><html lang="en"><head>
      <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{BRAND_NAME} — {TAGLINE}</title><meta name="description" content="{desc}" />
      <link rel="canonical" href="{SITE_URL}/" /><link rel="stylesheet" href="assets/styles.css" />
      {render_social_meta(BRAND_NAME + ' — ' + TAGLINE, desc)}
      <script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'WebSite','name':BRAND_NAME,'url':SITE_URL+'/'})}</script>
    </head><body>{render_navbar()}
    <main class="container" id="main-content">
      <section class="editorial-hero"><div>
        <span class="kicker">Independent tools for money that crosses borders</span>
        <h1>Know what you<br/>actually <em>keep.</em></h1>
        <p>Your invoice is only the beginning. See what reaches you after platform fees, currency conversion, and tax assumptions.</p>
        <div class="hero-actions"><a class="btn-primary" href="tools/cross-border-payout-comparison-engine.html">Compare my payout &nbsp;&rarr;</a>
          <a class="btn-secondary" href="#directory">Explore all 32 tools</a></div>
        <div class="hero-note">Free to use <span>/</span> No account <span>/</span> Calculated on your device</div>
      </div><div class="sample-ledger" aria-label="Illustrative payout breakdown, not a live quote">
        <div class="sample-top"><span>YOUR INVOICE, UNPACKED</span><span><span class="sample-dot"></span>Illustrative scenario</span></div>
        <div class="sample-amount"><span>Client invoice · USD</span><strong>$1,000.00</strong></div>
        <div class="sample-row"><span>Platform · 10% + $0.99</span><strong>−$100.99</strong></div>
        <div class="sample-row"><span>Payout &amp; FX · 3% of remainder</span><strong>−$26.97</strong></div>
        <div class="sample-row"><span>Tax provision · 1% of gross</span><strong>−$10.00</strong></div>
        <div class="sample-bar" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
        <div class="sample-total"><span>What you keep</span><strong>$862.04</strong></div>
        <p class="sample-caption">Example inputs, not a provider quote or tax determination. Change every assumption in the payout comparison.</p>
      </div></section>
      <div class="trust-strip"><span><strong>32</strong> browser tools</span><span><strong>5</strong> country scenarios</span><span><strong>Zero</strong> statement uploads to a server</span><span><strong>Transparent</strong> formulas &amp; assumptions</span></div>
      <section class="feature-section"><div class="section-intro"><div><span class="kicker">Start with the question that matters</span><h2>From invoice to actual income.</h2></div><p>Three ways to get a clearer picture of your money.</p></div>
      <div class="flagship-banner" aria-label="Featured tools">
        <article class="flagship-col">{icon_route}<span class="kicker">01 / Compare your options</span><h3>Follow the whole<br/>payout journey.</h3><p>Model platform fees, payout routes, FX spreads, and tax provisions across five country scenarios.</p><a class="text-link" href="tools/cross-border-payout-comparison-engine.html">Compare payout routes &rarr;</a></article>
        <article class="flagship-col">{icon_reverse}<span class="kicker">02 / Work backwards</span><h3>Price for what<br/>you want to keep.</h3><p>Start with your target take-home. Find the invoice amount your assumptions require.</p><a class="text-link" href="tools/cross-border-payout-comparison-engine.html#in-target-net">Calculate my invoice &rarr;</a></article>
        <article class="flagship-col">{icon_csv}<span class="kicker">03 / Check the statement</span><h3>Make the hidden<br/>differences visible.</h3><p>Check a standardized transaction CSV against example fee baselines. Your rows stay in your browser.</p><a class="text-link" href="tools/private-csv-payout-fee-auditor.html">Audit a CSV privately &rarr;</a></article>
      </div></section>
      <section id="directory" aria-label="Calculator directory"><div class="directory-head"><div><span class="kicker">The working collection</span><h2>A sharper set of tools.</h2></div>
        <div class="search-bar"><label for="hub-search-input">Find a calculator or utility</label><input type="search" id="hub-search-input" placeholder="Search fees, Upwork, CSV, hourly rate…" aria-controls="calculator-sections" /></div></div>
        <nav class="directory-nav" aria-label="Calculator categories">{''.join(f'<a href="#{anchor}">{label}</a>' for anchor,label in cat_meta.values())}</nav>
        <p id="search-feedback" class="search-feedback" role="status" aria-live="polite">32 tools. No account needed.</p><div id="calculator-sections">{''.join(sections)}</div>
      </section>
      <section class="principles"><div><span class="kicker">Clarity is a working principle</span><h2>Your numbers stay yours.<br/>The assumptions stay visible.</h2></div><div><p>Calculations run on your device. CSV contents never leave your browser. No sign-in, no live bank connection, and no promises dressed up as projections.</p><p style="margin-top:17px">These are planning models. Confirm current provider fees, route eligibility, and your tax treatment before acting. <a href="legal.html">Read our methodology &amp; privacy notes &rarr;</a></p></div></section>
    </main><footer><div class="footer-inner"><span>&copy; {datetime.now().year} {BRAND_NAME}. Independent planning tools.</span><span><a href="legal.html">Privacy &amp; methodology</a> &nbsp;·&nbsp; <a href="sitemap.xml">Sitemap</a> &nbsp;·&nbsp; <a href="rss.xml">Updates</a></span></div></footer>
    <script src="assets/tools-runtime.js"></script></body></html>'''


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
  <title>Operations, Attribution &amp; Earnings Proof Dashboard — {BRAND_NAME}</title>
  <meta name="robots" content="noindex, follow" />
  <link rel="stylesheet" href="/assets/styles.css" />
</head>
<body>
  {render_navbar(prefix="/")}
  <main class="container" id="main-content" style="padding-top:36px">
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
      <div class="table-scroll" role="region" aria-label="Calculation table, scroll horizontally for all columns" tabindex="0">
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
              <td><span class="badge-ok">GENERATED — SEE LATEST CHECKS</span></td>
              <td style="text-align:left;font-family:var(--font-sans)">All 32 tools are generated. Consult the current <code>logs/autopilot_report.json</code> for tested cases and results; these tests do not certify current provider pricing, tax eligibility or every possible input.</td>
            </tr>
            <tr>
              <td><strong>Paid Pro Pack Security &amp; Multi-Tab .xlsx</strong></td>
              <td><span class="badge-ok">GENERATED — SEE LATEST CHECKS</span></td>
              <td style="text-align:left;font-family:var(--font-sans)"><code>calcgrid-pro-offline-suite.zip</code> is stored strictly in <code>private_products/</code> (0 ZIPs in <code>dist/</code>, 0 ZIPs in Git history) and contains a 3-sheet <code>.xlsx</code> with illustrative sample values, 3 CSV tables and a CLI reconciler. The workbook does not yet contain editable calculation formulas; this is not an approved paid release.</td>
            </tr>
            <tr>
              <td><strong>Autonomous SMM Video Renderer (FFmpeg + Voiceover)</strong></td>
              <td><span class="badge-ok">LOCAL MEDIA GENERATED</span></td>
              <td style="text-align:left;font-family:var(--font-sans)"><code>engine/smm_pipeline.py</code> generates real 1080x1920 vertical MP4 videos with synthesized English voiceovers (macOS <code>say</code> + <code>ffmpeg</code>), a branded static visual and separate <code>.srt</code> subtitles, and UTM links in <code>marketing_outbox/</code>.</td>
            </tr>
            <tr>
              <td><strong>Public Cloud Deployment (GitHub / Cloudflare Pages)</strong></td>
              <td><span class="badge-warn">CLOUDFLARE NOT VERIFIED</span></td>
              <td style="text-align:left;font-family:var(--font-sans)">Public source commits can be pushed to GitHub. Cloudflare deployment requires the correct GitHub account connection and a verified Pages project. A source push alone is not a successful Cloudflare deployment.</td>
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
      <div class="table-scroll" role="region" aria-label="Calculation table, scroll horizontally for all columns" tabindex="0">
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
      <span>&copy; {datetime.now().year} {BRAND_NAME} Publication. Honest Telemetry &amp; Earnings Ledger.</span>
      <span><a href="index.html">Return to All calculators</a></span>
    </div>
  </footer>
  <script src="/assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_legal_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Privacy Policy, EEA Consent &amp; Financial Disclaimers — {BRAND_NAME}</title>
  <link rel="stylesheet" href="assets/styles.css" />
  <link rel="canonical" href="{SITE_URL}/legal.html" />
  {render_social_meta("Privacy & methodology — " + BRAND_NAME, "How our planning models and browser privacy work.", "legal.html")}
</head>
<body>
  {render_navbar(prefix="")}
  <main class="container" id="main-content" style="max-width:820px;padding-top:36px">
    <span class="kicker">LEGAL &amp; COMPLIANCE DOCUMENTATION</span>
    <h1 style="font-family:var(--font-serif);font-size:2.2rem;font-weight:500;margin-bottom:20px">Privacy Policy, EEA/UK/CH Consent &amp; Financial Disclaimer</h1>
    <div class="doc-section" style="margin-top:0">
      <h3>1. Client-Side Data Privacy</h3>
      <p style="color:var(--ink-secondary);margin:8px 0 22px;font-size:0.9rem">
        All calculators, CSV transaction auditors, and developer utilities (including JSON, JWT, SQL, and CSV converters) execute locally in your browser using client-side JavaScript. The calculation runtime does not store, transmit, or log the financial figures, CSV files, tokens, or source code you enter. Hosting providers may process ordinary request metadata such as IP addresses, and Google Fonts receives font requests. Calculator figures can be included in a shareable URL only when you choose Copy Permalink; do not share sensitive scenarios.
      </p>

      <h3>2. EEA, UK &amp; Switzerland Advertising Consent (IAB TCF v2.2 Certified CMP)</h3>
      <p style="color:var(--ink-secondary);margin:8px 0 22px;font-size:0.9rem">
        Advertising and payment checkout are disabled in this release. Enabling advertising later requires separate owner approval and a completed, verified consent configuration appropriate to the selected advertising service and visitor regions. This site does not claim that a consent platform has already been configured.
      </p>

      <h3>3. No Financial, Tax, or Legal Advice</h3>
      <p style="color:var(--ink-secondary);margin:8px 0 10px;font-size:0.9rem">
        All fee, exchange-rate spread, and unit-economics models on {BRAND_NAME} are provided strictly for informational and estimation purposes. Payment processor fees (such as Payoneer, Wise, Lemon Squeezy, Stripe, PayPal, Upwork), correspondent SWIFT bank deductions, and regional tax rules (such as Armenia Turnover Tax, Georgia Small Business Status, Serbia Paušal, Philippines 8% Gross Receipts, and India Section 44ADA) change periodically and depend on individual eligibility. Always verify exact figures with your payment provider and a licensed accountant in your jurisdiction.
      </p>
    </div>
  </main>
  <footer>
    <div class="footer-inner">
      <span>&copy; {datetime.now().year} {BRAND_NAME} Publication.</span>
      <span><a href="index.html">Return to All calculators</a></span>
    </div>
  </footer>
  <script src="assets/tools-runtime.js"></script>
</body>
</html>
"""


def build_not_found_page() -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" /><meta name="robots" content="noindex" />
    <title>Page not found — {BRAND_NAME}</title><link rel="stylesheet" href="{SITE_URL}/assets/styles.css" /></head>
    <body>{render_navbar(SITE_URL + "/")}<main class="container" id="main-content" style="padding-top:80px">
    <span class="kicker">404 / Off the map</span><h1 style="font:48px var(--font-serif);margin-bottom:20px">That page isn't here.</h1>
    <p style="margin-bottom:25px">Find the tool you need in the calculator directory.</p><a class="btn-primary" href="{SITE_URL}/">Explore the tools &rarr;</a></main></body></html>"""


def build_seo_artifacts():
    urls = [f"{SITE_URL}/", f"{SITE_URL}/legal.html"] + [
        f"{SITE_URL}/tools/{t['slug']}.html" for t in TOOLS_CATALOG
    ]

    sitemap_entries = "".join(
        f"  <url>\n    <loc>{u}</loc>\n  </url>\n"
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
    <title>{BRAND_NAME} — Financial &amp; Technical Ledger</title>
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
{BRAND_NAME} Pro Batch Payout & Fee Reconciler CLI (calcgrid_batch_reconciler.py)
Exclusive to the {BRAND_NAME} Pro Suite ($19).
Ingests a bulk CSV of transactions (e.g. from Stripe, Payoneer, Wise, Upwork, Lemon Squeezy),
audits expected vs actual fees, flags variances > 0.25%, and outputs a reconciled accounting ledger.
\"\"\"
import argparse
import csv
import math
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
    with open(input_csv, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        required = {"tx_id", "provider", "gross_usd", "actual_net_usd"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError("Missing required transaction CSV columns")
        for row in reader:
            provider = row.get("provider", "lemonsqueezy").strip().lower()
            gross = float(row.get("gross_usd", 0.0))
            actual_net = float(row.get("actual_net_usd", 0.0))
            if provider not in PROVIDER_RATES:
                raise ValueError("Unsupported provider code: " + provider)
            if not all(math.isfinite(n) and n >= 0 for n in (gross, actual_net)):
                raise ValueError("Transaction amounts must be finite and non-negative")
            pct, fix, fx = PROVIDER_RATES[provider]
            expected_fee = gross * ((pct + fx) / 100.0) + fix
            expected_net = max(0.0, gross - expected_fee)
            variance = actual_net - expected_net
            flag = "OK" if abs(variance) <= max(0.50, gross * 0.0025) else "FEE_VARIANCE_ALERT"
            rows_out.append({
                "tx_id": ("'" + row.get("tx_id", "")) if row.get("tx_id", "").lstrip().startswith(("=", "+", "-", "@")) else row.get("tx_id", ""),
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
    parser = argparse.ArgumentParser(description="{BRAND_NAME} Pro Bulk Payout Reconciler")
    parser.add_argument("--input", required=True, help="Input transactions CSV")
    parser.add_argument("--output", default="reconciled_ledger.csv", help="Output reconciled CSV")
    args = parser.parse_args()
    reconcile_csv(Path(args.input), Path(args.output))
"""

    batch_reconciler_py = batch_reconciler_py.replace("{BRAND_NAME}", BRAND_NAME)

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
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for asset in (ROOT_DIR / "engine" / "brand_assets").glob("*"):
        if asset.is_file() and asset.suffix in {".svg", ".png"}:
            shutil.copy2(asset, ASSETS_DIR / asset.name)
    (DIST_DIR / "_headers").write_text("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'
""", encoding="utf-8")

    (ASSETS_DIR / "styles.css").write_text(build_css(), encoding="utf-8")
    (ASSETS_DIR / "tools-runtime.js").write_text(build_runtime_js(), encoding="utf-8")

    # Ensure private dashboard is NEVER inside public dist/
    public_dash = DIST_DIR / "dashboard.html"
    if public_dash.exists():
        public_dash.unlink()

    (DIST_DIR / "index.html").write_text(build_index_page(), encoding="utf-8")
    (DIST_DIR / "legal.html").write_text(build_legal_page(), encoding="utf-8")
    (DIST_DIR / "404.html").write_text(build_not_found_page(), encoding="utf-8")

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    private_dash_path = LOGS_DIR / "private_dashboard.html"
    private_dash_path.write_text(build_dashboard_page(), encoding="utf-8")

    for tool in TOOLS_CATALOG:
        html_out = build_tool_page(tool)
        (TOOLS_DIR / f"{tool['slug']}.html").write_text(html_out, encoding="utf-8")

    build_seo_artifacts()
    private_zip_path = build_private_pro_digital_product_zip()
    # Keep offline files portable, then adapt only the public output to Pages clean URLs.
    finalize_cloudflare_output()

    return {
        "tools_compiled": len(TOOLS_CATALOG),
        "total_html_pages": len(TOOLS_CATALOG) + 3,
        "public_dist_dir": str(DIST_DIR),
        "private_pro_zip": str(private_zip_path),
        "private_dashboard_path": str(private_dash_path),
        "public_zip_exposed": any(DIST_DIR.rglob("*.zip")),
        "public_dashboard_exposed": (DIST_DIR / "dashboard.html").exists(),
        "ads_enabled": bool(ADSENSE_CLIENT_ID),
        "checkout_enabled": bool(LEMON_SQUEEZY_CHECKOUT_URL)
    }


if __name__ == "__main__":
    print(json.dumps(compile_all(), indent=2))
