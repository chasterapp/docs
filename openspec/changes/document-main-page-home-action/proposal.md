# Proposal

## Why

Partner developers need to know which home action opened their extension so one main page can display the matching view. The main page guide currently documents only `mainToken`, leaving the existing `extensionSlug` and newly added optional `homeActionSlug` unexplained.

## What changes

- Document all three fields in the URI-encoded JSON hash in the main page guide, with an updated URL example and JavaScript that reads the clicked action and falls back to the default view when absent.
- Explain in the session metadata guide that a clicked home action's declared `slug` reaches the main page as `homeActionSlug`, with a link to the parsing example.
- Add an Extensions API changelog entry for `homeActionSlug`.
- Verify the wording against `createSessionAuth` on `chasterapp/chaster` main. Preserve the issue's requirement to merge only after a production release includes `90a4748b3135dd8d4eec207f603efc192b33e844`.

## Capabilities

### New capabilities

None. This is documentation of existing behavior; `.openspec.yaml` sets `skip_specs: true`.

### Modified capabilities

None. No runtime or API requirements change.

## Impact

Repository: `chasterapp/docs`. Public content changes are limited to `docs/api/extensions-api/create-your-extension/main-page.mdx`, `docs/api/extensions-api/create-your-extension/session-metadata.mdx`, and `docs/api/extensions-api/changelog.mdx`. Planning and verification records stay under this OpenSpec change, outside the public `docs/` tree.

Feature switch: none. Sensitive surfaces: public developer content and an authentication-related API contract. Existing token security guidance remains authoritative; the action slug selects a view and is not an authorization credential.

No backend, frontend, generated client, dependency, sidebar, media or deployment changes are needed. Preparation and review may proceed before the production release, but the docs PR must remain unmerged until release inclusion is verified. This proposal does not authorize a production rollout.
