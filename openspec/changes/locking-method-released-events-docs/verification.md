# Verification

Docs `main` `d5be533`. Chaster `main` `4470c67de9fbb8ad402fe2c7742ed4514591c195` (T21 merge, chasterapp/chaster#2215); `git log 4470c67de..origin/main` on the Sources paths shows no later change (checked 2026-11-26).

## Field check

Paths relative to `server/src/modules/` on chaster `main`.

| Page statement | Proof |
| --- | --- |
| `type` is `locking_method_released` / `locking_method_released_by_support` | `extension-manifest/data/event-type-aliases.ts` (default-prefix aliases); `lock-event-delivery/jobs/fan-out-lock-event.job.integration.test.ts` asserts `data.type` for both (`it.each`) |
| Recovery row: `role: user`, `cause: recovery` | `lock/services/locking-method-release-event.service.test.ts` (`type: "locking_method_released"`, `role: "user"`, `payload: { cause: "recovery", lockingMethodKind: "combination" }`); `CAUSE_BY_TYPE` in `locking-method-release-event.service.ts` |
| Support row: `role: admin`, `cause: support` | `lock-admin/controllers/lock-admin-release-locking-method.test.ts` (`role: "admin"`, `payload: { cause: "support", lockingMethodKind: "combination" }`) |
| Support release on a locked lock also writes an `unlocked` history entry first (not a stream event type: it arrives with `type: null`) | same test: `rows(lock, "unlocked")` has length 1; `UnlockLockService`; `resolveEventType` has no alias for it |
| `lockingMethodKind` is `device`, else `combination`, else `partner`; `partner` = locking provider extension, `device` = device paired with Chaster | `lock/helpers/locking-method-kind-of.ts`; enum in `lock/models/locking-method-for-public.model.ts` |
| Payload has exactly `cause` and `lockingMethodKind` | `drain` entry payload; fan-out test asserts `payload: { cause, lockingMethodKind }` by equality |
| No list or `["*"]` receives both; a list cannot name them yet | fan-out test inserts subscriptions directly; but `isManifestId` (`extension-manifest/helpers/manifest-id.ts`) requires `<slug>.<kebab-name>` in `partner-extension-manifest.service.ts:84`, `webhook-console.service.ts:327` and `PutSessionSubscriptionsDto`, so snake_case names return `400 invalid-id` |
| A session's own list replaces the extension setting | existing page text (`Per session`) |
| Both are visible history entries (also `action_log.created`, unless `actionLogFeed` is `false`) | `action-log/data/common-actions.ts` entries (titles and templates, not hidden) |
| Recovery applies to a deserted lock | `recoverCombination` in `lock/lock.service.ts` filters `status: Deserted` |

Round 1 rework (review findings F1 to F4): the manifest instruction was removed (F1), `unlocked` reworded (F2), `device`/`partner` defined (F3), the staff-account sentence dropped as unverified (F4). The rework adds no link or heading, so the build result above still applies; `git diff --check` and the lint hook were rerun.

Example payloads are the test values; `eventId`, `seq`, `user` and dates are synthetic, in the style of the existing example.

## Checks

| Command | Result |
| --- | --- |
| `bash .claude/hooks/lint-docs.sh` on both pages | pass (one existing warning at `changelog.mdx` 2023-07-09 entry, untouched) |
| `git diff --check` | clean |
| `git diff -U0 \| grep '^+' \| grep -i -e previously -e "used to" -e "no longer" -e " now " -e DEVICES` | no match |
| `npm ci`, then `flock ... npm run build` (`NODE_OPTIONS=--max-old-space-size=3072`) | exit 0, "Generated static files", no broken link or anchor warning |
| `npx docusaurus serve --host 127.0.0.1 --port 4021` + curl | lock events page has `id="locking-method-released"`, both types and `lockingMethodKind`; changelog links to `lock-events#locking-method-released`; server stopped |

`npx prettier --check` flags `lock-events.mdx`, as it did before this change (existing table alignment); the repository has no formatter gate.

Checks: the repository has no `.github/workflows` (a `.gitlab-ci.yml` deploys the site), so the PR rollup is empty by design, as on PR #28.

The changelog heading is `2026-11-26`: the merger sets it to the merge day if that differs.
