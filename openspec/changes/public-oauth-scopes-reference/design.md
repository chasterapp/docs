# Design

## Context

See `proposal.md` for motivation. This Docusaurus 3 repository uses MDX frontmatter, explicit document IDs in `sidebars.json` and root-relative public routes. Its tone checker is `.claude/hooks/lint-docs.sh` (`npm run lint:docs`): headings use sentence case and prose avoids em dashes.

Verified refs on 2026-10-26:

- Docs: `4497e7f` (issue branch base).
- Core: `eea7b79541547cce938d947a77437b1d15616cc9` (`main`, includes T05 #1558).
- Planning source: Core `40320a552`, `docs/projects/granular-oauth-scopes/`. Its `design.md` and `api-changelog.md` are byte-identical on `eea7b79`.

### Sources

Read these at the Core refs above. Use a private scratch clone, never the shared human checkout.

| Fact | Source |
| --- | --- |
| Scope catalog and meaning | project `design.md`, Scope catalog; `api-changelog.md`, New scopes |
| Shipped scope values | `server/src/modules/auth/models/app-scope.model.ts` (`AppScope`, 24 values) |
| Scopes offered to developer apps | same file, `DEVELOPER_CLIENT_ALLOWED_SCOPES` (the 18 granular read/write scopes); `server/src/modules/developer/services/keycloak-client-sync.service.ts` (`profile` is a default client scope; no `email` or `phone`) |
| Legacy aliases | `server/src/modules/auth/utils/expand-scopes.ts` (`LEGACY_SCOPE_EXPANSION`) |
| Developer token scopes and generation | `server/src/modules/auth/guard/jwt-auth.guard.ts` (developer auth sets `scope: Object.values(AppScope)` and nothing else); `server/src/modules/developer/repositories/developer-token.repository.ts` (`randomBytes(32)`) |
| Per-endpoint scope | `@ApiScope(...)` on handlers in controllers of the modules listed in `includedModules` (`server/src/scripts/generate-swagger.ts`). `ApiScope` sets both the enforced scope and the OpenAPI `security` block, and `server/src/modules/auth/public-routes-scopes.test.ts` keeps them equal |
| Changes and actions for existing apps | project `api-changelog.md`, from the title through the end of the "Action needed" list (lines 1 to 134 at `40320a552`) |

The ticket also names `server/tmp/api.json` after `generate-api-clients`. That file is the web app's full client document, and generating it compiles the server. The handler-level `@ApiScope` declarations in published modules are the same data (enforced and documented scopes are equal by test), so a source cross-check is enough. Generate `api.json` only if the source check leaves a real doubt, under the heavy-check lock.

## Goals / non-goals

**Goals:** a developer can pick the least scopes their app needs, knows that email and phone are never available, knows which endpoints work without a scope and which stay reserved for the Chaster app, and can see what changed for an existing app and what to do.

**Non-goals:** no per-endpoint scope table (the OpenAPI reference lists each endpoint's scopes in `security`); no runtime, Keycloak or consent-copy change; no live publication; no new dates. The pages describe the state after T05 deploys, which is when the founder publishes them.

## Decisions

### 1. Scopes page structure (`docs/api/reference/scopes.mdx`)

Keep the document ID `api/reference/scopes`, title "OAuth scopes" and sidebar label "Scopes", so existing links keep working (`oauth-2.mdx` links to `/api/reference/scopes`). Sections, in order:

1. **Intro.** Each token holds scopes. Request only what the app uses; users see one consent line per scope. Link to the changes page.
2. **How scopes work.** Each area has a read scope and a write scope. A read scope only allows endpoints that change nothing (judged by what the endpoint does, not its HTTP method). A write scope does not include the read scope: request both if you need both. An endpoint needs every scope it lists; each endpoint's scopes are in its `security` block in the [API reference](https://api.chaster.app/api).
3. **Scope catalog.** One table with these rows, using the meanings from `api-changelog.md` New scopes:

   | Scope | Allows |
   | --- | --- |
   | `profile` | The user's id, username and avatar |
   | `profile:read` / `profile:write` | The user's own profile, settings, kink profile, stats |
   | `users:read` / `users:write` | Member search, blocks, reports |
   | `locks:read` / `locks:write` | The user's locks and their extensions |
   | `shared_locks:read` / `shared_locks:write` | The user's shared locks |
   | `keyholder:read` / `keyholder:write` | Locks the user keyholds |
   | `messaging:read` / `messaging:write` | Private conversations and attachments |
   | `notifications:read` / `notifications:write` | Notifications |
   | `calendar:read` / `calendar:write` | Calendar events |
   | `posts:read` / `posts:write` | Activity feed and keyholding request posts |
   | `developer` | Extensions API and developer extension management |

   Then state which scopes an OAuth app can request: `profile` is always included; the 18 read/write scopes are offered on the consent screen; `developer` is not offered to OAuth apps and comes only with the developer token (verify against `DEVELOPER_CLIENT_ALLOWED_SCOPES` and `keycloak-client-sync.service.ts`).
4. **Legacy scopes.** `locks`, `shared_locks`, `keyholder` and `messaging` stay valid with no end date. Each counts as its read and write pair (small table: legacy scope → pair). Apps created after the update are offered the granular scopes only; existing apps receive the granular scopes alongside their current ones. Recommend granular scopes for new work.
5. **Email and phone are never shared.** There is no `email` or `phone` scope. `GET /auth/profile` returns `email`, `billingEmail` and `phoneNumber` as `null` for every app and developer token. ID tokens and userinfo do not carry them. Profile edits (`PATCH /current-user`, `POST /auth/profile`) that change the email or phone number return `400`; other fields stay editable with `profile:write`. Identify users by their user id.
6. **Endpoints without a scope.**
   - Any valid token, no scope: public member profiles (`GET /users/profile/:username`, `/users/profile/:username/details`, `/users/profile/by-id/:userId`, `GET /user-profile/:username/*`, `GET /achievements/user/:userId`) and `POST /files/upload`.
   - Open without a token, any valid token accepted: public locks, pillory search, shared links, explore categories, the extensions list, session offer token lookup, community event categories, public Academy pages and `GET /data/countries`, `GET /data/countries/:code`.
   - Endpoints that work with or without a token check the scope when a token is sent. Example: `GET /extensions/tasks/votes/:taskVoteId` is open anonymously and needs `locks:read` with a token.
   Check each path against the shipped controllers before publishing; drop any item that does not match rather than guessing.
7. **Reserved for the Chaster app.** Only endpoints in the API reference are supported for apps. Name exactly these, from the public changelog: `GET /auth/totp/status`, `POST /auth/totp/disable` and `GET /auth/profile/update` return `403` to OAuth apps and developer tokens; `GET /users/search/by-discord-id/:discordId` is reserved for the Chaster Discord bot and returns `401`. Do not add any other examples or categories of reserved endpoints.
8. **Developer token.** It acts as the account that generated it and holds every scope in the catalog, including `developer` and the legacy scopes. It is still treated as an app token: email and phone are `null`, the reserved endpoints above stay closed, and identity edits return `400`. New tokens use a stronger random generator; existing tokens keep working. Link to `/api/public-api/developer-token`. Do not claim anything about expiry.

### 2. Changes page (`docs/api/reference/oauth-scopes-update.mdx`)

New page, title "OAuth scopes update", sidebar label "Scopes update", added to the Reference group right after `api/reference/scopes`.

Build it only from `api-changelog.md` lines 1 to 134 at `40320a552` (title through "Action needed"). Keep its structure (Part 1: security changes; Part 2: granular scopes; Action needed) and every endpoint, scope and status code in those lines. Edits allowed:

- Rewrite future and announcement wording to the present ("now return", "are no longer shared"), because the page is published after both parts are live. Drop "each announced with its date before it goes live"; add no dates.
- Link to the scopes page for the catalog instead of repeating its whole table, or keep the table: either is fine as long as all 24 values stay on the scopes page.
- Sentence-case headings and no em dashes, for the lint.

The content rules on the Paperclip issue (CHA-1412) apply to every page, this OpenSpec change, commit messages and the PR text.

### 3. Consistency edits

- `docs/api/basics/getting-started.mdx`: the `Scope:` line under Locks, Shared Locks, Keyholder and Messaging becomes the read/write pair (for example "Scopes: `locks:read`, `locks:write`") with one link to the scopes page. New apps are not offered the legacy names, so the old lines would mislead new developers. Keep the rest of the page.
- `docs/api/public-api/developer-token.mdx`, "Application scopes": replace "granted all scopes available and can use all endpoints" with the short statement from decision 1.8 and a link to `/api/reference/scopes#developer-token` (check the generated anchor). Keep the rest of the page.
- Leave `oauth-2.mdx` as is: its `scope=profile` examples stay valid and it already links to the scopes page.

## Risks / trade-offs

- **Pages describe the server before it deploys.** Accepted: merging the docs PR does not publish the site; the founder publishes after T05 deploys (roadmap). The pages carry no dates for that reason.
- **Endpoint lists drift.** The scopes page lists only the small sets that have no scope or are reserved, and points to the OpenAPI `security` blocks for everything else, so most future route changes need no docs edit.
- **Reserved list grows stale.** Decision 1.7 names only the four endpoints already announced in the public changelog and states the general rule (only endpoints in the API reference are supported), so it needs no update when other endpoints change.
