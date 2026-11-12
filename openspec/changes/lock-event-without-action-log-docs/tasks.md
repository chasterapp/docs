# Tasks

## 1. Confirm the shipped server

- [ ] 1.1 Read chaster `main` from a private scratch clone or `gh api` (not `/home/chasterdev/projects/chaster`). Record the docs and chaster refs in a new `verification.md`. If chaster `main` moved past `57583809953`, run `git log 57583809953..origin/main -- <Sources paths>` and check for changes.
- [ ] 1.2 Read every file in `design.md` Sources and write a claim trace table in `verification.md`: claim, page and section, chaster file and function. Settle the open points: when `user` is `null`, what `role: user` means, which partner endpoints hit the 2 MB cap. Drop or fix any claim the code does not support and note differences on the issue.

## 2. Write the pages

- [ ] 2.1 `docs/api/extensions-api/extension-communication/lock-events.mdx` per design decision 1. Verify: `grep -n actionLog` on the page shows only the `action_log.created` references in the warning; the example and table list `role`, `user`, `createdAt`; `bash .claude/hooks/lint-docs.sh <file>` passes.
- [ ] 2.2 `docs/api/extensions-api/create-your-extension/webhooks.mdx` per decision 2. Verify: no sentence says `lock_event.created` carries `actionLog`; the header table still maps `lock_event.created` to `data.eventId`; lint passes.
- [ ] 2.3 `docs/api/changelog.mdx` per decision 3, dated the apply day. Verify: the entry lists the `actionLog` removal, the 2 MB cap and the `offerToken` line; every "Documentation:" link resolves; lint passes.
- [ ] 2.4 Wording check on the diff: `git diff main -- docs | grep -n -i -e previously -e "used to" -e "no longer" -e "before"` shows nothing in added lines that describes a past state; no em dash (U+2014) in added lines.

## 3. Verify and hand off

- [ ] 3.1 Run `npm run lint:docs`, `git diff --check`, and `npx openspec validate lock-event-without-action-log-docs --strict` if available. Record commands and results in `verification.md`. Existing warnings on untouched pages are out of scope.
- [ ] 3.2 Commit and push the issue-owned paths. Then build under the host lock (`npm ci` first if `node_modules` is missing): `flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m env NODE_OPTIONS=--max-old-space-size=3072 npm run build`. Fix new broken-link or anchor warnings. Record the tested commit and result.
- [ ] 3.3 Serve the build on a free port other than 3000 and 3001 (for example `npm run serve -- --host 127.0.0.1 --port 4021`), open both pages and the changelog, check the Mermaid diagram, the tables and the anchors, then stop the server. Record observations in `verification.md`.
- [ ] 3.4 Put the claim trace in the PR description, flip the stage marker, push, and hand the same issue, branch and PR to the Reviewer. QA: none. Remind the merger to set the changelog date to the merge day.
