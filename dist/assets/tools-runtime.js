// ============================================================================
// PayoutFolio Client-Side Computation Engine, Country Corridor Router & CSV Auditor
// ============================================================================

const CALCGRID_CORRIDORS = {"AM": {"name": "Armenia", "currency": "AMD", "default_fx_placeholder": 388.0, "fx_note": "User-editable reference rate (AMD per 1 USD). Enter your bank or CBA rate; This tool never fabricates live FX feeds.", "verified_date": "2026-10-27", "official_sources": "RA Tax Code (Turnover Tax & High-Tech Registry), Payoneer Pricing Schedule, Wise Country Availability Docs, Lemon Squeezy MoR Payouts", "rails": {"payoneer": {"available": true, "status_badge": "SUPPORTED & WIDELY USED", "pct_fee": 1.0, "fixed_fee": 0.0, "fx_spread_expected": 2.0, "fx_spread_min": 1.5, "fx_spread_max": 3.0, "intermediary_min": 0.0, "intermediary_max": 0.0, "note": "Direct withdrawals to Armenian banks (Ameriabank, Inecobank, Ardshinbank, etc.) or Payoneer card. Typical local currency withdrawal markup is ~2% (range 1.5%\u20133.0%). Annual fee $29.95 applies if annual volume < $6,000."}, "wise": {"available": false, "status_badge": "RECEIVING RESTRICTED FOR RESIDENTS", "pct_fee": 0.65, "fixed_fee": 4.14, "fx_spread_expected": 0.0, "fx_spread_min": 0.0, "fx_spread_max": 0.5, "intermediary_min": 0.0, "intermediary_max": 15.0, "note": "Wise does not currently issue local USD/EUR receiving account details to residents of Armenia. Incoming direct transfers from foreign clients must typically route via SWIFT/Payoneer unless using an eligible foreign entity."}, "swift": {"available": true, "status_badge": "SUPPORTED (HIGH FIXED & INTERMEDIARY FEES)", "pct_fee": 0.2, "fixed_fee": 25.0, "fx_spread_expected": 1.2, "fx_spread_min": 0.8, "fx_spread_max": 2.0, "intermediary_min": 10.0, "intermediary_max": 35.0, "note": "Supported by all Armenian banks; requires formal invoice/contract for compliance. Correspondent intermediary banks typically deduct $10\u2013$35 mid-route."}, "lemonsqueezy": {"available": true, "status_badge": "SUPPORTED (MERCHANT OF RECORD WIRE)", "pct_fee": 5.0, "fixed_fee": 0.5, "fx_spread_expected": 1.5, "fx_spread_min": 1.5, "fx_spread_max": 2.5, "intermediary_min": 0.0, "intermediary_max": 15.0, "note": "Official Merchant of Record for SaaS & digital products; handles global VAT/GST and supports international wire payouts to Armenia ($50 minimum payout)."}}, "tax_presets": [{"label": "1.0% \u2014 Qualifying High-Tech / IT Turnover Tax (Gross Base per Art. 257, Eligibility Required)", "rate": 1.0}, {"label": "0.0% \u2014 Eligible Micro-Business (<24M AMD/yr, Activity Restrictions Apply)", "rate": 0.0}, {"label": "10.0% \u2014 General Turnover Tax Reference Example (Gross Base)", "rate": 10.0}], "tax_caveat": "Per Article 257 of the Republic of Armenia Tax Code, turnover tax is assessed on full GROSS sales turnover (the gross invoice billed to the client, BEFORE deducting marketplace or payment withdrawal fees). Both the 1% high-tech rate (up to 115M AMD cap) and the 0% micro-business regime (under 24M AMD cap) apply strictly to qualifying activities and eligible taxpayers; many professional/consulting services are excluded. Confirm your eligibility with a licensed Armenian accountant."}, "GE": {"name": "Georgia", "currency": "GEL", "default_fx_placeholder": 2.72, "fx_note": "User-editable reference rate (GEL per 1 USD). Enter your NBG or bank rate.", "verified_date": "2026-10-27", "official_sources": "Revenue Service of Georgia (rs.ge Small Business Status), Wise Georgia Pricing, Payoneer Pricing Schedule", "rails": {"payoneer": {"available": true, "status_badge": "SUPPORTED (TBC & BOG INTEGRATED)", "pct_fee": 1.0, "fixed_fee": 0.0, "fx_spread_expected": 2.0, "fx_spread_min": 1.8, "fx_spread_max": 3.0, "intermediary_min": 0.0, "intermediary_max": 0.0, "note": "Widely integrated with TBC Bank and Bank of Georgia; local withdrawal to GEL carries ~2%\u20133% conversion markup."}, "wise": {"available": true, "status_badge": "SUPPORTED (MID-MARKET FX)", "pct_fee": 0.65, "fixed_fee": 4.14, "fx_spread_expected": 0.0, "fx_spread_min": 0.0, "fx_spread_max": 0.3, "intermediary_min": 0.0, "intermediary_max": 5.0, "note": "Georgian residents can open multi-currency Wise accounts and convert at the mid-market rate with transparent route fees."}, "swift": {"available": true, "status_badge": "SUPPORTED (INTERMEDIARY DEDUCTIONS)", "pct_fee": 0.2, "fixed_fee": 20.0, "fx_spread_expected": 1.2, "fx_spread_min": 0.8, "fx_spread_max": 2.0, "intermediary_min": 10.0, "intermediary_max": 30.0, "note": "Direct wire to TBC or Bank of Georgia; intermediary correspondent fees ($10\u2013$30) apply unless sent OUR."}, "lemonsqueezy": {"available": true, "status_badge": "SUPPORTED (MOR BANK PAYOUT)", "pct_fee": 5.0, "fixed_fee": 0.5, "fx_spread_expected": 1.5, "fx_spread_min": 1.5, "fx_spread_max": 2.5, "intermediary_min": 0.0, "intermediary_max": 10.0, "note": "Supports digital product and SaaS payouts to Georgian bank accounts."}}, "tax_presets": [{"label": "1.0% \u2014 IE Small Business Status (up to 500,000 GEL/yr)", "rate": 1.0}, {"label": "3.0% \u2014 IE Small Business Status (Turnover above 500,000 GEL)", "rate": 3.0}, {"label": "0.0% \u2014 Pre-Tax Payout Comparison", "rate": 0.0}], "tax_caveat": "Georgia's Individual Entrepreneur Small Business Status taxes gross turnover at 1% up to 500,000 GEL/year (3% above cap). Certain consulting, legal, accounting, and medical services are excluded from the 1% regime."}, "RS": {"name": "Serbia", "currency": "RSD", "default_fx_placeholder": 108.5, "fx_note": "User-editable reference rate (RSD per 1 USD). Enter your NBS middle exchange rate.", "verified_date": "2026-10-27", "official_sources": "Tax Administration of Serbia (purs.gov.rs Pau\u0161al Rules), National Bank of Serbia, Wise & Payoneer Schedules", "rails": {"payoneer": {"available": true, "status_badge": "SUPPORTED", "pct_fee": 1.0, "fixed_fee": 0.0, "fx_spread_expected": 2.0, "fx_spread_min": 1.8, "fx_spread_max": 3.0, "intermediary_min": 0.0, "intermediary_max": 0.0, "note": "Popular among Serbian marketplace freelancers; ~2%\u20133% conversion spread when withdrawing to RSD."}, "wise": {"available": false, "status_badge": "NOT LISTED FOR WISE ACCOUNT HOLDING", "pct_fee": 0.65, "fixed_fee": 4.14, "fx_spread_expected": 0.0, "fx_spread_min": 0.0, "fx_spread_max": 0.3, "intermediary_min": 0.0, "intermediary_max": 5.0, "note": "Serbia is not listed on Wise\u2019s current holding-money eligibility page. This account-based route is excluded. Client-initiated Wise bank transfers are a different product and are not evaluated here. Check the provider for your exact account."}, "swift": {"available": true, "status_badge": "SUPPORTED (REQUIRES LOR / INFLOW BASIS)", "pct_fee": 0.3, "fixed_fee": 20.0, "fx_spread_expected": 1.5, "fx_spread_min": 1.0, "fx_spread_max": 2.5, "intermediary_min": 10.0, "intermediary_max": 30.0, "note": "Requires foreign inflow basis declaration (\u0161ifra osnova priliva) with local Serbian banks."}, "lemonsqueezy": {"available": true, "status_badge": "SUPPORTED (MOR WIRE PAYOUT)", "pct_fee": 5.0, "fixed_fee": 0.5, "fx_spread_expected": 1.5, "fx_spread_min": 1.5, "fx_spread_max": 2.5, "intermediary_min": 0.0, "intermediary_max": 15.0, "note": "Merchant of Record payouts for software and digital products."}}, "tax_presets": [{"label": "10.0% \u2014 Illustrative Effective Pau\u0161al Reserve (up to 6M RSD cap)", "rate": 10.0}, {"label": "0.0% \u2014 Pre-Tax Payout Comparison", "rate": 0.0}, {"label": "15.0% \u2014 Conservative Tax & Social Reserve Example", "rate": 15.0}], "tax_caveat": "Serbia's Preduzetnik Pau\u0161alac regime charges a fixed monthly RSD amount (determined by municipality and activity code, up to 6,000,000 RSD annual turnover) rather than a flat percentage, and requires passing the 9-criteria Independence Test (test samostalnosti)."}, "PH": {"name": "Philippines", "currency": "PHP", "default_fx_placeholder": 58.2, "fx_note": "User-editable reference rate (PHP per 1 USD). Enter your BSP or bank rate.", "verified_date": "2026-10-27", "official_sources": "Bureau of Internal Revenue (bir.gov.ph 8% Gross Receipts Option), Wise Philippines, Payoneer Philippines", "rails": {"payoneer": {"available": true, "status_badge": "SUPPORTED (GCASH & LOCAL BANKS)", "pct_fee": 1.0, "fixed_fee": 0.0, "fx_spread_expected": 2.0, "fx_spread_min": 1.8, "fx_spread_max": 3.0, "intermediary_min": 0.0, "intermediary_max": 0.0, "note": "Integrated with Upwork and GCash; ~2% conversion spread above mid-market rate."}, "wise": {"available": true, "status_badge": "SUPPORTED (FAST PHP / GCASH / MAYA)", "pct_fee": 0.6, "fixed_fee": 3.5, "fx_spread_expected": 0.0, "fx_spread_min": 0.0, "fx_spread_max": 0.2, "intermediary_min": 0.0, "intermediary_max": 0.0, "note": "Full Wise account support in the Philippines with mid-market PHP conversion to local banks (BPI, BDO, UnionBank) and e-wallets."}, "swift": {"available": true, "status_badge": "SUPPORTED (HIGH REMITTANCE FEES)", "pct_fee": 0.25, "fixed_fee": 25.0, "fx_spread_expected": 1.5, "fx_spread_min": 1.0, "fx_spread_max": 2.5, "intermediary_min": 10.0, "intermediary_max": 30.0, "note": "Traditional SWIFT wires incur correspondent bank deductions and wider PHP conversion spreads."}, "lemonsqueezy": {"available": true, "status_badge": "SUPPORTED (MOR PAYOUTS)", "pct_fee": 5.0, "fixed_fee": 0.5, "fx_spread_expected": 1.5, "fx_spread_min": 1.5, "fx_spread_max": 2.5, "intermediary_min": 0.0, "intermediary_max": 10.0, "note": "Supports digital creator payouts to Philippine bank accounts."}}, "tax_presets": [{"label": "8.0% \u2014 BIR 8% Gross Receipts Tax Option (Under PHP 3M VAT threshold)", "rate": 8.0}, {"label": "0.0% \u2014 Pre-Tax Payout Comparison", "rate": 0.0}], "tax_caveat": "Self-employed professionals in the Philippines earning under the PHP 3,000,000 VAT threshold can elect the 8% flat income tax rate on gross receipts in excess of PHP 250,000 under the TRAIN Law."}, "IN": {"name": "India", "currency": "INR", "default_fx_placeholder": 84.1, "fx_note": "User-editable reference rate (INR per 1 USD). Enter your RBI reference or bank card rate.", "verified_date": "2026-10-27", "official_sources": "Income Tax Act Section 44ADA, RBI FEMA Export Purpose Code P0802, Wise India eFIRC Docs, Payoneer India FIRA Schedule", "rails": {"payoneer": {"available": true, "status_badge": "SUPPORTED (AUTO DIGITAL FIRA)", "pct_fee": 1.0, "fixed_fee": 0.0, "fx_spread_expected": 2.2, "fx_spread_min": 2.0, "fx_spread_max": 3.0, "intermediary_min": 0.0, "intermediary_max": 0.0, "note": "Provides automatic digital FIRA certificates for RBI/GST export compliance; total conversion + withdrawal cost is ~2.2%\u20133.0%."}, "wise": {"available": true, "status_badge": "SUPPORTED (MID-MARKET + EFIRC FEE)", "pct_fee": 0.65, "fixed_fee": 2.5, "fx_spread_expected": 0.0, "fx_spread_min": 0.0, "fx_spread_max": 0.3, "intermediary_min": 0.0, "intermediary_max": 2.5, "note": "Uses mid-market INR exchange rate; automated digital eFIRC / FIRA certificate available for export compliance."}, "swift": {"available": true, "status_badge": "SUPPORTED (PURPOSE CODE P0802)", "pct_fee": 0.15, "fixed_fee": 15.0, "fx_spread_expected": 1.8, "fx_spread_min": 1.0, "fx_spread_max": 2.5, "intermediary_min": 10.0, "intermediary_max": 25.0, "note": "Direct bank inward remittance (HDFC/ICICI/SBI) requires RBI Purpose Code (e.g., P0802 for software); bank FX spread varies unless negotiated."}, "lemonsqueezy": {"available": true, "status_badge": "SUPPORTED (MOR WIRE PAYOUT)", "pct_fee": 5.0, "fixed_fee": 0.5, "fx_spread_expected": 1.5, "fx_spread_min": 1.5, "fx_spread_max": 2.5, "intermediary_min": 0.0, "intermediary_max": 15.0, "note": "Merchant of Record payouts for SaaS and digital products."}}, "tax_presets": [{"label": "7.5% \u2014 Illustrative Effective Tax Provision (Sec 44ADA 50% Deemed Profit)", "rate": 7.5}, {"label": "0.0% \u2014 Pre-Tax Payout Comparison", "rate": 0.0}], "tax_caveat": "Under Section 44ADA Presumptive Taxation, eligible Indian professionals with gross receipts up to INR 75 Lakh (when >=95% of receipts are digital) declare 50% of gross receipts as taxable income, taxed at applicable individual slab rates. Export of services under GST LUT is zero-rated."}};

