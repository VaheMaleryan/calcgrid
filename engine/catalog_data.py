#!/usr/bin/env python3
"""
Master Catalog of 32 Interactive Client-Side Calculators, Flagship Payout Engines & Developer Utilities.
Includes:
  - COMPETITOR_BENCHMARK_MATRIX: Research on 10 competing calculator sites and underserved gaps
  - COUNTRY_CORRIDORS: Source-verified cross-border payout availability, fee ranges, and simplified tax presets
    for Armenia, Georgia, Serbia, Philippines, and India (no fabricated live FX rates)
  - TOOLS_CATALOG: 2 Flagship Interactive Engines ('corridor_engine', 'csv_auditor') + 30 Core Calculators
"""

COMPETITOR_BENCHMARK_MATRIX = [
    {
        "rank": 1,
        "name": "FeeProbe (feeprobe.com)",
        "strengths": "Clean UI, side-by-side Stripe/PayPal/Wise comparison for US/UK, basic reverse fee calculation.",
        "underserved_gaps": "Ignores multi-stage freelance chains (e.g., Upwork -> Payoneer -> Local Bank), no emerging-market corridor restrictions (e.g., Wise receiving limits in Armenia), no local turnover tax, no CSV batch auditing."
    },
    {
        "rank": 2,
        "name": "Teamz Lab Payment Processor Fee Calculator",
        "strengths": "Covers PayPal, Stripe, Wise Business, Payoneer, Bank Wire, and Revolut with currency options.",
        "underserved_gaps": "Models single-hop transfers only; does not combine marketplace commission + payout rail FX spread + local tax into a reverse invoice solver; no browser CSV statement auditor."
    },
    {
        "rank": 3,
        "name": "Baznek Platform & Fee Comparison Center",
        "strengths": "Pairwise comparisons (Wise vs Payoneer, Upwork vs Fiverr, Stripe vs PayPal).",
        "underserved_gaps": "Lacks country-specific rail availability warnings, SWIFT intermediary bank uncertainty ranges ($10-$30 mid-route deductions), and multi-stage target-net invoice math."
    },
    {
        "rank": 4,
        "name": "HelloFees (hellofees.com)",
        "strengths": "Compares Stripe, PayPal, Square, and Shopify Payments across 60+ countries for e-commerce.",
        "underserved_gaps": "Built for e-commerce checkout only; omits Upwork/Fiverr/Lemon Squeezy MoR payouts and emerging-market IE tax regimes (Armenia 1% IT, Georgia 1% SBS)."
    },
    {
        "rank": 5,
        "name": "Calcimator Payment Gateway Calculator",
        "strengths": "Highlights forex conversion markups on Stripe, PayPal, Adyen, and Braintree.",
        "underserved_gaps": "Single-transaction only; no sensitivity matrix across volume tiers and no CSV reconciliation."
    },
    {
        "rank": 6,
        "name": "GetInvoicePDF Payment Fee Calculator",
        "strengths": "Simple invoice gross-up calculator for Stripe and PayPal.",
        "underserved_gaps": "No cross-border payout rails (Payoneer/Wise/SWIFT), no uncertainty bands, and no multi-hop deduction modeling."
    },
    {
        "rank": 7,
        "name": "QuadraPay Payment Gateway Cost Calculator",
        "strengths": "Calculates effective monthly merchant rate across card volume and per-transaction fees.",
        "underserved_gaps": "Targets traditional retail card processing; lacks freelancer marketplace and Merchant-of-Record fee structures."
    },
    {
        "rank": 8,
        "name": "DepositFix Payment Gateways Calculator",
        "strengths": "Useful for B2B HubSpot/Stripe checkout cost estimation.",
        "underserved_gaps": "No international contractor payout routing or FX spread auditing."
    },
    {
        "rank": 9,
        "name": "Payoneer Native Fee & Checkout Calculator",
        "strengths": "First-party Payoneer volume calculator.",
        "underserved_gaps": "Marketing tool that omits side-by-side comparison against Wise mid-market rates or Upwork Direct Contracts."
    },
    {
        "rank": 10,
        "name": "Wise Native Pricing & Corridor Estimator",
        "strengths": "Accurate single-transfer Wise route fees.",
        "underserved_gaps": "Does not integrate upstream marketplace commissions (Upwork 0%-15%, Fiverr 20%, Lemon Squeezy 5%+$0.50) or downstream local entrepreneur taxes."
    }
]

