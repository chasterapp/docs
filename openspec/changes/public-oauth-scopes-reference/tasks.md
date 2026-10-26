# Tasks

## 1. Confirm the shipped server

- [x] 1.1 Refresh the Core `main` ref in a private scratch clone (not `/home/chasterdev/projects/chaster`). Record the docs and Core refs in this change's `verification.md`. Read the sources listed in `design.md` and record: the 24 `AppScope` values, `DEVELOPER_CLIENT_ALLOWED_SCOPES`, the client default/optional scopes, `LEGACY_SCOPE_EXPANSION`, developer token scopes and generator. If `AppScope` or any fact in `design.md` decision 1 differs from the shipped code, stop and report it on the issue instead of writing around it.
- [x] 1.2 Cross-check every endpoint named on the two pages against the handler `@ApiScope(...)` declarations (or no auth guard) in published modules at that ref. Record a table (endpoint, page claim, shipped declaration) in `verification.md`. Fix or drop any claim that does not match.

## 2. Write the pages

- [x] 2.1 Rewrite `docs/api/reference/scopes.mdx` with the eight sections in `design.md` decision 1. Keep its document ID, title and sidebar label. Verify: every one of the 24 `AppScope` values appears on the page; the strings `` `email` `` and `` `phone` `` appear only in "there is no `email` or `phone` scope" wording; `bash .claude/hooks/lint-docs.sh docs/api/reference/scopes.mdx` passes.
- [x] 2.2 Add `docs/api/reference/oauth-scopes-update.mdx` per `design.md` decision 2, from `api-changelog.md` lines 1 to 134 at Core `40320a552` only. Verify: every endpoint, scope and status code from those lines is present; no dates; the page passes the content rules on the issue; lint passes.
- [x] 2.3 Add `api/reference/oauth-scopes-update` to the Reference group in `sidebars.json`, right after `api/reference/scopes`. Verify the ID resolves to the new file and no other sidebar entry changes.
- [x] 2.4 Make the consistency edits in `design.md` decision 3 (`getting-started.mdx` scope lines, `developer-token.mdx` "Application scopes"). Verify each link target and anchor exists in the built site (task 3.2) and lint both files.

## 3. Verify and hand off

- [x] 3.1 Run `npm run lint:docs`, `openspec validate public-oauth-scopes-reference --strict` and `git diff --check`. Run the content-rule check from the issue over the diff, commit messages and PR text. Record commands and results in `verification.md`; existing warnings on untouched pages are not in scope.
- [x] 3.2 Commit and push all issue-owned paths first. Announce possible lock contention, then build under `flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m env NODE_OPTIONS=--max-old-space-size=3072 npm run build`. Resolve new broken-link or anchor warnings. Record the tested commit and result.
- [x] 3.3 Serve the build on a free port that is not 3000 or 3001 (for example `npm run serve -- --host 127.0.0.1 --port 4021`). Open the scopes page and the changes page, check the sidebar order, links and tables render, then stop the server. Record the observations in `verification.md`. Update the same draft PR's body and stage marker, push, and hand the same issue, branch and PR to the Simplifier. QA is required after review.
