# Openline eSIM Compatibility: Company Changelog

This changelog records the Openline-maintained company edition. Original Git history, upstream notices, and earlier source release tags are preserved rather than rewritten.

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
