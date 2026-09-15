# Openline eSIM Compatibility Check

**Live:** [openline-comp.pplx.app](https://openline-comp.pplx.app) · **Modal preview:** [openline-comp.pplx.app/modal-preview.html](https://openline-comp.pplx.app/modal-preview.html)

A fast, offline-first web app that answers one question: **does your device support eSIM?**

Type any brand, model name, or model code — even with typos — and the app tells you in a second whether Openline can activate on it, with clear regional caveats where they apply.

## What's inside

- **9,496 devices** across 174 brands, from 1983 feature phones to 2026 flagships
- **Two arcs**:
  - Arc 1 — exhaustive eSIM-compatible catalog (iPhone, Samsung Galaxy, Pixel, Watch, iPad, hotspots, wearables, vehicle telematics) with regional SKU codes
  - Arc 2 — historical archive of pre-eSIM devices (Nokia, Motorola, Sony Ericsson, Siemens, BlackBerry, CDMA-only, Windows Phone, KaiOS, feature phones)
- **Typo-tolerant fuzzy search** — Damerau-Levenshtein matching, 60+ brand aliases, smooshed-token splitting (`iphone15pro` → `iphone 15 pro`), plus/`+` qualifier boost
- **Interactive warning pills** on every row with regional caveats or data-quality issues (US: eSIM only, JP domestic band lock, CDMA legacy, Windows Phone, Unverified variant, Cross-brand model code, Model code unverified, Ambiguous name, and many more)
- **Fully responsive**, tested down to 320×568 mobile with proper 44px tap targets and bottom-sheet modal treatment
- **Zero dependencies** — vanilla HTML / CSS / JS, ~30KB gzipped

## Files

```
index.html              Main app
modal-preview.html      Standalone modal-view preview (for embedding in openline.com)
style.css               ~700-line design system, Openline orange palette
app.js                  Search pipeline, filters, stats, popovers, empty state
devices.js              Generated device database (9,496 rows)
scripts/                Python generators for the device DB and audit tooling
  build_devices*.py     Modular DB builders (Apple, Samsung, Pixel, archive brands, mass, combinatorial)
  audit_add_warnings.py Post-processes devices.js to flag suspicious entries
  audit_search.py       Python port of the JS search for offline audit / QA
```

## Running locally

No build step. Serve the folder with any static server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Regenerating the device database

```bash
cd scripts
python3 build_devices.py                 # produces base devices.js
python3 build_devices_expansion.py
python3 build_devices_wave2.py
python3 build_devices_arc1_compatible.py
python3 build_devices_arc2_archive.py
python3 build_devices_arc2_mass.py
python3 build_devices_arc2_mass2.py
python3 build_devices_arc2_combinatorial.py
python3 audit_add_warnings.py            # flags suspicious entries with warning notes
```

## Data sources

Compatibility rules synthesized from Apple, Vodafone UK, Klook, Cybernews, esim-now, mysimguide (accurate as of Aug 2026). Model-code mappings from manufacturer support pages, FCC ID databases, and public spec sheets. Regional caveats sourced from carrier documentation. **Warning tags** are heuristic and reflect data-quality flags — always verify the exact model on the manufacturer's site before purchase.

## License

MIT — see `LICENSE`.

## Credits

Built for [Openline](https://openline.com) by Paul Fleury.
