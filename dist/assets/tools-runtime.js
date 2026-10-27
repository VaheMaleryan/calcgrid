// ============================================================================
// CalcGrid Client-Side Computation Engine, Sensitivity Matrix & CSV Exporter
// ============================================================================

(function () {
  // 1. Homepage Live Filter
  const searchInput = document.getElementById('hub-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      const q = searchInput.value.toLowerCase().trim();
      document.querySelectorAll('.tool-card').forEach(function (card) {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? 'flex' : 'none';
      });
    });
  }

  // 2. Interactive Tool Engine
  const toolContainer = document.getElementById('interactive-tool-root');
  if (!toolContainer) return;

  const toolType = toolContainer.getAttribute('data-tool-type');
  const rawConfig = toolContainer.getAttribute('data-tool-config');
  let cfg = {};
  try { cfg = JSON.parse(rawConfig); } catch (e) {}

  // Hydrate inputs from URL query string (?amount=... or ?a=...)
  const params = new URLSearchParams(window.location.search);

  function fmtMoney(n) {
    return '$' + Number(n || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  let currentCsvRows = [];

  // Bind Copy Permalink & CSV Export buttons
  const btnPermalink = document.getElementById('btn-copy-permalink');
  const btnExportCsv = document.getElementById('btn-export-csv');

  if (btnExportCsv) {
    btnExportCsv.addEventListener('click', function () {
      if (!currentCsvRows.length) return;
      const csvContent = currentCsvRows.map(function (r) { return r.join(','); }).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (window.location.pathname.split('/').pop().replace('.html', '') || 'calculation') + '-ledger.csv';
      a.click();
      URL.revokeObjectURL(url);
    });
  }

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

    // Preset chips (e.g., Upwork 0%, 5%, 10%, 15% documented & example rates)
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
      const totalPctRate = Math.min(0.99, Math.max(0, (pct + fx) / 100));
      const totalFee = gross * totalPctRate + fix;
      const net = Math.max(0, gross - totalFee);
      const effectiveRate = gross > 0 ? (totalFee / gross) * 100 : 0;
      const reverseGross = (gross + fix) / (1 - totalPctRate);
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

      // Build 6-tier sensitivity matrix + CSV export rows
      const tiers = [100, 500, 1000, 2500, 5000, 10000];
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

    if (btnPermalink) {
      btnPermalink.addEventListener('click', function () {
        const u = new URL(window.location.href);
        u.searchParams.set('amount', elAmt.value);
        u.searchParams.set('pct', elPct.value);
        u.searchParams.set('fixed', elFix.value);
        u.searchParams.set('fx', elFx.value);
        if (navigator.clipboard) navigator.clipboard.writeText(u.toString());
        btnPermalink.textContent = 'Permalink Copied';
        setTimeout(function () { btnPermalink.textContent = 'Copy Permalink'; }, 1600);
      });
    }

    [elAmt, elPct, elFix, elFx].forEach(function (el) {
      if (el) el.addEventListener('input', recalcFee);
    });
    recalcFee();
  }

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

      let r1Label = 'Primary Metric', r1Val = '$0.00';
      let r2Label = 'Secondary Metric', r2Val = '0';
      let r3Label = 'Efficiency Benchmark', r3Val = '0';

      if (mode === 'ltv') {
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
      } else if (mode === 'roas') {
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
        r1Label = 'Projected Campaign Net Profit';
        r1Val = fmtMoney(profit);
        r2Label = 'Estimated Conversions';
        r2Val = sales.toFixed(1) + ' sales';
        r3Label = 'Revenue Per Subscriber';
        r3Val = fmtMoney(a > 0 ? profit / a : 0);
      } else if (mode === 'cro') {
        const extraSales = a * ((c - b) / 100);
        const monthlyLift = extraSales * d;
        r1Label = 'Monthly Revenue Lift';
        r1Val = fmtMoney(monthlyLift);
        r2Label = 'Annual Revenue Impact';
        r2Val = fmtMoney(monthlyLift * 12);
        r3Label = 'Extra Monthly Customers';
        r3Val = '+' + extraSales.toFixed(1);
      } else if (mode === 'hourly_rate') {
        const grossNeeded = (a + b) / Math.max(0.1, 1 - d / 100);
        const annualBillableHours = Math.max(1, c * 48);
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
        r1Label = '95% Safe Quote (Hours & Price)';
        r1Val = safeHours.toFixed(1) + 'h (' + fmtMoney(safeHours * d) + ')';
        r2Label = 'PERT Expected Average';
        r2Val = expected.toFixed(1) + ' hours';
        r3Label = 'Risk Buffer (±2σ)';
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
        [a, b, c, d, '"' + r1Val + '"', '"' + r2Val + '"', '"' + r3Val + '"']
      ];
    }

    if (btnPermalink) {
      btnPermalink.addEventListener('click', function () {
        const u = new URL(window.location.href);
        u.searchParams.set('a', elA.value);
        u.searchParams.set('b', elB.value);
        u.searchParams.set('c', elC.value);
        u.searchParams.set('d', elD.value);
        if (navigator.clipboard) navigator.clipboard.writeText(u.toString());
        btnPermalink.textContent = 'Permalink Copied';
        setTimeout(function () { btnPermalink.textContent = 'Copy Permalink'; }, 1600);
      });
    }

    [elA, elB, elC, elD].forEach(function (el) {
      if (el) el.addEventListener('input', recalcSaas);
    });
    recalcSaas();
  }

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
          let ts = 'export interface GeneratedPayload {\n';
          let zod = 'import { z } from "zod";\n\nexport const GeneratedSchema = z.object({\n';
          Object.keys(obj).forEach(function (k) {
            const v = obj[k];
            const t = Array.isArray(v) ? 'any[]' : typeof v;
            ts += '  ' + k + ': ' + t + ';\n';
            const zt = Array.isArray(v) ? 'z.array(z.any())' : 'z.' + (typeof v === 'number' ? 'number()' : typeof v === 'boolean' ? 'boolean()' : 'string()');
            zod += '  ' + k + ': ' + zt + ',\n';
          });
          ts += '}\n\n';
          zod += '});';
          outputEl.textContent = ts + zod;
        } else if (mode === 'cron') {
          const parts = val.trim().split(/\s+/);
          if (parts.length !== 5) {
            outputEl.textContent = 'Invalid Cron: Expected 5 space-separated fields (Minute Hour DayOfMonth Month DayOfWeek)';
          } else {
            outputEl.textContent =
              'Valid 5-Field Cron Schedule:\n' +
              '• Minute:       ' + parts[0] + '\n' +
              '• Hour:         ' + parts[1] + '\n' +
              '• Day of Month: ' + parts[2] + '\n' +
              '• Month:        ' + parts[3] + '\n' +
              '• Day of Week:  ' + parts[4];
          }
        } else if (mode === 'jwt') {
          const segs = val.trim().split('.');
          if (segs.length < 2) {
            outputEl.textContent = 'Expected JWT format: header.payload.signature';
          } else {
            const decodeB64 = function (s) {
              return JSON.parse(atob(s.replace(/-/g, '+').replace(/_/g, '/')));
            };
            const header = decodeB64(segs[0]);
            const payload = decodeB64(segs[1]);
            outputEl.textContent =
              '// JWT HEADER:\n' + JSON.stringify(header, null, 2) +
              '\n\n// JWT PAYLOAD CLAIMS:\n' + JSON.stringify(payload, null, 2);
          }
        } else if (mode === 'sql') {
          const kw = /\b(SELECT|FROM|INNER JOIN|LEFT JOIN|RIGHT JOIN|WHERE|GROUP BY|HAVING|ORDER BY|LIMIT|INSERT INTO|VALUES|UPDATE|SET|DELETE FROM)\b/gi;
          const formatted = val
            .replace(/\s+/g, ' ')
            .replace(kw, function (m) { return '\n' + m.toUpperCase(); })
            .trim();
          outputEl.textContent = formatted;
        } else if (mode === 'base64') {
          const bytes = new TextEncoder().encode(val);
          let bin = '';
          bytes.forEach(function (b) { bin += String.fromCharCode(b); });
          const b64 = btoa(bin);
          outputEl.textContent =
            'Base64 Encoded:\n' + b64 +
            '\n\nURL-Encoded:\n' + encodeURIComponent(val);
        } else if (mode === 'csv_to_json') {
          const lines = val.trim().split(/\r?\n/).filter(Boolean);
          if (lines.length < 2) {
            outputEl.textContent = '[]';
          } else {
            const headers = lines[0].split(',').map(function (h) { return h.trim(); });
            const arr = lines.slice(1).map(function (line) {
              const cells = line.split(',').map(function (c) { return c.trim(); });
              const row = {};
              headers.forEach(function (h, i) {
                const raw = cells[i] || '';
                if (raw === 'true' || raw === 'false') row[h] = (raw === 'true');
                else if (raw !== '' && !isNaN(Number(raw))) row[h] = Number(raw);
                else row[h] = raw;
              });
              return row;
            });
            outputEl.textContent = JSON.stringify(arr, null, 2);
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
          window.crypto.getRandomValues(rnd);
          let out = '';
          for (let i = 0; i < len; i++) out += chars[rnd[i] % chars.length];
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
          const p = val.split('|').map(function (s) { return s.trim(); });
          const base = p[0] || 'https://example.com';
          const src = encodeURIComponent((p[1] || 'newsletter').toLowerCase());
          const med = encodeURIComponent((p[2] || 'email').toLowerCase());
          const cmp = encodeURIComponent((p[3] || 'launch').toLowerCase());
          outputEl.textContent = base + (base.includes('?') ? '&' : '?') +
            'utm_source=' + src + '&utm_medium=' + med + '&utm_campaign=' + cmp;
        }
      } catch (err) {
        outputEl.textContent = 'Error: ' + err.message;
      }
    }

    if (runBtn) runBtn.addEventListener('click', runDevTransform);
    if (inputEl) inputEl.addEventListener('input', runDevTransform);
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        if (navigator.clipboard) navigator.clipboard.writeText(outputEl.textContent);
        copyBtn.textContent = 'Copied';
        setTimeout(function () { copyBtn.textContent = 'Copy Output'; }, 1500);
      });
    }
    runDevTransform();
  }
})();