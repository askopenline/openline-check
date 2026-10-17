# Openline eSIM Compatibility

Openline's searchable reference for eSIM-capable device families, model codes, and regional variants. Maintained by [Openline](https://openline.com) in [askopenline/openline-check](https://github.com/askopenline/openline-check).

## Scope

This static application helps customers find a device and read its recorded compatibility notes. It provides search and filtering, a standalone interface, and an embeddable modal preview without a backend or build step.

The catalogue contains generated and curated entries, including records marked as unverified. A matching row is not a guarantee that a particular handset, firmware version, carrier-locked device, or Openline plan will work; confirm the exact model and regional variant before purchase.

## Repository guide

| File | Purpose |
| --- | --- |
| [`devices.js`](devices.js) | Device records and compatibility notes |
| [`app.js`](app.js) | Search, aliases, ranking, filters, and interface behavior |
| [`index.html`](index.html) | Standalone application |
| [`modal-preview.html`](modal-preview.html) | Embedding reference |
| [`style.css`](style.css) | Application-specific presentation |
| [`scripts/`](scripts/) | Historical catalogue-generation and search-audit tools |
| [`LICENSE`](LICENSE) | MIT license and original copyright notice |

## Run locally

```sh
git clone https://github.com/askopenline/openline-check.git
cd openline-check
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [the local application](http://127.0.0.1:8000) or [the modal preview](http://127.0.0.1:8000/modal-preview.html). No package installation is needed to serve the existing site.

## Maintain the catalogue

Each record includes `brand`, `name`, `model`, `year`, `esim`, and an optional `note`. Treat the manufacturer model code and regional restrictions as material data, not interchangeable labels.

- **Evidence:** Prefer manufacturer or carrier documentation for the exact variant and keep the source and review date in the change record.
- **Uncertainty:** Retain unverified labels and Wi-Fi-only, regional, firmware, and carrier-lock caveats.
- **Duplicates:** Check family-level entries and model-code variants before adding another row.
- **Search QA:** Exercise exact models, model codes, common spelling errors, brand filters, negative results, and the mobile layout.
- **Generator safety:** Some scripts contain historical absolute workstation paths or synthesize model variants. Inspect and adapt them before use; do not regenerate and publish a catalogue without reviewing the resulting records.

Catalogue size is not the number of independently tested devices. Documentation cleanup does not validate every compatibility claim in the dataset.

## Integration and deployment

The application can be served by a static web host, with `index.html` as its entry point. Review shared stylesheet URLs and embedding behavior before integrating it into another Openline surface.

The existing preview is recorded at [openline-comp.pplx.app](https://openline-comp.pplx.app). This company repository copy does not move that hosting, update a production embed, or certify current service availability.

## Ownership and license

This is an Openline company project distributed under the [MIT license](LICENSE). The original copyright notice and historical contributor attribution remain intact; company maintenance does not remove those notices or grant rights to third-party trademarks.

Report a catalogue or interface problem through [repository issues](https://github.com/askopenline/openline-check/issues). Include the exact model code, region, supporting evidence, and the observed problem, without personal device identifiers.
