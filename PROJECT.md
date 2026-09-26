# Ace Digital Services (acedigitalservicesco-clone)

## What it is
The production repo for Ace Digital Services' own homepage, and the active workspace for in-progress and delivered client website builds. GitHub remote: `acedigitalservicesco`.

## Status today (2026-09-26)
- Last commits (2026-09-21/22) are client work: Peace Traders Supply content updates, RMC-family enquiries tagged by category, an Inspiration Audio hero-image swap, and an installable "RMC Dashboard" PWA with phone notifications for new enquiries.
- Working tree clean, no uncommitted changes. Repo is 354MB on disk; 1,643 files under `work/`.
- Per this repo's own `_ops/check-box-drift.py`, this is "the repo the box is a checkout of, deploys by webhook" — i.e. pushes here go live on the ZimaOS box, unlike `ace-sites-v3/digital` (`ace-demos`), which the same script documents as having no webhook.
- Root `index.html` (the Ace Digital Services homepage) matches `ace-sites-v3/digital/index.html` almost byte-for-byte, but this copy additionally carries the canonical tag, the MC analytics tracker (`data-site="ace-digital"`), and a ProfessionalService JSON-LD block — this is the maintained/deployed copy.

## Architecture
- Plain static HTML/CSS/vanilla JS at the root; no package.json, no build tooling, no README.
- `work/<client-slug>/` — one folder per client build, each a self-contained static multi-page site (own `css/`, `img/`; several also carry their own nested `PROJECT.md`/`DESIGN.md`/`PRODUCT.md`, not touched by this task). Present: `rmc-studios`, `rmc-staging`, `inspiration-audio`, `gay-penguin-tattoo` (+ `gay-penguin-preview`), `carriage-city`, `hewitt-masonry`, `marlene-baldinger`, `peace-traders-supply`, `coach-eric-sanda`, plus `_archive/`.
- `clients/rmc/` — a deployed, installable PWA (`manifest.json` + `sw.js`), titled "Site dashboard | RMC, Inspiration Audio, Carriage City, RMC Staging": an enquiries/visitors dashboard for that business family, distinct from the in-progress builds under `work/`.
- `_ops/check-box-drift.py` (nested in this repo — distinct from the sibling `ace-sites-v3/_ops` repo) compares what's live on the ZimaOS box's `work/` against what's committed on `origin/main` of this repo and of `ace-demos`. Written after an August 2026 incident where 1,160MB / 3,452 files (mostly Lebanon Borough scraped PDFs) existed only on the box and in no repo.
- Analytics: MC tracker (`data-site="ace-digital"`) on the homepage.

## Where it's going
Not recorded in the repo.

## Key paths
- `index.html` — the deployed Ace Digital Services homepage
- `work/` — client build workspace (10 client folders, incl. a `gay-penguin-preview` variant, + `_archive/`)
- `clients/rmc/` — live, installable enquiries-dashboard PWA
- `_ops/check-box-drift.py` — box-vs-git drift detector for this repo + `ace-demos`
- `assets/` — homepage branding + work-showcase photos
