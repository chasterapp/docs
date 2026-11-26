# Tasks

## 1. Confirm the shipped server

- [x] 1.1 Read chaster `main` from a private clone, `gh api`, or the ticket's chaster worktree (never `~/projects/chaster`). Record the docs and chaster refs in a new `verification.md`. If chaster `main` moved past `4470c67de`, run `git log 4470c67de..origin/main -- <Sources paths>` and check for changes.
- [x] 1.2 Read every file in `design.md` Sources. Write the field check table in `verification.md`: each field and value the page states, and the T21 test file and assertion that proves it. Confirm the Locked-lock support path (an `unlocked` row is also written) and the `partner` meaning of `lockingMethodKind`. Drop or fix any claim the code does not support and note differences on the issue.

## 2. Write the pages

- [x] 2.1 `docs/api/extensions-api/extension-communication/lock-events.mdx` per design decision 1. Verify: both types, `role`, `cause` and `lockingMethodKind` values appear and match the field check table; the example payloads are the test values; `bash .claude/hooks/lint-docs.sh <file>` passes.
- [x] 2.2 `docs/api/changelog.mdx` per decision 2, dated the apply day. Verify: the entry names both types, the payload fields and the subscription rule; its "Documentation:" link points to `#locking-method-released`; lint passes.
- [x] 2.3 Wording check on the diff: `git diff origin/main -- docs | grep '^+' | grep -n -i -e previously -e "used to" -e "no longer" -e " now "` shows nothing that describes a past state; no em dash (U+2014) in added lines; no internal switch name (`DEVICES`) in page text.

## 3. Verify and hand off

- [x] 3.1 Run `npm run lint:docs` on the two pages, `git diff --check`, and `npx openspec validate locking-method-released-events-docs --strict` if available. Record commands and results in `verification.md`. Existing warnings on untouched pages are out of scope.
- [x] 3.2 Commit the issue-owned paths. Build under the host lock (`npm ci` first if `node_modules` is missing): `flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m env NODE_OPTIONS=--max-old-space-size=3072 npm run build`. Fix new broken-link or anchor warnings. Record the tested commit and result.
- [x] 3.3 Serve the build on a free port other than 3000 and 3001 (for example `npm run serve -- --host 127.0.0.1 --port 4021`), open the lock events page and the changelog, check the new tables, example and anchor, then stop the server. Record observations in `verification.md`.
- [x] 3.4 Put the field check in the PR description, flip the stage marker, push, and hand the same issue, branch and PR to the Reviewer. QA: none. Remind the merger to set the changelog date to the merge day.
