# Tasks

## 1. Confirm delivered contracts

- [x] 1.1 Refresh the three repository default refs without changing this issue branch. Compare the Core DTOs/mappers/generated client and Extensions generated contracts, validation and executable examples named in `design.md`. Record exact refs and a route/request/response field table in this change's `verification.md`; verify `_id`, cursor paging, declaration semantics and distinct history/webhook criterion counts against source.

## 2. Write the developer guides

- [x] 2.1 Add `docs/api/extensions-api/create-your-extension/files.mdx` with multipart upload, metadata read and unattached deletion examples, token/ownership boundaries, expiry, retained-media rules and errors. Verify every example against the file controller/DTO/service and SDK file smoke example; lint the page with `bash .claude/hooks/lint-docs.sh <path>`.
- [x] 2.2 Add `docs/api/extensions-api/create-your-extension/peer-verifications.mdx` with declared-kind portal/manifest examples, generic criteria/reasons, create response and saved `_id`, LockAction[] punishments, all-status filtered cursor search, audience/timing/error semantics and ambiguous-create guidance. Verify JSON/code examples against generated types and the SDK validation/smoke usage, including retired-kind history and no count/paginationLastId; lint the page.
- [x] 2.3 Extend `create-your-extension/webhooks.mdx` with the typed synthetic `peer_verification.ended` payload, creating-session-only routing, stable partner deduplication key, Chaster-owned actions and the accepted partial-action/queued-callback/lock-end limitations. Verify every field against the generated webhook model and origin listener; lint the page. Do not repeat rejection actions in the handler example or claim reliable enqueue/exactly-once delivery.

## 3. Connect the flows

- [x] 3.1 Update `sidebars.json` with both author guides and the existing native Verification Picture interaction page. Add reciprocal standalone/native links and narrow links from authentication, sessions and lock actions as appropriate. Verify each added document ID resolves to an MDX file and every added internal route/fragment exists; preserve unrelated navigation.

## 4. Verify and hand off

- [x] 4.1 Run `npm run lint:docs`, check JSON example syntax, and recheck each published example's field names, units, placeholder credentials and synthetic IDs against the recorded contracts. Record commands/results and the verified input scope in `verification.md`. Run `openspec validate extension-file-and-review-guides --strict` and `git diff --check`; resolve affected findings without expanding scope.
- [x] 4.2 Commit and push all issue-owned source/evidence paths before the docs build. Announce possible lock contention, then run the build under `flock --verbose /tmp/chaster-recovery-heavy-check.lock` with `timeout --kill-after=30s 10m` and `NODE_OPTIONS=--max-old-space-size=3072`: `npm run build`. Inspect link warnings and resolve newly introduced failures. Record the tested commit, result and relevant input scope; no full upstream test suite or frontend build is needed.
- [x] 4.3 Preview the built pages on an available non-dev-env port (for example `npm run serve -- --host 127.0.0.1 --port 4020`), verify API sidebar placement, native/standalone distinction, cross-links and readable request/response code blocks, then stop the temporary preview. Record the page/navigation observations in `verification.md`; QA remains none. Update this same draft PR's body/stage marker, push evidence and hand the same issue/branch/PR to the Simplifier with sensitive surfaces and verification results.