(function () {
  // No analytics or network requests: all inputs remain on this device.

  // 1. Homepage Live Filter
  const searchInput = document.getElementById('hub-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const q = searchInput.value.toLowerCase().trim();
      let count = 0;
      document.querySelectorAll('.category-section').forEach(function (section) {
        let visible = 0;
        section.querySelectorAll('.tool-card').forEach(function (card) {
          const matches = card.textContent.toLowerCase().includes(q);
          card.hidden = !matches;
          if (matches) { count++; visible++; }
        });
        section.hidden = visible === 0;
      });
      const feedback = document.getElementById('search-feedback');
      if (feedback) feedback.textContent = count ? count + ' tool' + (count === 1 ? '' : 's') + ' found.' : 'No tools found. Try a provider name or a shorter search.';
    });
  }

  // 2. Interactive Tool Engine
  const toolContainer = document.getElementById('interactive-tool-root');
  if (!toolContainer) return;

  const toolType = toolContainer.getAttribute('data-tool-type');
  const rawConfig = toolContainer.getAttribute('data-tool-config');
  let cfg = {};
  try { cfg = JSON.parse(rawConfig); } catch (e) {}

  const params = new URLSearchParams(window.location.search);

  function fmtMoney(n) {
    if (!Number.isFinite(n)) return 'Not achievable';
    return (cfg.currency === 'AMD' ? 'AMD ' : '$') + Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  let currentCsvRows = [];

  const btnPermalink = document.getElementById('btn-copy-permalink');
  const btnExportCsv = document.getElementById('btn-export-csv');

  if (btnExportCsv) {
    btnExportCsv.addEventListener('click', function () {
      if (!currentCsvRows.length) return;
      const exportRows = currentCsvRows.map(function (row, i) { return i === 0 && cfg.currency === 'AMD' ? row.map(v => String(v).replace(/USD/g, 'AMD')) : row; });
      const csvContent = exportRows.map(function (r) { return r.map(function (cell) {
        let value = String(cell);
        if (/^[\s]*[=+@\t\r]/.test(value) || (/^[\s]*-/.test(value) && !Number.isFinite(Number(value)))) value = "'" + value;
        return '"' + value.replace(/"/g, '""') + '"';
      }).join(','); }).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (window.location.pathname.split('/').pop().replace('.html', '') || 'calculation') + '-ledger.csv';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  function escapeText(value) {
    return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  if (btnPermalink) btnPermalink.addEventListener('click', async function () {
    const u = new URL(window.location.href);
    u.search = '';
    const keys = {country:'in-country',amount:'in-amount',origin_pct:'in-origin-pct',origin_fix:'in-origin-fix',tax:'in-tax-pct',fx_rate:'in-fx-rate',target_net:'in-target-net',pct:'in-pct',fixed:'in-fixed',fx:'in-fx',a:'in-a',b:'in-b',c:'in-c',d:'in-d'};
    Object.keys(keys).forEach(function (key) {
      const el = document.getElementById(keys[key]);
      if (el) u.searchParams.set(key, el.value);
    });
    const mor = document.getElementById('in-include-mor');
    if (mor && mor.checked) u.searchParams.set('include_mor', '1');
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(u.toString());
      btnPermalink.textContent = 'Link copied';
    } catch (e) { btnPermalink.textContent = 'Clipboard unavailable'; }
    setTimeout(function () { btnPermalink.textContent = 'Copy Permalink'; }, 2000);
  });

    function parseCsv(text) {
      const rows = []; let row = [], cell = '', quoted = false;
      text = text.replace(/^\uFEFF/, '');
      for (let i = 0; i < text.length; i++) {
        const c = text[i];
        if (c === '"') {
          if (quoted && text[i + 1] === '"') { cell += '"'; i++; }
          else quoted = !quoted;
        } else if (c === ',' && !quoted) { row.push(cell); cell = ''; }
        else if ((c === '\n' || c === '\r') && !quoted) {
          if (c === '\r' && text[i + 1] === '\n') i++;
          row.push(cell); if (row.some(v => v.trim())) rows.push(row); row = []; cell = '';
        } else cell += c;
      }
      if (quoted) throw new Error('Unclosed quoted field. Check your CSV.');
      row.push(cell); if (row.some(v => v.trim())) rows.push(row);
      return rows;
    }

  // ==========================================================================
  // ENGINE A: COUNTRY-AWARE END-TO-END PAYOUT & REVERSE INVOICE ENGINE
  // ==========================================================================
  if (toolType === 'corridor_engine') {
    const elCountry = document.getElementById('in-country');
    const elAmount  = document.getElementById('in-amount');
    const elOriginPct = document.getElementById('in-origin-pct');
    const elOriginFix = document.getElementById('in-origin-fix');
    const elTaxPct  = document.getElementById('in-tax-pct');
    const elFxRate  = document.getElementById('in-fx-rate');
    const elTargetNet = document.getElementById('in-target-net');
    const taxPresetsBox = document.getElementById('corridor-tax-presets');
    const compareBody = document.getElementById('corridor-comparison-body');

    if (params.get('country') && CALCGRID_CORRIDORS[params.get('country')]) {
      elCountry.value = params.get('country');
    }
    if (params.get('amount')) elAmount.value = params.get('amount');
    if (params.get('origin_pct')) elOriginPct.value = params.get('origin_pct');
    if (params.get('origin_fix')) elOriginFix.value = params.get('origin_fix');
    if (params.get('target_net')) elTargetNet.value = params.get('target_net');
    if (params.get('tax')) elTaxPct.value = params.get('tax');

    document.querySelectorAll('.origin-preset-chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        elOriginPct.value = chip.getAttribute('data-pct') || '0';
        elOriginFix.value = chip.getAttribute('data-fix') || '0';
        recalcCorridor();
      });
    });

    function syncCountryPresets(initial = false) {
      const code = elCountry.value || 'AM';
      const cData = CALCGRID_CORRIDORS[code] || CALCGRID_CORRIDORS['AM'];
      if (elFxRate) {
        elFxRate.value = cData.default_fx_placeholder;
      }
      const fxHint = document.getElementById('fx-rate-hint');
      if (fxHint) fxHint.textContent = cData.fx_note;
      const caveatEl = document.getElementById('corridor-tax-caveat');
      if (caveatEl) caveatEl.textContent = cData.tax_caveat + ' (Sources: ' + cData.official_sources + ' • Model dated: ' + cData.verified_date + ')';

      if (taxPresetsBox && cData.tax_presets) {
        taxPresetsBox.innerHTML = '';
        if (cData.tax_presets.length > 0 && (!initial || !params.has('tax'))) {
          elTaxPct.value = cData.tax_presets[0].rate;
        }
        cData.tax_presets.forEach(function (tp) {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'preset-chip';
          btn.textContent = tp.label;
          btn.addEventListener('click', function () {
            elTaxPct.value = tp.rate;
            recalcCorridor();
          });
          taxPresetsBox.appendChild(btn);
        });
      }
    }

    function evalRoute(gross, originPct, originFix, rail, taxPct) {
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

      return {
        afterOrigin: afterOrigin,
        netUsdExp: netUsdExp,
        grossTurnoverTax: grossTurnoverTax,
        finalNetExp: finalNetExp,
        finalNetBest: finalNetBest,
        finalNetWorst: finalNetWorst,
        totalFeeExp: Math.max(0, gross - finalNetExp),
        effectivePct: gross > 0 ? ((gross - finalNetExp) / gross) * 100 : 0
      };
    }

    function solveReverseGross(targetNet, originPct, originFix, rail, taxPct) {
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
    }

    function recalcCorridor() {
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

      railNames.forEach(function (pair) {
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

        if (routeAvailable && (!bestAvailableResult || res.finalNetExp > bestAvailableResult.finalNetExp)) {
          bestAvailableRoute = rLabel;
          bestAvailableResult = res;
        } if (routeAvailable && Number.isFinite(revGross) && revGross < bestAvailableReverse) {
          bestAvailableReverse = revGross;
        }

        const rangeStr = fmtMoney(res.finalNetWorst) + ' – ' + fmtMoney(res.finalNetBest);
        const localStr = Math.round(localNet).toLocaleString('en-US') + ' ' + cData.currency;

        currentCsvRows.push([
          cData.name, cData.currency, rLabel, routeStatus,
          gross.toFixed(2), res.finalNetExp.toFixed(2), rangeStr,
          localStr, res.effectivePct.toFixed(2) + '%', revGross.toFixed(2)
        ]);

        if (compareBody) {
          const badgeClass = routeAvailable ? 'badge-ok' : 'badge-alert';
          const tr = document.createElement('tr');
          tr.innerHTML =
            '<td><strong>' + rLabel + '</strong><br/><span class="' + badgeClass + '">' + routeStatus + '</span><div style="font-family:var(--font-sans);font-size:0.72rem;color:var(--ink-secondary);margin-top:4px">' + rail.note + '</div></td>' +
            '<td><strong>' + fmtMoney(res.finalNetExp) + '</strong><br/><span style="font-size:0.68rem;color:var(--ink-muted)">' + localStr + '</span></td>' +
            '<td>' + rangeStr + '</td>' +
            '<td>' + res.effectivePct.toFixed(2) + '%</td>' +
            '<td><strong>' + fmtMoney(revGross) + '</strong></td>';
          compareBody.appendChild(tr);
        }
      });

      if (bestAvailableResult) {
        document.getElementById('out-net').textContent = fmtMoney(bestAvailableResult.finalNetExp);
        document.getElementById('out-best-rail').textContent = bestAvailableRoute + ' (' + cData.name + ')';
        document.getElementById('out-range').textContent = fmtMoney(bestAvailableResult.finalNetWorst) + ' to ' + fmtMoney(bestAvailableResult.finalNetBest);
        document.getElementById('out-local').textContent = Math.round(bestAvailableResult.finalNetExp * fxRate).toLocaleString('en-US') + ' ' + cData.currency;
        document.getElementById('out-fee').textContent = fmtMoney(bestAvailableResult.totalFeeExp) + ' (' + bestAvailableResult.effectivePct.toFixed(2) + '%)';
        document.getElementById('out-reverse').textContent = fmtMoney(bestAvailableReverse);
      }
    }

    if (elCountry) {
      elCountry.addEventListener('change', function () {
        syncCountryPresets();
        recalcCorridor();
      });
    }
    [elAmount, elOriginPct, elOriginFix, elTaxPct, elFxRate, elTargetNet].forEach(function (el) {
      if (el) el.addEventListener('input', recalcCorridor);
    });

    const morChoice = document.getElementById('in-include-mor');
    if (morChoice) {
      if (params.has('include_mor')) morChoice.checked = params.get('include_mor') === '1';
      morChoice.addEventListener('change', recalcCorridor);
    }
    syncCountryPresets(true);
    if (params.get('fx_rate')) elFxRate.value = params.get('fx_rate');
    recalcCorridor();
  }

  // ==========================================================================
  // ENGINE B: PRIVATE BROWSER CSV TRANSACTION & HIDDEN FX AUDITOR
  // ==========================================================================
  if (toolType === 'csv_auditor') {
    const csvInput = document.getElementById('csv-audit-input');
    const fileInput = document.getElementById('csv-file-upload');
    const auditBody = document.getElementById('csv-audit-body');
    const btnRunAudit = document.getElementById('btn-run-audit');

    const PUBLISHED_RATES = {
      lemonsqueezy: { pct: 5.0, fix: 0.50, fx: 1.5 },
      payoneer:     { pct: 1.0, fix: 0.00, fx: 2.0 },
      wise:         { pct: 0.65, fix: 4.14, fx: 0.0 },
      upwork_10:    { pct: 10.0, fix: 0.99, fx: 0.0 },
      upwork_5:     { pct: 5.0, fix: 0.99, fx: 0.0 },
      upwork_15:    { pct: 15.0, fix: 0.99, fx: 0.0 },
      stripe_intl:  { pct: 2.9, fix: 0.30, fx: 2.5 },
      fiverr:       { pct: 20.0, fix: 1.00, fx: 0.0 }
    };

    function runBrowserCsvAudit() {
      const raw = (csvInput ? csvInput.value : '').trim();
      const message = document.getElementById('csv-audit-status');
      if (auditBody) auditBody.innerHTML = '';
      currentCsvRows = [];
      ['out-audit-gross','out-audit-net','out-audit-leakage'].forEach(function (id) { document.getElementById(id).textContent = '$0.00'; });
      document.getElementById('out-audit-alerts').textContent = '0 flagged';
      let records;
      try {
        if (raw.length > 1000000) throw new Error('Use a CSV smaller than 1 MB.');
        records = parseCsv(raw);
        if (records.length < 2) throw new Error('Add the header and at least one transaction.');
        if (records[0].map(v => v.trim().toLowerCase()).join(',') !== 'tx_id,provider,gross_usd,actual_net_usd') throw new Error('Expected header: tx_id,provider,gross_usd,actual_net_usd');
        if (records.length > 51) throw new Error('This browser auditor accepts up to 50 transactions per audit.');
        records.slice(1).forEach(function (cols, i) {
          if (cols.length !== 4) throw new Error('Row ' + (i + 2) + ': expected four fields.');
          const provider = cols[1].trim().toLowerCase();
          if (!Object.prototype.hasOwnProperty.call(PUBLISHED_RATES, provider)) throw new Error('Row ' + (i + 2) + ': unsupported provider code.');
          if (!cols[2].trim() || !cols[3].trim() || !Number.isFinite(Number(cols[2])) || !Number.isFinite(Number(cols[3])) || Number(cols[2]) < 0 || Number(cols[3]) < 0) throw new Error('Row ' + (i + 2) + ': amounts must be finite, non-negative numbers.');
        });
      } catch (e) { if (message) message.textContent = e.message; return; }
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

      records.slice(1).forEach(function (cols) {
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

        if (auditBody) {
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
        }
      });

      const effFeePct = totalGross > 0 ? ((totalGross - totalActualNet) / totalGross) * 100 : 0;
      document.getElementById('out-audit-gross').textContent = fmtMoney(totalGross);
      document.getElementById('out-audit-net').textContent = fmtMoney(totalActualNet);
      document.getElementById('out-audit-leakage').textContent = fmtMoney(totalLeakage);
      document.getElementById('out-audit-alerts').textContent = alertCount + ' flagged (' + effFeePct.toFixed(2) + '% eff. fee)';
    }

    if (fileInput) {
      fileInput.addEventListener('change', function (e) {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        if (file.size > 1000000) {
          const status = document.getElementById('csv-audit-status');
          if (status) status.textContent = 'Use a CSV smaller than 1 MB.';
          return;
        }
        const reader = new FileReader();
        reader.onload = function (ev) {
          if (csvInput) csvInput.value = String(ev.target.result || '');
          runBrowserCsvAudit();
        };
        reader.readAsText(file);
      });
    }

    if (btnRunAudit) btnRunAudit.addEventListener('click', runBrowserCsvAudit);
    if (csvInput) csvInput.addEventListener('input', runBrowserCsvAudit);
    runBrowserCsvAudit();
  }

  // ==========================================================================
  // ENGINE C: STANDARD FEE & REVERSE INVOICE CALCULATORS (10 TOOLS)
  // ==========================================================================
  if (toolType === 'fee_calc') {
    const elAmt = document.getElementById('in-amount');
    const elPct = document.getElementById('in-pct');
    const elFix = document.getElementById('in-fixed');
    const elFx  = document.getElementById('in-fx');
    const matrixBody = document.getElementById('sensitivity-matrix-body');

    if (params.get('amount')) elAmt.value = params.get('amount');
    if (params.get('pct')) elPct.value = params.get('pct');
    if (params.get('fixed')) elFix.value = params.get('fixed');
    if (params.get('fx')) elFx.value = params.get('fx');

    document.querySelectorAll('.preset-chip').forEach(function (chip) {
      chip.addEventListener('click', function () {
        const pctVal = chip.getAttribute('data-pct');
        if (pctVal !== null && elPct) {
          elPct.value = pctVal;
          recalcFee();
        }
      });
    });

    function calcSingleTier(gross, pct, fix, fx) {
      const totalPctRate = Math.min(1, Math.max(0, (pct + fx) / 100));
      const totalFee = gross * totalPctRate + fix;
      const net = Math.max(0, gross - totalFee);
      const effectiveRate = gross > 0 ? (totalFee / gross) * 100 : 0;
      const reverseGross = totalPctRate >= 1 ? NaN : (gross + fix) / (1 - totalPctRate);
      return { gross: gross, fee: totalFee, net: net, rate: effectiveRate, reverse: reverseGross };
    }

    function recalcFee() {
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

      if (matrixBody) {
        matrixBody.innerHTML = '';
        tiers.forEach(function (tAmt) {
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
        });
      }
    }


    [elAmt, elPct, elFix, elFx].forEach(function (el) {
      if (el) el.addEventListener('input', recalcFee);
    });
    recalcFee();
  }

  // ==========================================================================
  // ENGINE D: SAAS & OPERATIONS UNIT ECONOMICS MODELS (9 TOOLS)
  // ==========================================================================
  if (toolType === 'saas_calc') {
    const elA = document.getElementById('in-a');
    const elB = document.getElementById('in-b');
    const elC = document.getElementById('in-c');
    const elD = document.getElementById('in-d');

    if (params.get('a')) elA.value = params.get('a');
    if (params.get('b')) elB.value = params.get('b');
    if (params.get('c')) elC.value = params.get('c');
    if (params.get('d')) elD.value = params.get('d');

    function recalcSaas() {
      const a = Math.max(0, parseFloat(elA.value) || 0);
      const b = Math.max(0, parseFloat(elB.value) || 0);
      const c = Math.max(0, parseFloat(elC.value) || 0);
      const d = Math.max(0, parseFloat(elD.value) || 0);
      const mode = cfg.mode || 'ltv';
      function invalid(message) {
        document.getElementById('lbl-r1').textContent = 'Check model inputs';
        document.getElementById('val-r1').textContent = '—';
        const status = document.getElementById('model-status');
        if (status) status.textContent = message;
        document.getElementById('val-r2').textContent = '—';
        document.getElementById('val-r3').textContent = '—';
        currentCsvRows = [];
      }
      if ([elA,elB,elC,elD].some(el => !el.value.trim() || !Number.isFinite(Number(el.value)) || Number(el.value) < 0)) { invalid('Use finite, non-negative inputs.'); return; }
      const status = document.getElementById('model-status');
      if (status) status.textContent = '';
      const percentages = {ltv:[b,c], ad_rev:[d], ecom:[d], email_roi:[b,c], cro:[b,c], hourly_rate:[d], llm_cost:[d]};
      if ((percentages[mode] || []).some(v => v > 100)) { invalid('Percentages must be 0–100.'); return; }
      if (mode === 'roas' && a <= 0) { invalid('Use a positive sale price.'); return; }
      if (mode === 'pert' && !(a <= b && b <= c)) { invalid('Use optimistic ≤ likely ≤ pessimistic.'); return; }

      let r1Label = 'Primary Metric', r1Val = '$0.00';
      let r2Label = 'Secondary Metric', r2Val = '0';
      let r3Label = 'Efficiency Benchmark', r3Val = '0';

      if (mode === 'ltv') {
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
      } else if (mode === 'roas') {
        const margin = a - b;
        const marginPct = a > 0 ? margin / a : 0;
        const beRoas = 1 / marginPct;
        const grossRev = c * d;
        const orders = a > 0 ? grossRev / a : 0;
        const netProfit = orders * margin - c;
        r1Label = 'Break-Even ROAS Required';
        r1Val = margin <= 0 || a <= 0 ? 'Not achievable' : beRoas.toFixed(2) + 'x';
        r2Label = 'Break-Even CPA Ceiling';
        r2Val = fmtMoney(Math.max(0, margin));
        r3Label = 'Estimated Monthly Net Profit';
        r3Val = fmtMoney(netProfit);
      } else if (mode === 'ad_rev') {
        const monthlyImps = a * 30 * b;
        const grossRev = (monthlyImps / 1000) * c;
        const netRev = grossRev * (d / 100);
        r1Label = 'Estimated Monthly Net Ad Revenue';
        r1Val = fmtMoney(netRev);
        r2Label = 'Monthly Paid Ad Impressions';
        r2Val = Math.round(monthlyImps).toLocaleString('en-US');
        r3Label = 'Annual Run-Rate';
        r3Val = fmtMoney(netRev * 12);
      } else if (mode === 'ecom') {
        const fee = a * (d / 100);
        const net = a - b - c - fee;
        const marginPct = a > 0 ? (net / a) * 100 : 0;
        r1Label = 'Net Profit Per Order';
        r1Val = fmtMoney(net);
        r2Label = 'Net Profit Margin (%)';
        r2Val = marginPct.toFixed(1) + '%';
        r3Label = 'Profit on 100 Orders';
        r3Val = fmtMoney(net * 100);
      } else if (mode === 'email_roi') {
        const clicks = a * (b / 100);
        const sales = clicks * (c / 100);
        const profit = sales * d;
        r1Label = 'Contribution Before Campaign Costs';
        r1Val = fmtMoney(profit);
        r2Label = 'Estimated Conversions';
        r2Val = sales.toFixed(1) + ' sales';
        r3Label = 'Contribution Per Subscriber';
        r3Val = fmtMoney(a > 0 ? profit / a : 0);
      } else if (mode === 'cro') {
        const extraSales = a * ((c - b) / 100);
        const monthlyLift = extraSales * d;
        r1Label = 'Monthly Revenue Lift';
        r1Val = fmtMoney(monthlyLift);
        r2Label = 'Annual Revenue Impact';
        r2Val = fmtMoney(monthlyLift * 12);
        r3Label = 'Extra Monthly Customers';
        r3Val = (extraSales >= 0 ? '+' : '') + extraSales.toFixed(1);
      } else if (mode === 'hourly_rate') {
        if (d >= 100 || c <= 0) { invalid('Use hours > 0 and deductions < 100%.'); return; }
        const grossNeeded = (a + b) / (1 - d / 100);
        const annualBillableHours = c * 48;
        const hourly = grossNeeded / annualBillableHours;
        r1Label = 'Minimum Billable Hourly Rate';
        r1Val = fmtMoney(hourly) + '/hr';
        r2Label = 'Recommended Day Rate (8h)';
        r2Val = fmtMoney(hourly * 8) + '/day';
        r3Label = 'Required Gross Annual Billings';
        r3Val = fmtMoney(grossNeeded);
      } else if (mode === 'pert') {
        const expected = (a + 4 * b + c) / 6;
        const sd = (c - a) / 6;
        const safeHours = expected + 2 * sd;
        r1Label = 'Quote With 2σ Planning Buffer';
        r1Val = safeHours.toFixed(1) + 'h (' + fmtMoney(safeHours * d) + ')';
        r2Label = 'PERT Expected Average';
        r2Val = expected.toFixed(1) + ' hours';
        r3Label = 'Additional 2σ Hours';
        r3Val = '+' + (2 * sd).toFixed(1) + ' hours';
      } else if (mode === 'llm_cost') {
        const monthlyTokens = a * 30 * b;
        const rawCost = (monthlyTokens / 1000000) * c;
        const netCost = rawCost * (1 - d / 100);
        r1Label = 'Estimated Monthly API Cost';
        r1Val = fmtMoney(netCost);
        r2Label = 'Total Monthly Tokens';
        r2Val = (monthlyTokens / 1000000).toFixed(2) + 'M tokens';
        r3Label = 'Cost Per 1,000 User Requests';
        r3Val = fmtMoney((b / 1000) * c * (1 - d / 100));
      }

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
    }


    [elA, elB, elC, elD].forEach(function (el) {
      if (el) el.addEventListener('input', recalcSaas);
    });
    recalcSaas();
  }

  // ==========================================================================
  // ENGINE E: DEVELOPER & DATA INSTRUMENTS (11 TOOLS)
  // ==========================================================================
  if (toolType === 'dev_tool') {
    const inputEl = document.getElementById('dev-input');
    const outputEl = document.getElementById('dev-output');
    const runBtn = document.getElementById('btn-run-dev');
    const copyBtn = document.getElementById('btn-copy-dev');

    function runDevTransform() {
      const val = inputEl.value;
      const mode = cfg.dev_mode;
      try {
        if (mode === 'json_to_ts') {
          const obj = JSON.parse(val);
          if (obj === null || Array.isArray(obj) || typeof obj !== 'object') throw new Error('Use a JSON object at the root.');
          function ts(v) {
            if (v === null) return 'null';
            if (Array.isArray(v)) return v.length ? '(' + [...new Set(v.map(ts))].join(' | ') + ')[]' : 'unknown[]';
            if (typeof v === 'object') return '{ ' + Object.entries(v).map(([k,x]) => JSON.stringify(k) + ': ' + ts(x)).join('; ') + ' }';
            return typeof v;
          }
          function zod(v) {
            if (v === null) return 'z.null()';
            if (Array.isArray(v)) { const types = [...new Set(v.map(zod))]; return 'z.array(' + (types.length > 1 ? 'z.union([' + types.join(', ') + '])' : types[0] || 'z.unknown()') + ')'; }
            if (typeof v === 'object') return 'z.object({ ' + Object.entries(v).map(([k,x]) => '[' + JSON.stringify(k) + ']: ' + zod(x)).join(', ') + ' })';
            return 'z.' + typeof v + '()';
          }
          outputEl.textContent = 'export interface GeneratedPayload {\n' + Object.entries(obj).map(([k,v]) => '  ' + JSON.stringify(k) + ': ' + ts(v) + ';').join('\n') + '\n}\n\nimport { z } from "zod";\nexport const GeneratedSchema = ' + zod(obj) + ';';
        } else if (mode === 'cron') {
          const parts = val.trim().split(/\s+/);
          const limits = [[0,59],[0,23],[1,31],[1,12],[0,7]];
          const valid = parts.length === 5 && parts.every((field,i) => field.split(',').every(piece => {
            const split = piece.split('/');
            if (split.length > 2 || (split.length === 2 && (!/^\d+$/.test(split[1]) || !Number.isSafeInteger(Number(split[1])) || Number(split[1]) < 1))) return false;
            if (split[0] === '*') return true;
            if (!/^\d+(?:-\d+)?$/.test(split[0])) return false;
            const ends = split[0].split('-').map(Number);
            return ends.every(n => n >= limits[i][0] && n <= limits[i][1]) && (ends.length === 1 || ends[0] <= ends[1]);
          }));
          if (!valid) throw new Error('Use five numeric cron fields with valid ranges, lists, * and positive steps. Named months/weekdays and extensions are not supported.');
          outputEl.textContent = 'Valid 5-Field Cron Schedule:\n' + ['Minute','Hour','Day of Month','Month','Day of Week'].map((label,i) => label + ': ' + parts[i]).join('\n') + '\nTimezone is set by your scheduler; execution dates are not predicted.';
        } else if (mode === 'jwt') {
          const segs = val.trim().split('.');
          if (segs.length < 2) {
            outputEl.textContent = 'Expected JWT format: header.payload.signature';
          } else {
            const decodeB64 = function (s) {
              const binary = atob(s.replace(/-/g, '+').replace(/_/g, '/'));
              return JSON.parse(new TextDecoder().decode(Uint8Array.from(binary, c => c.charCodeAt(0))));
            };
            const header = decodeB64(segs[0]);
            const payload = decodeB64(segs[1]);
            outputEl.textContent =
              '// DECODED ONLY — SIGNATURE NOT VERIFIED\n// JWT HEADER:\n' + JSON.stringify(header, null, 2) +
              '\n\n// JWT PAYLOAD CLAIMS:\n' + JSON.stringify(payload, null, 2);
          }
        } else if (mode === 'sql') {
          const segments = val.split(/('(?:''|[^'])*'|"(?:""|[^"])*"|`[^`]*`|--[^\n]*(?:\n|$)|\/\*[\s\S]*?\*\/)/g);
          outputEl.textContent = segments.map((part,i) => i % 2 ? part : part.replace(/\s+/g, ' ').replace(/\b(SELECT|FROM|INNER JOIN|LEFT JOIN|RIGHT JOIN|WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|INSERT INTO|VALUES|UPDATE|SET|DELETE FROM)\b/gi, m => '\n' + m.toUpperCase())).join('').trim();
        } else if (mode === 'base64') {
          const operation = document.getElementById('dev-operation');
          const action = operation ? operation.value : 'encode';
          if (action === 'decode-url') outputEl.textContent = decodeURIComponent(val);
          else if (action === 'decode') {
            const bin = atob(val.trim().replace(/-/g, '+').replace(/_/g, '/'));
            outputEl.textContent = new TextDecoder('utf-8', {fatal:true}).decode(Uint8Array.from(bin, c => c.charCodeAt(0)));
          } else {
            const bytes = new TextEncoder().encode(val); let bin = '';
            bytes.forEach(b => { bin += String.fromCharCode(b); });
            const b64 = btoa(bin);
            outputEl.textContent = 'Base64 Encoded:\n' + b64 + '\n\nBase64Url Encoded:\n' + b64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '') + '\n\nURL-Encoded:\n' + encodeURIComponent(val);
          }
        } else if (mode === 'csv_to_json') {
          const records = parseCsv(val);
          if (!records.length) outputEl.textContent = '[]';
          else {
            const headers = records[0].map(h => h.trim());
            if (headers.some(h => !h) || new Set(headers).size !== headers.length) throw new Error('Headers must be unique and non-empty.');
            const data = records.slice(1).map((cells,i) => {
              if (cells.length !== headers.length) throw new Error('Row ' + (i + 2) + ': column count differs from header.');
              const row = Object.create(null);
              headers.forEach((h,j) => {
                const raw = cells[j];
                if (raw === 'true' || raw === 'false') row[h] = raw === 'true';
                else if (/^[+-]?(?:0|[1-9]\d*)(?:\.\d+)?(?:e[+-]?\d+)?$/i.test(raw) && Number.isFinite(Number(raw))) row[h] = Number(raw);
                else row[h] = raw;
              }); return row;
            }); outputEl.textContent = JSON.stringify(data,null,2);
          }
        } else if (mode === 'regex') {
          const re = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|#INV-\d+/g;
          const matches = Array.from(val.matchAll(re)).map(function (m) {
            return 'Match: "' + m[0] + '" at index ' + m.index;
          });
          outputEl.textContent = matches.length ? matches.join('\n') : 'No matches found.';
        } else if (mode === 'svg') {
          const clean = val.trim().replace(/\s+/g, ' ');
          const dataUri = 'data:image/svg+xml;utf8,' + encodeURIComponent(clean);
          const jsx = clean.replace(/stroke-width=/g, 'strokeWidth=').replace(/class=/g, 'className=');
          outputEl.textContent =
            '/* CSS Background Data URI */\nbackground-image: url("' + dataUri + '");\n\n/* React JSX */\n' + jsx;
        } else if (mode === 'password') {
          const len = Math.min(64, Math.max(8, parseInt(val, 10) || 24));
          const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+';
          const rnd = new Uint32Array(len);
          const limit = Math.floor(4294967296 / chars.length) * chars.length;
          let out = '';
          while (out.length < len) {
            window.crypto.getRandomValues(rnd);
            for (const n of rnd) if (n < limit && out.length < len) out += chars[n % chars.length];
          }
          const entropy = (len * Math.log2(chars.length)).toFixed(1);
          outputEl.textContent = 'Generated Key: ' + out + '\nEntropy:       ' + entropy + ' bits (Cryptographically Secure)';
        } else if (mode === 'markdown') {
          const htmlOut = val
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/^- (.*$)/gm, '<li>$1</li>');
          outputEl.textContent = htmlOut;
        } else if (mode === 'utm') {
          const p = val.split('|').map(s => s.trim());
          const u = new URL(p[0] || 'https://example.com');
          if (!['https:','http:'].includes(u.protocol)) throw new Error('Use an HTTP or HTTPS URL.');
          ['source','medium','campaign'].forEach((key,i) => u.searchParams.set('utm_' + key, (p[i+1] || ['newsletter','email','launch'][i]).toLowerCase()));
          outputEl.textContent = u.toString();
        }
      } catch (err) {
        outputEl.textContent = 'Error: ' + err.message;
      }
    }

    if (runBtn) runBtn.addEventListener('click', runDevTransform);
    if (inputEl) inputEl.addEventListener('input', runDevTransform);
    const operation = document.getElementById('dev-operation');
    if (operation) operation.addEventListener('change', runDevTransform);
    if (copyBtn) {
      copyBtn.addEventListener('click', async function () {
        try {
          if (!navigator.clipboard) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(outputEl.textContent);
          copyBtn.textContent = 'Copied';
        } catch (e) { copyBtn.textContent = 'Clipboard unavailable'; }
        setTimeout(function () { copyBtn.textContent = 'Copy Output'; }, 1500);
      });
    }
    runDevTransform();
  }
})();