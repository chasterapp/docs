# Proposal

## Why

The Chaster server now checks granular OAuth scopes such as `locks:read` and `locks:write` on every public endpoint. The public scopes page still lists five all-or-nothing scopes and says `profile` gives access to the email address, which is no longer true. App developers need a page that matches the shipped server: which scopes exist, what each one allows, that email and phone are never shared, which endpoints stay reserved for the Chaster app, and how the developer token behaves. They also need one page that explains what changed and what they must do.

## What changes

- Rewrite `docs/api/reference/scopes.mdx` from the approved scope catalog and the shipped server: the read and write rule, the full catalog, the legacy scopes that keep working, endpoints that need no scope, email and phone, endpoints reserved for the Chaster app, and the developer token.
- Add `docs/api/reference/oauth-scopes-update.mdx`, a "Changes" page built from the project's API changelog: new scopes, endpoints that changed scope, newly available, deprecated and removed endpoints, and the action list for existing apps.
- Add the new page to the Reference group in `sidebars.json`, after Scopes.
- Narrow consistency edits so the API pages agree with the new reference: the per-area `Scope:` lines in `docs/api/basics/getting-started.mdx` and the "Application scopes" paragraph in `docs/api/public-api/developer-token.mdx`.

## Capabilities

### New capabilities

None. This change documents shipped behavior and sets `skip_specs: true`.

### Modified capabilities

None. No API or runtime requirement changes.

## Impact

Repository: `chasterapp/docs`, default branch `main`. Changes are limited to the four pages above, `sidebars.json` and this OpenSpec change. No server, client, Keycloak, consent-screen or localization work. Publishing the site is the founder's step after T05 deploys (project roadmap, Human checklist).

Runtime flag: none. The server change rolls out by deploy (project `design.md`, Rollout and rollback); this page only describes it.

Sensitive surfaces: public developer documentation and product copy, published to API users; it describes auth/authz behavior and the public API contract. Content rules for this page are recorded on the Paperclip issue (CHA-1412) and are part of the acceptance criteria.

Merge: autonomous, decided by the founder on CHA-1406 (2026-10-25) after the docs site build passes. The normal Reviewer pass still applies. QA: required (build the site locally, open the scopes page and the changes page, check every shipped `AppScope` value is listed and there is no `email` or `phone` scope).

Canonical scope: [T06](https://github.com/chasterapp/chaster/blob/40320a552/docs/projects/granular-oauth-scopes/epics/E02-granular-scopes/T06-public-scopes-docs.md), the approved project [design](https://github.com/chasterapp/chaster/blob/40320a552/docs/projects/granular-oauth-scopes/design.md) and decisions D01 to D09. T05 is merged on Core `main` (`eea7b79`, #1558).
