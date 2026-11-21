# Proposal

## Why

The merged partner API accepts experimental AI reviews and can report an unavailable result. Public guides still describe only human reviews. Extension authors need accurate examples and a clear warning before sending intimate images for external AI processing.

## What changes

- Document `visibility: "ai"` for built-in and generic checks, request-time wearer OR keyholder cohort eligibility, 403 before review/media-state consumption and the unchanged keyholder 409.
- Add unavailable history and callback examples for `provider_error` and `eligibility_revoked`, with zero counts and the exact merged field placement. Keep existing verified/rejected examples and generic reason/source semantics.
- Explain bounded processing retries, no automatic human fallback, ambiguous creation POST risks and backend model selection.
- Add experimental external AI and punishment-risk disclosures to partner integration and applicable native Verification Picture/Tasks guides. Require an equivalent warning before capture in partner-owned interfaces.
- Verify examples against the tested core bundle and compatible SDK facade; run per-file lint, the Docusaurus build, link checks and rendered disclosure inspection.

## Capabilities

### New capabilities

None. This documents delivered behavior; `.openspec.yaml` sets `skip_specs: true`.

### Modified capabilities

None. No runtime or API requirement changes.

## Impact

Repository: `chasterapp/docs`. Planned public edits are limited to `docs/api/extensions-api/create-your-extension/{peer-verifications,webhooks}.mdx`, `docs/api/extensions-api/interact-with-extensions/verification-picture.mdx` and `docs/extensions/{verification-picture,tasks}.mdx`. Planning and verification records stay outside the public `docs/` tree. No new dependencies, sidebar entries, backend/SDK changes, application UI, deployment, publication or cohort activation.

This is the Docs carrier CHA-1099 for T03 / CHA-1096, authorized by CHA-1097. The canonical T03 scope at Core `f94b3de4127b0067d5dea881026fcfbfef88faee` and approved P01-P04 / D01-D05 remain unchanged. Core PR #981 merged at `b8dcc69487d389aab787acc699ec0ddc42a549f6`; the Founding Engineer released this carrier's prerequisite edges.

Sensitive surfaces: public API/webhook/SDK examples, intimate-media disclosure, punishment descriptions and public product copy. Apply the current user-authored company merge policy with Reviewer approval and green CI; this proposal grants no exception. QA: none for the approved documentation scope. Founding Engineer owns final compatibility across repositories; this carrier cannot certify all T03 behavior or authorize AI enablement.
