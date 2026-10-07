# Proposal

## Why

Extension authors need a public guide for the delivered private-file and standalone peer-review APIs. The current native Verification Picture guide covers requesting a picture through that extension, rather than uploading an image and creating an independent review.

## What changes

- Add private extension-file and standalone peer-review guides with multipart upload, creation, all-status history search, declared kinds, generic checks and rejection-action examples.
- Extend webhook guidance with the typed `peer_verification.ended` envelope, origin-only delivery, partner deduplication and current action/delivery limitations.
- Add sidebar entries and cross-links, including the existing native Verification Picture interaction guide as a distinct flow.
- Explain ownership, expiry and retention, errors, zero-vote approval, the 75% approval threshold and keyholder review without a timeout.
- Check examples against merged Core DTOs/generated contracts and the extensions SDK/executable examples. Use synthetic IDs and placeholder credentials throughout.

## Capabilities

### New capabilities

None. This change documents existing behavior and sets `skip_specs: true`.

### Modified capabilities

None. No API or runtime requirement changes.

## Impact

Repository: `chasterapp/docs`, default branch `main`. Public source changes are limited to `docs/api/extensions-api/`, `sidebars.json` and narrowly necessary documentation verification support. No backend, SDK, interactive application, localization, analytics or live-publication work is included.

Sensitive surfaces: public developer documentation/product copy, authentication and private-media guidance, API contracts, webhook contracts and lock-action execution descriptions. The issue's explicit project-owner authorization permits automatic repository merge after normal agent review and exact-head checks. It does not authorize live deployment. QA: none; the Applier still checks built-page navigation and examples.

Canonical scope: [T10](https://github.com/chasterapp/chaster/blob/354d6256778b0c7dee5aa639d9f487456dad9ec6/docs/projects/extension-verifications/epics/E03-configure-discover-and-integrate/T10-public-developer-guides.md), approved design and decisions D01-D06. T01, T05, T06 and T07 are complete. T03/T04 contracts are also checked for creation and generic criteria.
