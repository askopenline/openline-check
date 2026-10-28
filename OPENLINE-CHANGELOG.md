# Openline eSIM Compatibility: Company Changelog

This changelog records the Openline-maintained company edition. Original Git history, upstream notices, and earlier source release tags are preserved rather than rewritten.

## Faster loading and full caching: 28 October 2026

Tag: `company-2026.10.28b`. Live on [check.openline.com](https://check.openline.com).

- Inter is now self-hosted and split by script, with the Latin file preloaded: no more render-blocking Google Fonts stylesheet or third-party connections.
- The catalogue ships as a compact `devices.min.js` decoded with `JSON.parse` (395 KB instead of 931 KB before compression); JavaScript and CSS are minified. The build verifies the compact catalogue decodes to exactly `devices.js`.
- Cache policy: versioned files and fonts cached for a year as immutable; flags, icons and the OG image for a week with background refresh; pages revalidated on every visit.
- A service worker makes repeat visits instant and keeps the checker usable offline.
- Cloudflare CDN switched on for `check.openline.com` (Proxied): static files are served from Cloudflare's edge worldwide; pages stay fresh from the origin. The service worker script is sent with `no-store` so it always updates.
- Cache version 26.

## French punctuation fix: 28 October 2026

- French now uses non-breaking spaces before ? ! : ; and inside « », so a question mark can no longer wrap onto its own line (e.g. the page title). Applied in `scripts/build_i18n.py` for every French string. Cache version 25.

## 33 languages: 28 October 2026

Tag: `company-2026.10.28`. Live on [check.openline.com](https://check.openline.com).

- The checker is now available in the same 33 languages as [openline.com](https://openline.com), at the same paths (`/fr/`, `/de/`, `/latam/`, `/br/`, `/tw/` …).
- A flag switcher in the top bar lists every language in its own name. It keeps the current search and remembers the choice; first-time visitors on the English home page are sent to their browser language once.
- Everything is localized: page copy, FAQ, titles and descriptions, Open Graph and JSON-LD, filters, counts with proper plural forms and local number formats, empty states, warning badges and their explanations, accessibility labels and the 404 page.
- SEO: `hreflang` alternates for every language plus `x-default`, `og:locale` alternates, and a sitemap listing all 33 pages.
- Translations were drafted with Gemini 3.7 Flash and proofread by Claude Sonnet 5.5 as a native-speaker review through OpenRouter, then checked automatically for keys, placeholders, HTML and plural forms. Source strings live in `scripts/i18n/en.json`; `scripts/translate_i18n.py` and `scripts/build_i18n.py` regenerate everything.
- Assets moved to absolute paths and the cache version is now 24.

## Search highlight fix: 26 October 2026

Tag: `company-2026.10.26`. Live on [check.openline.com](https://check.openline.com).

- Partial queries such as “iphone ma” no longer show literal `<mark>` tags in results. Highlighting now merges all match ranges on the raw text before escaping, so a short term can never match inside markup inserted for another term.

## Catalogue refresh: 24 October 2026

Tag: `company-2026.10.24b`. A data audit and update of the latest devices, live on [check.openline.com](https://check.openline.com).

- **9,906 devices** (+410) from 173 brands, **1,158 eSIM-compatible** (+112).
- **Apple rebuilt from Apple's own model tables**: iPhone 14 through iPhone 18 Pro / 18 Pro Max, iPhone 17e, iPhone Air and iPhone Duo, each with its US, Canada/Japan/Gulf, global and China model numbers; iPad Pro (M5), iPad Air (M3, M4) and iPad (A16) cellular models; Apple Watch Series 11, Series 12, SE 3, Ultra 3 and Ultra 4.
- **China mainland, Hong Kong and Macao iPhones** that use two nano-SIMs (iPhone 14–16 families, iPhone 17 / 17 Pro / 17 Pro Max China) are now marked not compatible. China models that do support eSIM (iPhone Air, 17e, 18 Pro, Duo) carry a local-rules caveat.
- **New devices** from Samsung (Galaxy Z Fold8 Ultra, Z Fold8, Z Flip8, Z TriFold, Tab S12, Watch9, Watch Ultra2, A57, A37…), Google (Pixel 11 series, Pixel 11 Pro Fold, Pixel Watch 5), OnePlus 15, Nothing Phone (3)/(4a) Pro, Xiaomi 17T, vivo X500, Motorola, Oppo, Honor, Huawei, realme, ZTE/nubia, Sony and more, checked against GSMArena spec sheets.
- **Corrections**: wrong model codes on Galaxy S26/S26+/S26 FE, Z Flip7, the Pixel 10 family and Pixel 9a, OnePlus 13R/13s/13T/Nord 5 and others; Huawei Mate 80 / 80 Pro / 80 Pro Max no longer marked eSIM; rumour-era entries (iPhone 17 Air, iPhone SE 4th gen) removed; stray backslashes in iPad names fixed; duplicated brand names (“Apple Apple Watch”) removed.
- **New warnings**: carrier watch plan (cellular smartwatches), GPS-only watches, China dual nano-SIM, China local eSIM rules, no SIM tray.
- **Search**: “oneplus” and “one plus” no longer split into “one” + “plus”; misspelled brands such as “motorolla” now match; the list opens on the newest devices.

## Production hosting: 24 October 2026

Tag: `company-2026.10.24`. The explorer moves from its preview host to the company domain.

- Live at [check.openline.com](https://check.openline.com), with the modal reference at [check.openline.com/modal-preview.html](https://check.openline.com/modal-preview.html).
- Hosted on Fly.io (`openline-check`, Paris) behind Cloudflare DNS, serving a pinned commit of this repository.
- Repository homepage, README links and page metadata (canonical, Open Graph, `@askopenline` card) now point to the company domain.
- Brand assets load from [askopenline/openline-brand-assets](https://github.com/askopenline/openline-brand-assets).
- Search and sharing: new title and description, Open Graph and X cards with a dedicated 1200×630 image, JSON-LD (Organization, WebSite, WebApplication, FAQPage), robots.txt, sitemap.xml, web manifest and self-hosted icons.
- New visible FAQ section, a branded 404 page, and shareable `?q=` search links.
- No catalogue changes in this edition.

## Company edition: 17 October 2026

Tag: `company-2026.10.17`. This edition establishes the official company presentation and repository documentation without claiming a new upstream product version.

- Added an Openline visual identity for the README, supporting guides, and social preview.
- Expanded the project overview, capabilities, workflow, setup, repository map, and operating guidance.
- Added project-specific contribution and sensitive-reporting guidance.
- Refreshed company repository descriptions, homepages, topics, and release presentation.
- Updated current README links and asset examples to the official company namespace.
- Preserved existing visibility, original history, licenses, and upstream attribution.

This edition is strictly repository-focused: no live hosting, DNS, credentials, or Notion-workspace cutover is included. A documentation edition alone does not certify every application feature or external service.

## Earlier release history

No earlier GitHub release records were present in the source inventory. Earlier development history remains available through the preserved Git commits and tags.

## Release principles

Keep release notes specific about what changed, what was checked, and what remains outside scope. Preserve original technical and legal attribution, and do not turn an illustrative state, forecast, or prototype into a verified production claim.