COUNTRY_CORRIDORS = {
    "AM": {
        "name": "Armenia",
        "currency": "AMD",
        "default_fx_placeholder": 388.0,
        "fx_note": "User-editable reference rate (AMD per 1 USD). Enter your bank or CBA rate; CalcGrid never fabricates live FX feeds.",
        "verified_date": "2026-10-27",
        "official_sources": "RA Tax Code (Turnover Tax & High-Tech Registry), Payoneer Pricing Schedule, Wise Country Availability Docs, Lemon Squeezy MoR Payouts",
        "rails": {
            "payoneer": {
                "available": True,
                "status_badge": "SUPPORTED & WIDELY USED",
                "pct_fee": 1.0,
                "fixed_fee": 0.0,
                "fx_spread_expected": 2.0,
                "fx_spread_min": 1.5,
                "fx_spread_max": 3.0,
                "intermediary_min": 0.0,
                "intermediary_max": 0.0,
                "note": "Direct withdrawals to Armenian banks (Ameriabank, Inecobank, Ardshinbank, etc.) or Payoneer card. Typical local currency withdrawal markup is ~2% (range 1.5%–3.0%). Annual fee $29.95 applies if annual volume < $6,000."
            },
            "wise": {
                "available": False,
                "status_badge": "RECEIVING RESTRICTED FOR RESIDENTS",
                "pct_fee": 0.65,
                "fixed_fee": 4.14,
                "fx_spread_expected": 0.0,
                "fx_spread_min": 0.0,
                "fx_spread_max": 0.5,
                "intermediary_min": 0.0,
                "intermediary_max": 15.0,
                "note": "Wise does not currently issue local USD/EUR receiving account details to residents of Armenia. Incoming direct transfers from foreign clients must typically route via SWIFT/Payoneer unless using an eligible foreign entity."
            },
            "swift": {
                "available": True,
                "status_badge": "SUPPORTED (HIGH FIXED & INTERMEDIARY FEES)",
                "pct_fee": 0.2,
                "fixed_fee": 25.0,
                "fx_spread_expected": 1.2,
                "fx_spread_min": 0.8,
                "fx_spread_max": 2.0,
                "intermediary_min": 10.0,
                "intermediary_max": 35.0,
                "note": "Supported by all Armenian banks; requires formal invoice/contract for compliance. Correspondent intermediary banks typically deduct $10–$35 mid-route."
            },
            "lemonsqueezy": {
                "available": True,
                "status_badge": "SUPPORTED (MERCHANT OF RECORD WIRE)",
                "pct_fee": 5.0,
                "fixed_fee": 0.50,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.5,
                "fx_spread_max": 2.5,
                "intermediary_min": 0.0,
                "intermediary_max": 15.0,
                "note": "Official Merchant of Record for SaaS & digital products; handles global VAT/GST and supports international wire payouts to Armenia ($50 minimum payout)."
            }
        },
        "tax_presets": [
            {"label": "1.0% — Qualifying High-Tech / IT Turnover Tax (Gross Base per Art. 257, Eligibility Required)", "rate": 1.0},
            {"label": "0.0% — Eligible Micro-Business (<24M AMD/yr, Activity Restrictions Apply)", "rate": 0.0},
            {"label": "10.0% — General Turnover Tax Reference Example (Gross Base)", "rate": 10.0}
        ],
        "tax_caveat": "Per Article 257 of the Republic of Armenia Tax Code, turnover tax is assessed on full GROSS sales turnover (the gross invoice billed to the client, BEFORE deducting marketplace or payment withdrawal fees). Both the 1% high-tech rate (up to 115M AMD cap) and the 0% micro-business regime (under 24M AMD cap) apply strictly to qualifying activities and eligible taxpayers; many professional/consulting services are excluded. Confirm your eligibility with a licensed Armenian accountant."
    },
    "GE": {
        "name": "Georgia",
        "currency": "GEL",
        "default_fx_placeholder": 2.72,
        "fx_note": "User-editable reference rate (GEL per 1 USD). Enter your NBG or bank rate.",
        "verified_date": "2026-10-27",
        "official_sources": "Revenue Service of Georgia (rs.ge Small Business Status), Wise Georgia Pricing, Payoneer Pricing Schedule",
        "rails": {
            "payoneer": {
                "available": True,
                "status_badge": "SUPPORTED (TBC & BOG INTEGRATED)",
                "pct_fee": 1.0,
                "fixed_fee": 0.0,
                "fx_spread_expected": 2.0,
                "fx_spread_min": 1.8,
                "fx_spread_max": 3.0,
                "intermediary_min": 0.0,
                "intermediary_max": 0.0,
                "note": "Widely integrated with TBC Bank and Bank of Georgia; local withdrawal to GEL carries ~2%–3% conversion markup."
            },
            "wise": {
                "available": True,
                "status_badge": "SUPPORTED (MID-MARKET FX)",
                "pct_fee": 0.65,
                "fixed_fee": 4.14,
                "fx_spread_expected": 0.0,
                "fx_spread_min": 0.0,
                "fx_spread_max": 0.3,
                "intermediary_min": 0.0,
                "intermediary_max": 5.0,
                "note": "Georgian residents can open multi-currency Wise accounts and convert at the mid-market rate with transparent route fees."
            },
            "swift": {
                "available": True,
                "status_badge": "SUPPORTED (INTERMEDIARY DEDUCTIONS)",
                "pct_fee": 0.2,
                "fixed_fee": 20.0,
                "fx_spread_expected": 1.2,
                "fx_spread_min": 0.8,
                "fx_spread_max": 2.0,
                "intermediary_min": 10.0,
                "intermediary_max": 30.0,
                "note": "Direct wire to TBC or Bank of Georgia; intermediary correspondent fees ($10–$30) apply unless sent OUR."
            },
            "lemonsqueezy": {
                "available": True,
                "status_badge": "SUPPORTED (MOR BANK PAYOUT)",
                "pct_fee": 5.0,
                "fixed_fee": 0.50,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.5,
                "fx_spread_max": 2.5,
                "intermediary_min": 0.0,
                "intermediary_max": 10.0,
                "note": "Supports digital product and SaaS payouts to Georgian bank accounts."
            }
        },
        "tax_presets": [
            {"label": "1.0% — IE Small Business Status (up to 500,000 GEL/yr)", "rate": 1.0},
            {"label": "3.0% — IE Small Business Status (Turnover above 500,000 GEL)", "rate": 3.0},
            {"label": "0.0% — Pre-Tax Payout Comparison", "rate": 0.0}
        ],
        "tax_caveat": "Georgia's Individual Entrepreneur Small Business Status taxes gross turnover at 1% up to 500,000 GEL/year (3% above cap). Certain consulting, legal, accounting, and medical services are excluded from the 1% regime."
    },
    "RS": {
        "name": "Serbia",
        "currency": "RSD",
        "default_fx_placeholder": 108.5,
        "fx_note": "User-editable reference rate (RSD per 1 USD). Enter your NBS middle exchange rate.",
        "verified_date": "2026-10-27",
        "official_sources": "Tax Administration of Serbia (purs.gov.rs Paušal Rules), National Bank of Serbia, Wise & Payoneer Schedules",
        "rails": {
            "payoneer": {
                "available": True,
                "status_badge": "SUPPORTED",
                "pct_fee": 1.0,
                "fixed_fee": 0.0,
                "fx_spread_expected": 2.0,
                "fx_spread_min": 1.8,
                "fx_spread_max": 3.0,
                "intermediary_min": 0.0,
                "intermediary_max": 0.0,
                "note": "Popular among Serbian marketplace freelancers; ~2%–3% conversion spread when withdrawing to RSD."
            },
            "wise": {
                "available": True,
                "status_badge": "SUPPORTED (MID-MARKET FX)",
                "pct_fee": 0.65,
                "fixed_fee": 4.14,
                "fx_spread_expected": 0.0,
                "fx_spread_min": 0.0,
                "fx_spread_max": 0.3,
                "intermediary_min": 0.0,
                "intermediary_max": 5.0,
                "note": "Operational for Serbian residents with mid-market rate conversion and transparent route fees."
            },
            "swift": {
                "available": True,
                "status_badge": "SUPPORTED (REQUIRES LOR / INFLOW BASIS)",
                "pct_fee": 0.3,
                "fixed_fee": 20.0,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.0,
                "fx_spread_max": 2.5,
                "intermediary_min": 10.0,
                "intermediary_max": 30.0,
                "note": "Requires foreign inflow basis declaration (šifra osnova priliva) with local Serbian banks."
            },
            "lemonsqueezy": {
                "available": True,
                "status_badge": "SUPPORTED (MOR WIRE PAYOUT)",
                "pct_fee": 5.0,
                "fixed_fee": 0.50,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.5,
                "fx_spread_max": 2.5,
                "intermediary_min": 0.0,
                "intermediary_max": 15.0,
                "note": "Merchant of Record payouts for software and digital products."
            }
        },
        "tax_presets": [
            {"label": "10.0% — Illustrative Effective Paušal Reserve (up to 6M RSD cap)", "rate": 10.0},
            {"label": "0.0% — Pre-Tax Payout Comparison", "rate": 0.0},
            {"label": "15.0% — Conservative Tax & Social Reserve Example", "rate": 15.0}
        ],
        "tax_caveat": "Serbia's Preduzetnik Paušalac regime charges a fixed monthly RSD amount (determined by municipality and activity code, up to 6,000,000 RSD annual turnover) rather than a flat percentage, and requires passing the 9-criteria Independence Test (test samostalnosti)."
    },
    "PH": {
        "name": "Philippines",
        "currency": "PHP",
        "default_fx_placeholder": 58.2,
        "fx_note": "User-editable reference rate (PHP per 1 USD). Enter your BSP or bank rate.",
        "verified_date": "2026-10-27",
        "official_sources": "Bureau of Internal Revenue (bir.gov.ph 8% Gross Receipts Option), Wise Philippines, Payoneer Philippines",
        "rails": {
            "payoneer": {
                "available": True,
                "status_badge": "SUPPORTED (GCASH & LOCAL BANKS)",
                "pct_fee": 1.0,
                "fixed_fee": 0.0,
                "fx_spread_expected": 2.0,
                "fx_spread_min": 1.8,
                "fx_spread_max": 3.0,
                "intermediary_min": 0.0,
                "intermediary_max": 0.0,
                "note": "Integrated with Upwork and GCash; ~2% conversion spread above mid-market rate."
            },
            "wise": {
                "available": True,
                "status_badge": "SUPPORTED (FAST PHP / GCASH / MAYA)",
                "pct_fee": 0.60,
                "fixed_fee": 3.50,
                "fx_spread_expected": 0.0,
                "fx_spread_min": 0.0,
                "fx_spread_max": 0.2,
                "intermediary_min": 0.0,
                "intermediary_max": 0.0,
                "note": "Full Wise account support in the Philippines with mid-market PHP conversion to local banks (BPI, BDO, UnionBank) and e-wallets."
            },
            "swift": {
                "available": True,
                "status_badge": "SUPPORTED (HIGH REMITTANCE FEES)",
                "pct_fee": 0.25,
                "fixed_fee": 25.0,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.0,
                "fx_spread_max": 2.5,
                "intermediary_min": 10.0,
                "intermediary_max": 30.0,
                "note": "Traditional SWIFT wires incur correspondent bank deductions and wider PHP conversion spreads."
            },
            "lemonsqueezy": {
                "available": True,
                "status_badge": "SUPPORTED (MOR PAYOUTS)",
                "pct_fee": 5.0,
                "fixed_fee": 0.50,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.5,
                "fx_spread_max": 2.5,
                "intermediary_min": 0.0,
                "intermediary_max": 10.0,
                "note": "Supports digital creator payouts to Philippine bank accounts."
            }
        },
        "tax_presets": [
            {"label": "8.0% — BIR 8% Gross Receipts Tax Option (Under PHP 3M VAT threshold)", "rate": 8.0},
            {"label": "0.0% — Pre-Tax Payout Comparison", "rate": 0.0}
        ],
        "tax_caveat": "Self-employed professionals in the Philippines earning under the PHP 3,000,000 VAT threshold can elect the 8% flat income tax rate on gross receipts in excess of PHP 250,000 under the TRAIN Law."
    },
    "IN": {
        "name": "India",
        "currency": "INR",
        "default_fx_placeholder": 84.1,
        "fx_note": "User-editable reference rate (INR per 1 USD). Enter your RBI reference or bank card rate.",
        "verified_date": "2026-10-27",
        "official_sources": "Income Tax Act Section 44ADA, RBI FEMA Export Purpose Code P0802, Wise India eFIRC Docs, Payoneer India FIRA Schedule",
        "rails": {
            "payoneer": {
                "available": True,
                "status_badge": "SUPPORTED (AUTO DIGITAL FIRA)",
                "pct_fee": 1.0,
                "fixed_fee": 0.0,
                "fx_spread_expected": 2.2,
                "fx_spread_min": 2.0,
                "fx_spread_max": 3.0,
                "intermediary_min": 0.0,
                "intermediary_max": 0.0,
                "note": "Provides automatic digital FIRA certificates for RBI/GST export compliance; total conversion + withdrawal cost is ~2.2%–3.0%."
            },
            "wise": {
                "available": True,
                "status_badge": "SUPPORTED (MID-MARKET + EFIRC FEE)",
                "pct_fee": 0.65,
                "fixed_fee": 2.50,
                "fx_spread_expected": 0.0,
                "fx_spread_min": 0.0,
                "fx_spread_max": 0.3,
                "intermediary_min": 0.0,
                "intermediary_max": 2.50,
                "note": "Uses mid-market INR exchange rate; automated digital eFIRC / FIRA certificate available for export compliance."
            },
            "swift": {
                "available": True,
                "status_badge": "SUPPORTED (PURPOSE CODE P0802)",
                "pct_fee": 0.15,
                "fixed_fee": 15.0,
                "fx_spread_expected": 1.8,
                "fx_spread_min": 1.0,
                "fx_spread_max": 2.5,
                "intermediary_min": 10.0,
                "intermediary_max": 25.0,
                "note": "Direct bank inward remittance (HDFC/ICICI/SBI) requires RBI Purpose Code (e.g., P0802 for software); bank FX spread varies unless negotiated."
            },
            "lemonsqueezy": {
                "available": True,
                "status_badge": "SUPPORTED (MOR WIRE PAYOUT)",
                "pct_fee": 5.0,
                "fixed_fee": 0.50,
                "fx_spread_expected": 1.5,
                "fx_spread_min": 1.5,
                "fx_spread_max": 2.5,
                "intermediary_min": 0.0,
                "intermediary_max": 15.0,
                "note": "Merchant of Record payouts for SaaS and digital products."
            }
        },
        "tax_presets": [
            {"label": "7.5% — Illustrative Effective Tax Provision (Sec 44ADA 50% Deemed Profit)", "rate": 7.5},
            {"label": "0.0% — Pre-Tax Payout Comparison", "rate": 0.0}
        ],
        "tax_caveat": "Under Section 44ADA Presumptive Taxation, eligible Indian professionals with gross receipts up to INR 75 Lakh (when >=95% of receipts are digital) declare 50% of gross receipts as taxable income, taxed at applicable individual slab rates. Export of services under GST LUT is zero-rated."
    }
}

