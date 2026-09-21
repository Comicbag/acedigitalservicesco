# RMC Staging, site rebuild

Preview of a rebuilt rmcstaging.com for EJ Gaub and Liz Robbins (Garwood, NJ). Second of the four
EJ/Liz sites after Inspiration Audio. Built 2026-09-20.

| | |
|---|---|
| Live preview | https://acedigitalservicesco.com/work/rmc-staging/ (noindex, preview banner) |
| Repo | Comicbag/acedigitalservicesco, `work/rmc-staging/` (deploys on push) |
| Generator | `~/ace-sites-v3/_captures/rmcstaging-current/_build/build.py` (private, not in the web root). Pages are generated; edit the generator, not the HTML. `ASSET_V=<n> python3 build.py` |
| Capture | `~/ace-sites-v3/_captures/rmcstaging-current/` (site, Facebook, Instagram, Google, directories, news, manufacturer specs); originals on the SSD `/Volumes/CoreysSSD/ace-captures/rmcstaging-current/assets` |
| Forms | quote.html posts to the RMC PocketBase `submissions` as `site: rmc-staging, kind: booking`; shows in the client dashboard Inbox |
| Design | `PRODUCT.md` and `DESIGN.md` here. Orange #fd5521 is theirs; Big Shoulders Display + Chivo |
| Sources | every fact is from rmcstaging.com, their Google listing, their Instagram, manufacturer spec sheets, or local press; the rest is a visible "Confirm with EJ" placeholder |

Pages: index, stage, truss, audio, events, gallery, about, quote, privacy, accessibility.
