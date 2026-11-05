# Tasks

## 1. Confirm the shipped server

- [x] 1.1 Refresh chaster `main` in a private scratch clone (not `/home/chasterdev/projects/chaster`). Record the docs and chaster refs in this change's `verification.md`. If chaster `main` moved past `78e540eb`, check the files in `design.md` Sources for changes since then (`git log 78e540eb..origin/main -- <paths>`).
- [x] 1.2 Read every source in `design.md` Sources and record, in `verification.md`, a table: claim, page and section, source file (and function or constant). Read the `developers.json` `webhooks.*` keys and the `webhooks/` components for exact UI labels. Any claim the code does not support is fixed or dropped; any difference from `design.md` goes on the issue.

## 2. Write the pages

- [x] 2.1 `docs/api/extensions-api/create-your-extension/webhooks.mdx` per `design.md` decision 1 (11 items). Verify: the "not available yet" caution is gone; existing anchors still resolve; the seven endpoints, the four headers, the three statuses, the 5-attempt schedule, the `"test": true` flag, the 30 per minute limit and the `action_log.created` switch are on the page; `bash .claude/hooks/lint-docs.sh <file>` passes.
- [x] 2.2 `docs/api/extensions-api/extension-communication/manifest.mdx` per decision 2. Verify: the old warning "a manifest without `subscriptions` stops `lock_event.created` deliveries" is gone; `["*"]`, `wildcard-not-alone`, the first and later upload rules, the no-review rule and the session `null` rule are present; lint passes.
- [x] 2.3 `docs/api/extensions-api/extension-communication/lock-events.mdx` per decision 3. Verify: the diagram renders (task 3.2), the bullets match `LockEventSubscriptionsService.matches`, lint passes.
- [x] 2.4 `docs/api/changelog.mdx` per decision 4, dated `2026-11-05`. Verify every endpoint and header in the entry is on the webhook page and every "Documentation:" link resolves.
- [x] 2.5 Screenshots per decision 6, or record why they were skipped. Verify `npm run compress:images` ran on new images and every image reference resolves.

## 3. Verify and hand off

- [x] 3.1 Run `npm run lint:docs`, `git diff --check`, and (if available) `npx openspec validate webhook-console-public-docs --strict`. Record commands and results in `verification.md`. Existing warnings on untouched pages are out of scope.
- [ ] 3.2 Commit and push all issue-owned paths first. Then build under the host lock: `flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m env NODE_OPTIONS=--max-old-space-size=3072 npm run build` (run `npm ci` first if `node_modules` is missing). Fix new broken-link or anchor warnings. Record the tested commit and result.
- [ ] 3.3 Serve the build on a free port other than 3000 and 3001 (for example `npm run serve -- --host 127.0.0.1 --port 4021`), open the three pages and the changelog, check the Mermaid diagram, tables and anchors, then stop the server. Record observations in `verification.md`.
- [ ] 3.4 Put the claim trace (claim to chaster file on `main`) in the PR description, as the ticket's definition of done requires. Update the stage marker, push, and hand the same issue, branch and PR to the Reviewer. QA: none.