TOOLS_CATALOG = [
    # =========================================================================
    # FLAGSHIP COMPETITIVE ADVANTAGE INSTRUMENTS (PRIORITY #1, #2, #3)
    # =========================================================================
    {
        "slug": "cross-border-payout-comparison-engine",
        "title": "Cross-Border Freelancer Payout, Reverse Invoice & Tax Comparison Engine",
        "category": "Payment & Fee Calculators",
        "short_desc": "Compare end-to-end net take-home pay and required reverse invoice amounts across Upwork, Direct Contracts, Fiverr, Payoneer, Wise, and SWIFT for Armenia, Georgia, Serbia, Philippines, and India.",
        "tool_type": "corridor_engine",
        "config": {
            "default_country": "AM",
            "default_amount": 1000,
            "default_origin_pct": 10.0,
            "default_origin_fixed": 0.99,
            "verified_date": "2026-10-27",
            "source_name": "Multi-Provider Corridor Schedule (Wise, Payoneer, Upwork, RA/GE/RS/PH/IN Tax Codes)"
        },
        "formula_explanation": "Stage 1 (Platform Deduction): After_Platform = Gross × (1 - Platform_Pct) - Platform_Fixed. Stage 2 (Payout Rail & FX Uncertainty Band): Net_USD = After_Platform × (1 - Rail_Pct - FX_Spread_[Min..Max]) - Rail_Fixed - Intermediary_[Min..Max]. Stage 3 (Gross Turnover Tax Base — e.g. RA Tax Code Art. 257): Turnover_Tax = Gross × Local_Tax_Pct; Final_Net = Net_USD - Turnover_Tax. Multi-Stage Reverse Invoice Solver: Required_Gross = (Target_Net + Platform_Fixed × (1 - Rail_Pct - FX_Spread) + Rail_Fixed + Intermediary) / ((1 - Platform_Pct) × (1 - Rail_Pct - FX_Spread) - Local_Tax_Pct).",
        "faqs": [
            ("Why is turnover tax calculated on the Gross Invoice rather than the post-fee payout?", "Under gross turnover tax regimes—such as Article 257 of Armenia's Tax Code or Georgia's Small Business Status—the tax base is your gross sales revenue (the full invoice amount billed to the client), without deducting marketplace commissions (like Upwork's 10%) or bank withdrawal fees. Subtracting tax only from the remaining post-fee payout understates your legal tax obligation."),
            ("Who qualifies for Armenia's 1% High-Tech rate or 0% Micro-Business regime?", "Both regimes have strict statutory eligibility requirements under the RA Tax Code. The 1% turnover tax rate applies only to qualifying high-tech/IT activities and eligible taxpayers (within the 115M AMD annual threshold), and the 0% micro-business regime (under 24M AMD) excludes several professional, consulting, and specialized service categories. Always confirm your activity classification with a certified accountant."),
            ("Does this calculator invent live exchange rates?", "Never. Exchange rates fluctuate every minute and banks apply custom spreads. We provide a user-editable Reference Exchange Rate field and calculate transparent Best-Case to Worst-Case Net Payout ranges so you can see the exact impact of FX markups and SWIFT intermediary fees.")
        ]
    },
    {
        "slug": "private-csv-payout-fee-auditor",
        "title": "Private Browser CSV Transaction & Hidden FX Fee Auditor",
        "category": "Payment & Fee Calculators",
        "short_desc": "Audit Stripe, Payoneer, Wise, Upwork, and Lemon Squeezy CSV payout statements 100% locally in your browser to detect hidden FX markups and fee variances.",
        "tool_type": "csv_auditor",
        "config": {
            "sample_csv": "tx_id,provider,gross_usd,actual_net_usd\nTX-1001,lemonsqueezy,49.00,45.32\nTX-1002,upwork_10,1200.00,1079.01\nTX-1003,payoneer,2500.00,2400.00\nTX-1004,wise,3000.00,2976.36\nTX-1005,stripe_intl,500.00,465.00",
            "verified_date": "2026-10-27",
            "source_name": "Published Provider Fee Schedules (Lemon Squeezy, Upwork, Payoneer, Wise, Stripe)"
        },
        "formula_explanation": "For each CSV transaction row: Expected_Fee = Gross_USD × ((Published_Base_Pct + Published_FX_Spread_Pct) / 100) + Published_Fixed_Fee. Expected_Net = Gross_USD - Expected_Fee. Fee_Leakage_Variance = Actual_Net_USD - Expected_Net. Rows with hidden fee leakage exceeding max($0.50, 0.25% of Gross) are flagged as FEE_VARIANCE_ALERT.",
        "faqs": [
            ("Are my financial CSV rows uploaded to any server?", "No. 100% of CSV parsing, fee variance math, and report generation runs inside your browser's local JavaScript memory. No transaction data ever leaves your device."),
            ("What does FEE_VARIANCE_ALERT mean on a Payoneer or Stripe row?", "It means the actual net settlement you received was lower than the provider's baseline fee schedule—typically caused by an undisclosed 2.5%–3.5% currency conversion spread, an international card surcharge (+1.5%), or an intermediary bank deduction.")
        ]
    },
    # =========================================================================
    # VERTICAL 1: CROSS-BORDER PAYOUT & FREELANCER FEE CALCULATORS
    # =========================================================================
    {
        "slug": "payoneer-fee-calculator",
        "title": "Payoneer Fee & Net Payout Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate exact Payoneer receiving fees, local bank withdrawal deductions, and FX conversion markup.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Gross Payment Amount ($ USD)",
            "default_amount": 1000,
            "percent_fee": 1.0,
            "fixed_fee": 0.0,
            "fx_markup_percent": 2.0,
            "label_pct": "Receiving Fee (%)",
            "label_fixed": "Fixed Bank Withdrawal Fee ($)",
            "label_fx": "Currency Conversion / Withdrawal Markup (%)"
        },
        "formula_explanation": "Net Payout = Gross Amount - (Gross × Receiving Fee %) - Fixed Fee - (Remaining × FX Conversion Markup %).",
        "faqs": [
            ("How much does Payoneer charge to withdraw to a local bank account?", "Payoneer typically charges up to 2% above the mid-market exchange rate when withdrawing to a local currency bank account, or a fixed fee (often $15) for USD wire withdrawals."),
            ("Are Payoneer-to-Payoneer transfers free?", "Receiving payments from another Payoneer customer balance is generally free, while receiving ACH bank debit payments in USD typically carries a 1% fee and credit card payments carry ~3%.")
        ]
    },
    {
        "slug": "wise-transfer-fee-calculator",
        "title": "Wise International Transfer & FX Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Estimate Wise (TransferWise) variable transfer percentage, fixed wire cost, and net recipient amount.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Transfer Send Amount ($ USD)",
            "default_amount": 1500,
            "percent_fee": 0.65,
            "fixed_fee": 4.14,
            "fx_markup_percent": 0.0,
            "label_pct": "Wise Variable Route Fee (%)",
            "label_fixed": "Fixed Wire / ACH Fee ($)",
            "label_fx": "Exchange Rate Spread (%) — Wise uses 0% mid-market"
        },
        "formula_explanation": "Net Converted Amount = Send Amount - Fixed Route Fee - (Send Amount × Variable Route Fee %).",
        "faqs": [
            ("Does Wise add a markup to the exchange rate?", "No. Wise uses the real mid-market exchange rate and charges an upfront transparent fixed + variable percentage fee depending on the currency corridor."),
            ("Why is there a fixed fee on USD SWIFT wires?", "International SWIFT transfers involve correspondent banks, which adds a small fixed rail fee compared to local ACH transfers.")
        ]
    },
    {
        "slug": "lemonsqueezy-fee-calculator",
        "title": "Lemon Squeezy Merchant of Record Fee Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate Lemon Squeezy 5% + $0.50 base MoR fees, international card surcharges, and payout transfer costs.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Digital Product / SaaS Price ($ USD)",
            "default_amount": 49,
            "percent_fee": 5.0,
            "fixed_fee": 0.50,
            "fx_markup_percent": 1.5,
            "label_pct": "Base Platform Fee (%)",
            "label_fixed": "Per-Transaction Fixed Fee ($)",
            "label_fx": "International / PayPal / Subscription Surcharge (%)"
        },
        "formula_explanation": "Net Earnings = Sale Price - (Sale Price × (Base 5% + Surcharge %)) - $0.50 Fixed Fee.",
        "faqs": [
            ("What does Lemon Squeezy's 5% + $0.50 fee cover?", "As a Merchant of Record (MoR), Lemon Squeezy handles payment processing, global VAT/GST calculation and remittance, fraud protection, and license key delivery."),
            ("Does Lemon Squeezy support bank payouts to Armenia and international countries?", "Yes, Lemon Squeezy supports direct bank payouts across 80+ countries including Armenia, with a small payout fee depending on the payout rail.")
        ]
    },
    {
        "slug": "gumroad-fee-calculator",
        "title": "Gumroad 10% + Processing Fee Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate Gumroad's 10% flat commission plus credit card processing fees and your net creator take-home pay.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Product Sale Price ($ USD)",
            "default_amount": 39,
            "percent_fee": 10.0,
            "fixed_fee": 0.80,
            "fx_markup_percent": 2.9,
            "label_pct": "Gumroad Flat Commission (%)",
            "label_fixed": "Fixed Per-Sale Fee ($0.50 + $0.30 card fee)",
            "label_fx": "Card Processing Fee (%)"
        },
        "formula_explanation": "Net Creator Revenue = Sale Price - (Sale Price × 10% Gumroad Fee) - $0.50 - (Sale Price × 2.9% + $0.30 Card Fee).",
        "faqs": [
            ("Did Gumroad become a Merchant of Record?", "Yes, Gumroad handles global tax collection on digital sales, charging a 10% + $0.50 platform fee plus standard payment processor fees."),
            ("How much do Gumroad Discover sales cost?", "Sales generated organically through Gumroad Discover carry a 30% total fee instead of the standard direct-link fee.")
        ]
    },
    {
        "slug": "paddle-fee-calculator",
        "title": "Paddle SaaS Checkout & MoR Fee Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate Paddle's 5% + $0.50 Merchant of Record fees and net recurring revenue for software products.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Subscription / Software Price ($ USD)",
            "default_amount": 79,
            "percent_fee": 5.0,
            "fixed_fee": 0.50,
            "fx_markup_percent": 0.0,
            "label_pct": "Paddle MoR Fee (%)",
            "label_fixed": "Fixed Checkout Fee ($)",
            "label_fx": "Optional FX Conversion Spread (%)"
        },
        "formula_explanation": "Net SaaS Revenue = Price - (Price × 5%) - $0.50.",
        "faqs": [
            ("Why do B2B SaaS founders use Paddle?", "Paddle acts as the legal reseller (Merchant of Record), handling global sales tax registration, invoicing, and compliance automatically."),
            ("Are credit card fees included in Paddle's 5% + $0.50?", "Yes, Visa, Mastercard, and PayPal processing costs are bundled into Paddle's standard 5% + $0.50 rate.")
        ]
    },
    {
        "slug": "upwork-freelancer-fee-calculator",
        "title": "Upwork Variable Freelancer Fee Calculator (0%–15%)",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate Upwork's variable 0% to 15% freelancer service fee, withdrawal costs, and exact gross bid required to reach your target net pay.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Client Contract / Milestone Amount ($ USD)",
            "default_amount": 1000,
            "percent_fee": 10.0,
            "fixed_fee": 0.99,
            "fx_markup_percent": 0.0,
            "label_pct": "Upwork Variable Freelancer Service Fee (0%–15%)",
            "label_fixed": "Withdrawal Fee ($0.99 ACH / $30 Wire)",
            "label_fx": "Optional Currency Conversion Markup (%)",
            "presets": [
                {"label": "0% (Direct Contract — Freelancer Plus)", "pct": 0.0},
                {"label": "5% (Direct Contract Standard / Example)", "pct": 5.0},
                {"label": "10% (Example Marketplace Rate)", "pct": 10.0},
                {"label": "15% (Example Marketplace Rate)", "pct": 15.0}
            ],
            "source_name": "Upwork Freelancer Service Fee & Direct Contracts Schedule",
            "verified_date": "October 2026"
        },
        "formula_explanation": "Freelancer Net Payout = Contract Amount × (1 - Contract Fee Rate [0% to 15%]) - Withdrawal Fee. Gross Bid Required = (Target Net + Withdrawal Fee) / (1 - Contract Fee Rate).",
        "faqs": [
            ("How do Upwork's 0% to 15% fees and Direct Contract rates work?", "Upwork's marketplace freelancer service fee varies from 0% to 15% per contract. For Direct Contracts (clients you bring to Upwork), the standard fee is 5%, while eligible Freelancer Plus subscribers receive a 0% Direct Contract fee."),
            ("How much should I bid to take home $1,000 net at an example 10% or 15% fee?", "At a 10% rate (before withdrawal fee), bid $1,111.11 ($1,000 / 0.90). At a 15% rate, bid $1,176.47 ($1,000 / 0.85). Select any preset above or enter your exact contract rate.")
        ]
    },
    {
        "slug": "fiverr-seller-fee-calculator",
        "title": "Fiverr 20% Seller Commission & Payout Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate Fiverr's 20% seller commission and required order price to reach your target freelance earnings.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Fiverr Gig Order Price ($ USD)",
            "default_amount": 250,
            "percent_fee": 20.0,
            "fixed_fee": 1.00,
            "fx_markup_percent": 0.0,
            "label_pct": "Fiverr Seller Commission (%)",
            "label_fixed": "Payout Withdrawal Fee ($)",
            "label_fx": "Currency Conversion Spread (%)"
        },
        "formula_explanation": "Seller Net Payout = Order Price × 0.80 - Payout Fee.",
        "faqs": [
            ("Does Fiverr take 20% from tips as well?", "Yes, Fiverr applies its standard 20% commission to gig orders, custom extras, and buyer tips."),
            ("What gross price is needed to net $100 on Fiverr?", "Divide $100 by 0.80 = $125 gross gig price.")
        ]
    },
    {
        "slug": "stripe-international-fee-calculator",
        "title": "Stripe Card, International & FX Fee Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate Stripe 2.9% + $0.30 domestic card fees plus +1.5% international card and +1% currency conversion fees.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Charge Amount ($ USD)",
            "default_amount": 100,
            "percent_fee": 2.9,
            "fixed_fee": 0.30,
            "fx_markup_percent": 2.5,
            "label_pct": "Base Card Processing Fee (%)",
            "label_fixed": "Fixed Cent Fee ($)",
            "label_fx": "International Card (+1.5%) & FX (+1.0%) Surcharge (%)"
        },
        "formula_explanation": "Net Stripe Payout = Charge - (Charge × (2.9% + International/FX %)) - $0.30.",
        "faqs": [
            ("Why did Stripe charge more than 2.9% + $0.30?", "When a customer pays with a card issued outside your Stripe account's country (+1.5%) or in a different currency (+1.0%), total percentage fees reach 5.4% + $0.30."),
            ("How do I pass the Stripe fee on to the customer?", "Use the reverse gross-up formula: Total to Charge = (Target Net + $0.30) / (1 - Total Fee %).")
        ]
    },
    {
        "slug": "paypal-goods-services-fee-calculator",
        "title": "PayPal Commercial & International Fee Calculator",
        "category": "Payment & Fee Calculators",
        "short_desc": "Calculate PayPal Goods & Services fees (3.49% + $0.49), cross-border surcharges (+1.5%), and FX spread.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Invoice / Payment Amount ($ USD)",
            "default_amount": 200,
            "percent_fee": 3.49,
            "fixed_fee": 0.49,
            "fx_markup_percent": 1.5,
            "label_pct": "PayPal Commercial Rate (%)",
            "label_fixed": "Fixed Transaction Fee ($)",
            "label_fx": "Cross-Border Surcharge (%)"
        },
        "formula_explanation": "Net PayPal Balance = Invoice Amount - (Invoice × (3.49% + Cross-Border %)) - $0.49.",
        "faqs": [
            ("What is PayPal's international transaction surcharge?", "Receiving a commercial payment from a sender in another country typically adds a 1.50% cross-border fee, plus 3%–4% if currency conversion is required."),
            ("How can I calculate the exact invoice amount to receive $500 net?", "Our calculator automatically displays the Reverse Gross-Up Invoice price right below your net result.")
        ]
    },
    {
        "slug": "armenia-it-tax-turnover-calculator",
        "title": "Armenia Freelancer, Sole Proprietor & Gross Turnover Tax Calculator (Art. 257)",
        "category": "Payment & Fee Calculators",
        "short_desc": "Estimate net take-home income in Armenia with turnover tax assessed on full gross sales revenue (RA Tax Code Art. 257), fixed social/stamp contributions, and banking fees.",
        "tool_type": "fee_calc",
        "config": {
            "label_amount": "Monthly Gross Sales Turnover (AMD or USD equiv. — Art. 257 Gross Base)",
            "default_amount": 1000000,
            "percent_fee": 1.0,
            "fixed_fee": 15000,
            "fx_markup_percent": 0.0,
            "label_pct": "Gross Turnover Tax Rate (% on Full Gross Revenue)",
            "label_fixed": "Monthly Fixed Social + Stamp Duty (Zinapah)",
            "label_fx": "Bank / Payout Gateway Fee (% on Gross)",
            "presets": [
                {"label": "1% (Qualifying High-Tech / IT — Eligibility Required)", "pct": 1.0},
                {"label": "0% (Eligible Micro-Business <24M AMD — Restrictions Apply)", "pct": 0.0},
                {"label": "5% (Example Turnover Rate)", "pct": 5.0},
                {"label": "10% (General Turnover Tax Reference)", "pct": 10.0}
            ],
            "source_name": "Republic of Armenia Tax Code (Article 257 Gross Turnover Base)",
            "verified_date": "2026-10-27"
        },
        "formula_explanation": "Per RA Tax Code Article 257, Turnover Tax is calculated on Gross Sales Turnover (before deducting platform or bank fees): Turnover_Tax = Gross_Turnover × Tax_Rate%. Net Monthly Income = Gross_Turnover - Turnover_Tax - (Gross_Turnover × Bank_Fee%) - Fixed_Monthly_Contributions.",
        "faqs": [
            ("How is the turnover tax base defined under Article 257 of Armenia's Tax Code?", "Article 257 defines the turnover tax base as gross sales turnover. Marketplace commissions (such as Upwork or Fiverr fees) and payment processor withdrawal fees do not reduce the gross turnover tax base."),
            ("Does every freelancer automatically qualify for the 1% High-Tech rate or 0% Micro-Business regime?", "No. The 1% rate applies strictly to qualifying high-tech/IT activities and eligible taxpayers under the 115M AMD threshold, while the 0% micro-business regime (under 24M AMD) excludes consulting and several professional services. Verify your exact classification with a licensed Armenian accountant.")
        ]
    },

    # =========================================================================
    # VERTICAL 2: SAAS, ADVERTISING & E-COMMERCE UNIT ECONOMICS
    # =========================================================================
    {
        "slug": "saas-mrr-churn-ltv-calculator",
        "title": "SaaS Customer Lifetime Value (LTV) & Churn Calculator",
        "category": "SaaS & Marketing Calculators",
        "short_desc": "Calculate SaaS Customer Lifetime Value (LTV), LTV:CAC ratio, and annual revenue lost to monthly churn.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Average Revenue Per User / Mo (ARPU $)",
            "default_a": 49,
            "label_b": "Gross Margin (%)",
            "default_b": 85,
            "label_c": "Monthly Customer Churn Rate (%)",
            "default_c": 4.5,
            "label_d": "Customer Acquisition Cost (CAC $)",
            "default_d": 180,
            "mode": "ltv"
        },
        "formula_explanation": "LTV = (ARPU × Gross Margin %) / Monthly Churn Rate. LTV:CAC Ratio = LTV / CAC. CAC Payback Months = CAC / (ARPU × Gross Margin %).",
        "faqs": [
            ("What is a healthy LTV:CAC ratio for a SaaS business?", "A benchmark LTV:CAC ratio of 3:1 or higher indicates sustainable unit economics, while a CAC payback period under 6–12 months is ideal for bootstrapped founders."),
            ("How does reducing churn from 5% to 2.5% impact LTV?", "Cutting monthly churn in half doubles average customer lifespan (from 20 months to 40 months) and doubles Customer Lifetime Value.")
        ]
    },
    {
        "slug": "roas-break-even-calculator",
        "title": "Break-Even ROAS & Target CPA Ad Calculator",
        "category": "SaaS & Marketing Calculators",
        "short_desc": "Calculate your exact Break-Even Return on Ad Spend (ROAS) and maximum profitable Cost Per Acquisition (CPA).",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Average Order Value / Product Price ($)",
            "default_a": 80,
            "label_b": "Product COGS + Fulfillment + Payment Fees ($)",
            "default_b": 28,
            "label_c": "Monthly Ad Spend Budget ($)",
            "default_c": 1500,
            "label_d": "Actual / Expected Ad ROAS (e.g. 2.5x)",
            "default_d": 2.5,
            "mode": "roas"
        },
        "formula_explanation": "Contribution Margin = Price - COGS. Profit Margin % = Margin / Price. Break-Even ROAS = 1 / Profit Margin %. Break-Even CPA = Contribution Margin.",
        "faqs": [
            ("Why is 2.0x ROAS sometimes unprofitable?", "If your gross profit margin after COGS, shipping, and payment fees is 40%, your Break-Even ROAS is 1 / 0.40 = 2.50x. Any ROAS below 2.50x loses money on the first order."),
            ("What is Maximum Profitable CPA?", "Your Maximum CPA is the exact dollar profit left from an average order after deducting all non-ad variable costs.")
        ]
    },
    {
        "slug": "cpm-cpc-ctr-ad-revenue-calculator",
        "title": "Website Display Ad & Game eCPM Revenue Calculator",
        "category": "SaaS & Marketing Calculators",
        "short_desc": "Estimate monthly website or HTML5 game ad earnings from daily sessions, ad impressions per visit, eCPM, and platform revenue split.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Daily Sessions / Visitors",
            "default_a": 2500,
            "label_b": "Paid Ad Impressions Per Session",
            "default_b": 2.0,
            "label_c": "Effective CPM (eCPM $ per 1,000 Ads)",
            "default_c": 3.20,
            "label_d": "Publisher Revenue Share (%)",
            "default_d": 68,
            "mode": "ad_rev"
        },
        "formula_explanation": "Monthly Net Ad Revenue = (Daily Sessions × 30 × Ads/Session / 1000) × eCPM × (Publisher Share % / 100).",
        "faqs": [
            ("What is the difference between Advertiser eCPM and Publisher Page RPM?", "eCPM is the gross cost per 1,000 ad impressions before the ad network or portal takes its cut. Google AdSense typically gives publishers 68% of content ad revenue."),
            ("Why do finance and developer utility pages have higher eCPMs than gaming?", "B2B software and financial advertisers pay much higher CPC bids than casual entertainment advertisers, resulting in higher RPMs per visitor.")
        ]
    },
    {
        "slug": "shopify-profit-margin-calculator",
        "title": "E-Commerce & Dropshipping Net Margin Calculator",
        "category": "SaaS & Marketing Calculators",
        "short_desc": "Calculate net profit per order and profit margin percentage after product cost, shipping, ad CPA, and gateway fees.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Retail Selling Price ($)",
            "default_a": 65,
            "label_b": "Product Cost + Shipping ($)",
            "default_b": 22,
            "label_c": "Ad Cost Per Purchase / CPA ($)",
            "default_c": 18,
            "label_d": "Gateway & Refund Allowance (%)",
            "default_d": 4.5,
            "mode": "ecom"
        },
        "formula_explanation": "Net Profit = Selling Price - Product & Shipping Cost - Ad CPA - (Selling Price × Gateway/Refund %).",
        "faqs": [
            ("What net profit margin should an e-commerce store target?", "Healthy direct-to-consumer stores typically aim for a 15% to 25% net profit margin after accounting for customer acquisition cost (CPA) and payment fees."),
            ("Should refund rates be included in unit economics?", "Yes, setting aside 2%–5% for returns and chargebacks prevents overestimating net profit.")
        ]
    },
    {
        "slug": "email-marketing-roi-calculator",
        "title": "Email Marketing & Newsletter ROI Calculator",
        "category": "SaaS & Marketing Calculators",
        "short_desc": "Calculate open-to-click conversions, total sales generated, and net ROI percentage from email campaigns.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Total Subscribers Sent",
            "default_a": 5000,
            "label_b": "Click-Through Rate (CTR % of Total Sent)",
            "default_b": 3.2,
            "label_c": "Landing Page Conversion Rate (%)",
            "default_c": 4.0,
            "label_d": "Net Profit Per Conversion ($)",
            "default_d": 45,
            "mode": "email_roi"
        },
        "formula_explanation": "Total Clicks = Subscribers × CTR%. Conversions = Clicks × Conv%. Net Revenue = Conversions × Profit per Sale.",
        "faqs": [
            ("What is a realistic Click-to-Conversion rate for targeted email lists?", "Warm newsletter subscribers typically convert at 2% to 5% on relevant digital products or SaaS offers."),
            ("How is Email Revenue Per Subscriber (RPS) calculated?", "Divide monthly email-attributed net revenue by your total active subscriber count.")
        ]
    },
    {
        "slug": "ab-test-sample-size-calculator",
        "title": "Conversion Rate Lift & Monthly Revenue Impact Calculator",
        "category": "SaaS & Marketing Calculators",
        "short_desc": "Calculate how much additional monthly and annual revenue a small conversion rate improvement generates.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Monthly Website Visitors",
            "default_a": 10000,
            "label_b": "Current Conversion Rate (%)",
            "default_b": 2.0,
            "label_c": "Improved Conversion Rate (%)",
            "default_c": 2.6,
            "label_d": "Average Customer Value ($)",
            "default_d": 59,
            "mode": "cro"
        },
        "formula_explanation": "Extra Monthly Conversions = Visitors × (New CR% - Current CR%). Annual Revenue Lift = Extra Monthly Conversions × Customer Value × 12.",
        "faqs": [
            ("Why is Conversion Rate Optimization (CRO) higher leverage than buying more ads?", "Increasing conversion rate from 2.0% to 2.6% (+30% relative lift) increases revenue by 30% without spending an extra dollar on traffic.")
        ]
    },

    # =========================================================================
    # VERTICAL 3: INSTANT CLIENT-SIDE DEVELOPER & DATA UTILITIES
    # =========================================================================
    {
        "slug": "json-to-typescript-schema-converter",
        "title": "JSON to TypeScript Interface & Zod Schema Converter",
        "category": "Developer Utilities",
        "short_desc": "Convert any raw JSON object or API payload into strict TypeScript interfaces and runtime Zod validation schemas instantly in your browser.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "json_to_ts",
            "sample_input": '{\n  "id": 1024,\n  "username": "armenia_dev",\n  "isVerified": true,\n  "balanceUsd": 1450.75,\n  "tags": ["saas", "automation"]\n}'
        },
        "formula_explanation": "Parses JSON AST in-memory inside your browser (100% private—zero server uploads) and infers TypeScript types and Zod schemas recursively.",
        "faqs": [
            ("Is my JSON data sent to any backend server?", "No. 100% of parsing and code generation happens locally inside your browser's JavaScript engine."),
            ("Does it handle arrays and nested objects?", "Yes, nested objects and typed arrays are automatically mapped to corresponding TypeScript and Zod definitions.")
        ]
    },
    {
        "slug": "cron-expression-explainer",
        "title": "Cron Expression Explainer & Schedule Validator",
        "category": "Developer Utilities",
        "short_desc": "Translate 5-field Linux/GitHub Actions cron expressions into plain English and verify execution schedules.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "cron",
            "sample_input": "*/15 9-17 * * 1-5"
        },
        "formula_explanation": "Standard 5-field Cron syntax: [Minute 0-59] [Hour 0-23] [Day of Month 1-31] [Month 1-12] [Day of Week 0-6 (Sun-Sat)].",
        "faqs": [
            ("What does */15 mean in a cron expression?", "The slash (/) specifies step values—*/15 in the minute field runs the job every 15 minutes (at :00, :15, :30, and :45)."),
            ("How do I run a cron job only on weekdays?", "Set the 5th field (Day of Week) to 1-5 (Monday through Friday).")
        ]
    },
    {
        "slug": "jwt-token-decoder",
        "title": "Offline JWT Token Header & Payload Decoder",
        "category": "Developer Utilities",
        "short_desc": "Inspect JSON Web Token (JWT) headers, claims, and expiration timestamps 100% client-side without exposing secrets over the network.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "jwt",
            "sample_input": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyXzkwMSIsIm5hbWUiOiJWYWhlIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzMwMDAwMDAwLCJleHAiOjE5MDAwMDAwMDB9.signature_placeholder"
        },
        "formula_explanation": "Splits the token on '.' delimiters and Base64Url-decodes the Header (Part 1) and Payload Claims (Part 2), formatting `iat` and `exp` Unix timestamps into ISO dates.",
        "faqs": [
            ("Why is it safer to decode JWTs in a client-side static tool?", "Many online decoders log requests on their servers. Because this page is a static client-side script, your token never leaves your browser tab.")
        ]
    },
    {
        "slug": "sql-query-formatter",
        "title": "SQL Query Pretty Printer & Clause Formatter",
        "category": "Developer Utilities",
        "short_desc": "Format minified or messy SQL queries with clean uppercase keywords and structured clause indentation.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "sql",
            "sample_input": "select u.id, u.email, count(o.id) as total_orders from users u inner join orders o on u.id = o.user_id where u.status = 'active' group by u.id, u.email having count(o.id) > 2 order by total_orders desc limit 25;"
        },
        "formula_explanation": "Normalizes whitespace, uppercases standard ANSI SQL keywords, and places major clauses (SELECT, FROM, JOIN, WHERE, GROUP BY, ORDER BY) on clean indented lines.",
        "faqs": [
            ("Which SQL dialects are supported?", "Standard ANSI SQL, PostgreSQL, MySQL, SQLite, and BigQuery queries work out of the box.")
        ]
    },
    {
        "slug": "base64-url-hash-encoder",
        "title": "UTF-8 Safe Base64 & URL Encoder / Decoder",
        "category": "Developer Utilities",
        "short_desc": "Encode and decode UTF-8 strings to Base64, Base64Url, and URL-encoded query parameters instantly.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "base64",
            "sample_input": "https://calcgrid.dev/api?merchant=armenia&currency=AMD&amount=45000"
        },
        "formula_explanation": "Uses TextEncoder UTF-8 byte arrays to safely Base64-encode Unicode characters without `btoa` Latin1 exceptions.",
        "faqs": [
            ("Why does standard JavaScript btoa() fail on Armenian or emoji characters?", "Standard `btoa()` only accepts 8-bit Latin1 characters. Converting through `TextEncoder` UTF-8 bytes ensures multi-byte Unicode strings encode accurately.")
        ]
    },
    {
        "slug": "csv-to-json-converter",
        "title": "Instant Browser CSV to JSON & SQL Converter",
        "category": "Developer Utilities",
        "short_desc": "Convert CSV spreadsheet rows with headers into formatted JSON arrays locally in your browser.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "csv_to_json",
            "sample_input": "product_id,name,price_usd,in_stock\n101,Pro CLI Pack,29.00,true\n102,Automation Templates,19.00,true\n103,Enterprise License,99.00,false"
        },
        "formula_explanation": "Parses the header row for property keys and automatically casts numeric and boolean cell values into typed JSON objects.",
        "faqs": [
            ("Are numeric and boolean columns automatically typed?", "Yes, cells matching numbers or `true`/`false` are automatically converted to native JSON numbers and booleans.")
        ]
    },
    {
        "slug": "regex-pattern-tester",
        "title": "Live Regular Expression Matcher & Group Extractor",
        "category": "Developer Utilities",
        "short_desc": "Test JavaScript RegExp patterns against multi-line sample text and inspect all matched substrings and capture groups.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "regex",
            "sample_input": "Contact support@company.am or sales@startup.io for invoices #INV-2049 and #INV-8831."
        },
        "formula_explanation": "Executes `String.prototype.matchAll()` with global/multiline flags and lists every match index and capture group.",
        "faqs": [
            ("How do I match email addresses or invoice IDs?", "Our default test pattern extracts all email addresses and shows exact character positions.")
        ]
    },
    {
        "slug": "svg-to-data-uri-optimizer",
        "title": "SVG to CSS Data URI & React JSX Component Converter",
        "category": "Developer Utilities",
        "short_desc": "Convert raw SVG markup into URL-encoded CSS `background-image` Data URIs and clean React JSX components.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "svg",
            "sample_input": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5z"/></svg>'
        },
        "formula_explanation": "Strips redundant whitespace, converts `stroke-width` to camelCase `strokeWidth` for React JSX, and generates a compact `data:image/svg+xml` CSS string.",
        "faqs": [
            ("Why is URL-encoded SVG better than Base64 for CSS backgrounds?", "URL-encoded SVGs are ~25% smaller than Base64 strings and compress much better with Gzip/Brotli.")
        ]
    },

    # =========================================================================
    # VERTICAL 4: BUSINESS OPERATIONS, AI COST & PRICING TOOLS
    # =========================================================================
    {
        "slug": "freelance-hourly-rate-calculator",
        "title": "Freelance Target Annual Income to Billable Hourly Rate Calculator",
        "category": "Business & Operations Tools",
        "short_desc": "Calculate your minimum billable hourly and daily rate after accounting for vacation days, non-billable admin time, overhead, and taxes.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Target Annual Net Income ($ USD)",
            "default_a": 48000,
            "label_b": "Annual Business Overhead & Software ($)",
            "default_b": 2400,
            "label_c": "Billable Hours Per Week (After Admin/Sales)",
            "default_c": 25,
            "label_d": "Effective Tax & Platform Fee Rate (%)",
            "default_d": 15,
            "mode": "hourly_rate"
        },
        "formula_explanation": "Gross Required = (Target Net + Overhead) / (1 - Tax%). Billable Hours/Year = Billable Hours/Week × 48 Working Weeks. Minimum Hourly Rate = Gross Required / Billable Hours/Year.",
        "faqs": [
            ("Why can't freelancers divide annual salary by 2,080 hours?", "Full-time freelancers typically spend 30%–40% of their week on unbilled tasks (proposals, invoicing, revisions) and take holidays, leaving ~1,100–1,250 true billable hours per year.")
        ]
    },
    {
        "slug": "software-project-estimation-calculator",
        "title": "PERT 3-Point Software Project Time & Quote Calculator",
        "category": "Business & Operations Tools",
        "short_desc": "Use the engineering PERT formula (Optimistic, Most Likely, Pessimistic hours) to calculate realistic project timelines and fixed-price quotes.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Optimistic Hours (Best Case)",
            "default_a": 40,
            "label_b": "Most Likely Hours (Realistic)",
            "default_b": 65,
            "label_c": "Pessimistic Hours (Worst Case / Bugs)",
            "default_c": 120,
            "label_d": "Hourly Billing Rate ($/hr)",
            "default_d": 50,
            "mode": "pert"
        },
        "formula_explanation": "PERT Expected Hours = (Optimistic + 4 × Most Likely + Pessimistic) / 6. Standard Deviation σ = (Pessimistic - Optimistic) / 6. 95% Confidence Buffer = Expected + 2σ.",
        "faqs": [
            ("Why should fixed-price contracts be quoted at the 95% Confidence level?", "Quoting at Expected + 2 Standard Deviations protects your margin against unexpected API changes, scope creep, and edge-case bugs.")
        ]
    },
    {
        "slug": "cloud-llm-token-cost-calculator",
        "title": "AI LLM API Token & Monthly Cost Calculator",
        "category": "Business & Operations Tools",
        "short_desc": "Estimate monthly LLM API costs from daily requests, prompt input tokens, completion output tokens, and model pricing per 1M tokens.",
        "tool_type": "saas_calc",
        "config": {
            "label_a": "Daily API Requests",
            "default_a": 1000,
            "label_b": "Avg Input + Output Tokens Per Request",
            "default_b": 2500,
            "label_c": "Blended Model Cost Per 1M Tokens ($)",
            "default_c": 1.50,
            "label_d": "Prompt Caching Discount (%)",
            "default_d": 30,
            "mode": "llm_cost"
        },
        "formula_explanation": "Monthly Tokens = Daily Requests × 30 × Tokens/Request. Monthly Cost = (Monthly Tokens / 1,000,000) × Price per 1M × (1 - Caching Discount %).",
        "faqs": [
            ("How many words is 1,000 LLM tokens?", "In English, 1,000 tokens is approximately 750 words (or roughly 4 characters per token).")
        ]
    },
    {
        "slug": "password-entropy-generator",
        "title": "Cryptographic Password & Entropy Bits Generator",
        "category": "Business & Operations Tools",
        "short_desc": "Generate high-entropy random API keys and passwords using `window.crypto.getRandomValues()` and calculate brute-force entropy bits.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "password",
            "sample_input": "24"
        },
        "formula_explanation": "Entropy (bits) = Length × log2(Character Pool Size). A 24-character mixed-charset password yields >142 bits of entropy.",
        "faqs": [
            ("Does this use Math.random() or Web Crypto?", "It uses the browser's cryptographically secure `window.crypto.getRandomValues()` CSPRNG.")
        ]
    },
    {
        "slug": "markdown-to-html-converter",
        "title": "Instant Markdown to Clean Semantic HTML Converter",
        "category": "Business & Operations Tools",
        "short_desc": "Convert Markdown headings, lists, code blocks, and links into clean semantic HTML snippets ready to paste into any CMS.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "markdown",
            "sample_input": "# Launch Checklist\n\n- **Zero Operating Cost:** Hosted on static CDN\n- **Armenia Payouts:** Lemon Squeezy & AdSense wire transfers\n\n```bash\npython3 engine/autopilot.py --verify\n```"
        },
        "formula_explanation": "Client-side regex parser converts Markdown block and inline syntax into semantic HTML tags.",
        "faqs": [
            ("Can I copy the raw HTML output directly?", "Yes, the output panel gives you clean, unbloated HTML with zero inline style clutter.")
        ]
    },
    {
        "slug": "utm-campaign-link-builder",
        "title": "UTM Marketing URL Builder & Campaign Tag Generator",
        "category": "Business & Operations Tools",
        "short_desc": "Generate properly URL-encoded UTM tracking links (`utm_source`, `utm_medium`, `utm_campaign`) for analytics attribution.",
        "tool_type": "dev_tool",
        "config": {
            "dev_mode": "utm",
            "sample_input": "https://calcgrid.dev/tools/lemonsqueezy-fee-calculator|reddit|organic_post|q4_launch"
        },
        "formula_explanation": "Parses `BaseURL | Source | Medium | Campaign` and constructs a validated, URL-encoded tracking link.",
        "faqs": [
            ("Why should UTM parameters always be lowercase?", "Analytics tools treat `UTM_Source=Reddit` and `utm_source=reddit` as two separate traffic sources. Our builder automatically normalizes tags to lowercase.")
        ]
    }
]
