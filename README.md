# PayoutFolio

**Know what you actually keep.** Independent browser tools for payout comparison, reverse invoice math, CSV auditing, unit economics, and developer work. Formerly CalcGrid. Repository and existing tool filenames remain compatible.

## Build and verify

Python 3.11+ and Node.js 22 are sufficient. No paid service or Python dependency is required to build the site.

```sh
python3 engine/autopilot.py --ci
python3 -m unittest discover -s tests -v
```

`engine/build_site.py` is the source of truth for the website, styles, navigation, icons, metadata and calculator runtime. `engine/catalog_data.py` preserves all 32 calculators and the five country scenarios. Rebuild generated `dist/` after changing either. `engine/brand_assets/` contains the checked-in original brand assets.

`--ci` builds and tests without video rendering or social publication. A normal local `python3 engine/autopilot.py` additionally renders the three local marketing videos. It requires macOS voice synthesis and FFmpeg for narrated media. Financial claims are checked before an episode can be queued. CI and normal local runs never publish to social platforms.

## Cloudflare Pages

Create a **Pages project with Git integration**, repository `VaheMaleryan/calcgrid`, production branch `main`, framework **None**, build command `python3 engine/autopilot.py --ci`, build output `dist`. Cloudflare runs the same mathematical, security and regression gates before publishing. A custom 404 page prevents missing or private-looking paths from falling through to a successful homepage response. GitHub Actions provides push, PR, manual and weekly checks, with no GitHub Pages deployment job and no uploaded private artifacts. Cloudflare Git integration deploys each main-branch push automatically; no recurring owner action or per-deploy token is required.

`launch_config.json` controls the brand, verified production `site_url`, and release switches. `SITE_URL` may explicitly override the canonical origin. Preview URLs never silently become canonicals. The initial rebrand keeps the last verified GitHub origin until a successful Cloudflare deployment is checked live. The production origin is changed in a separate migration commit after verification.

If a build fails, Cloudflare keeps serving the last successful deployment. `--auto-rollback` remains accepted for compatibility, but never discards local source changes. The build clears and regenerates only `dist/`, so stale files cannot leak through an incremental build.

## Private boundaries and launch controls

Never track, publish, copy into `dist/`, or upload as workflow artifacts:

- `private_products/calcgrid-pro-offline-suite.zip`
- `marketing_outbox/videos/`
- `logs/`, including `private_dashboard.html`
- `.env` files and Cloudflare credentials

The private ZIP retains its established filename and is built outside `dist/`. Source code for the site is public; this boundary prevents direct distribution of the packaged product, not reconstruction from public code. Private revenue metrics are local records and are never presented as verified sales or live analytics. The static website has no analytics receiver; no financial inputs, CSV contents or developer buffers are transmitted.

Checkout and ads require `monetization_approved: true` plus configured service details; the current release leaves approval **false** and both service fields empty. Social publishing requires an explicit enabled switch, credentials, passed claims checks, and a separately authorized publishing invocation; routine build commands leave it off. These release switches must not be enabled as a side effect of a build.

Local preview: `python3 engine/server.py` binds to `127.0.0.1:8098`. The private dashboard is available only through this local server's `/admin/dashboard` path. Do not expose this preview server publicly.

## Model limitations

All financial figures are planning estimates. Provider rates, route eligibility, FX inputs and tax regimes vary by account, date and jurisdiction. A dated assumption is not a live quote or eligibility determination. Official provider links and disclaimers are shown in the UI. The freshness check reports dated assumptions; it does not claim to perform live legal or fee verification.

Reverse calculations use the same multi-stage equation as forward payouts, including tax on the selected gross turnover base. The target solver compares all available routes and identifies impossible retention factors. The CSV auditor supports quoted CSV fields, validates provider codes and amounts, and accepts up to 50 transactions / 1 MB. A flagged variance is a difference from an example baseline, not proof of wrongdoing. Imported text is escaped; CSV exports quote fields and neutralize spreadsheet formulas.

## Naming research — 27 October 2026

FeeAtlas was rejected after finding an existing NAOHP fee-benchmarking product and another fee-research use. `feeatlas.com` is registered and offered for sale; no purchase was made. `feeatlas.io` returned no RDAP registration record, which is not a reservation or guarantee of availability.

PayoutFolio is the working replacement: exact-name web screening found no indexed exact commercial use, USPTO Wordmark queries for `PayoutFolio` and `payout folio` returned no records, and `payoutfolio.com` returned RDAP HTTP 404. This is a preliminary conflict screen, not full international or similarity-based trademark clearance. No domain has been purchased and no claim of trademark registration is made. The display name remains configurable.
