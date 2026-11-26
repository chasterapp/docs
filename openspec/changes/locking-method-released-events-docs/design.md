# Design

## Context

See `proposal.md`. Docusaurus 3, MDX pages, root-relative links. Tone checker: `.claude/hooks/lint-docs.sh` (`npm run lint:docs`): sentence-case headings, no em dashes. Describe current behaviour only: no "previously", "used to", "no longer", "now" phrasing.

Verified refs on 2026-11-26:

- Docs: `d5be533` (`main`).
- Chaster: `4470c67de9fbb8ad402fe2c7742ed4514591c195` (`main`, the T21 merge, chasterapp/chaster#2215).

Read chaster from a private scratch clone (`git clone --depth 30 --filter=blob:none https://github.com/chasterapp/chaster`), `gh api`, or the ticket's own chaster worktree at that commit. Never the shared human checkout under `~/projects/`. The docs repository too: work in a private clone, never `~/projects/docs` (a human checkout on another branch).

### Sources

Paths are relative to `server/src/modules/` on chaster `main`. Every claim on the page comes from this table, or from another file the Applier reads and adds to the trace in `verification.md`.

| Fact | Source |
| --- | --- |
| Both rows are default-prefix history entries with titles "%USER% recovered the lock after desertion" and "Support released the locking method" (visible in the lock history) | `action-log/data/common-actions.ts` |
| `type` in `lock_event.created` is `locking_method_released` / `locking_method_released_by_support` (alias of the default-prefix name) | `extension-manifest/data/event-type-aliases.ts`, `event-type-aliases.test.ts` (22 aliases) |
| Payload is `{ cause, lockingMethodKind }`; `cause` is `recovery` for `locking_method_released`, `support` for `locking_method_released_by_support` | `lock/services/locking-method-release-event.service.ts` (`CAUSE_BY_TYPE`, `drain`) |
| `lockingMethodKind` is `device` when the lock holds a device, else `combination` when it has a combination, else `partner` | `lock/helpers/locking-method-kind-of.ts`, enum in `lock/models/locking-method-for-public.model.ts` |
| Recovery row: `role: user` (the wearer), `user` is the wearer; written once per recovery, a retry writes nothing more | `lock/lock.service.ts` (`recoverCombination`), `lock/lock.service.recovery.test.ts`, `locking-method-release-event.service.test.ts` |
| Support row: `role: admin`; on a Locked lock the lock is unlocked first (an `unlocked` row too), on another status (Unlocked, Deserted, archived) only the release row is written; once per lock | `lock-admin/services/lock-admin.service.ts` (`releaseLockingMethod`), `lock/services/unlock-lock.service.ts`, `lock-admin/controllers/lock-admin-release-locking-method.test.ts` |
| Delivery: a partner with no list receives both; a partner whose list names the type receives it; a list without it does not | `lock-event-delivery/jobs/fan-out-lock-event.job.integration.test.ts` (`it.each` over both types) |
| `data` fields and `user` shape are the generic `LockEventDto` already documented on the page | `lock-event-delivery/mappers/lock-event.mapper.ts`, `lock-event-delivery/dto/lock-event.dto.ts` |

Payload examples must be copied from these tests, never invented:

- `locking_method_released`: `role: "user"`, `payload: { "cause": "recovery", "lockingMethodKind": "combination" }` (`locking-method-release-event.service.test.ts`), or `lockingMethodKind: "device"` (fan-out test).
- `locking_method_released_by_support`: `role: "admin"`, `payload: { "cause": "support", "lockingMethodKind": "combination" }` (`lock-admin-release-locking-method.test.ts`).

`eventId`, `seq`, `user._id`, `username` and dates in the examples are synthetic placeholders in the same style as the existing example on the page. If the code disagrees with this design, the code wins: write the page from the code and note the difference on the issue.

## Decisions

### 1. `lock-events.mdx`: new section "Locking method released"

A new `##` section placed after "Receive events" (after its "Delivery" subsection and the keyholder-view sentence) and before "Read the event stream". Heading `## Locking method released`, anchor `#locking-method-released`. Content, in this order:

1. One sentence: when a lock's locking method (its combination, the partner extension that holds it, or its device) is released outside a normal unlock, Chaster adds one of two events to the stream.
2. A table, one row per type: `type`, when it is sent, `role`, `payload.cause`.
   - `locking_method_released`: the wearer recovered a deserted lock after the 7-day wait. `role` `user`. `cause` `recovery`.
   - `locking_method_released_by_support`: Chaster support released the locking method. `role` `admin`. `cause` `support`. Add the Locked-lock behaviour only as traced (the lock is also unlocked).
3. A payload field table: `cause` (`recovery` or `support`), `lockingMethodKind` (`combination`, `partner` or `device`, with one plain phrase each from `lockingMethodKindOf`).
4. One JSON `data` example (the `data` object only, like the page's event stream format, or a full `lock_event.created` body matching the existing example; pick one and keep it consistent) using the `locking_method_released` test values. A second short example or a sentence for the support type with its test values.
5. What the extension should do: treat it as "the lock no longer holds this locking method"; for a partner locking provider, release on your side. Keep it to what the code guarantees: one row per release, so deduplicate on `eventId` like any event. Link [locking providers](/api/extensions-api/locking-providers) if that page is the right target (Applier checks its content).
6. Subscription note as an `:::info` (or `:::note`) box: an extension with no subscription list (or `["*"]`) receives both. An extension with a list must add `locking_method_released` and `locking_method_released_by_support` to its [manifest subscriptions](/api/extensions-api/extension-communication/manifest#subscriptions) or the Webhooks tab. Both are visible history entries, so they are also sent as `action_log.created` (link the existing overlap warning `#choose-which-events-you-receive`).

The intro bullet on line 18 (`type` examples) and the generic field table stay unchanged.

### 2. `changelog.mdx`

New entry at the top, `## <YYYY-MM-DD>` = the day this docs PR merges. The Applier writes the apply day; whoever merges updates the heading if the merge happens on another UTC day. Same style as the 2026-11-12 entry.

**New features**

- Two lock event types tell your extension that a lock's locking method was released: `locking_method_released` (the wearer recovered a deserted lock after 7 days) and `locking_method_released_by_support` (Chaster support released it)
  - `payload` carries `cause` (`recovery` or `support`) and `lockingMethodKind` (`combination`, `partner` or `device`)
  - Extensions with no subscription list receive them. If your extension has a list, add both types to receive them
  - Documentation: [Locking method released](/api/extensions-api/extension-communication/lock-events#locking-method-released)

Earlier entries are not edited.

## Verification design

- Field check: a table in `verification.md` with each field and value on the page, and the test file and assertion that proves it (T21 fan-out test for type and payload delivery; service and admin tests for `role` and `cause`).
- Build: `npm ci` if needed, then the Docusaurus build under the host lock, no broken link or anchor warning.
- The repository has no `.github/workflows`; it carries a `.gitlab-ci.yml` for the site deploy. The Applier records the exact-head check rollup on the PR (empty is expected) and the trigger evidence, as PR #28 did.

## Risks

- **The events are dark in production.** On chaster `main`, `recoverCombination` writes the release intent only when `DEVICES` is on for the wearer, and the staff route is behind `FeatureSwitchGuard(DEVICES)`. `DEVICES` is off in production until the owner's rollout. So until then the page describes events no partner receives. The page names no internal switch. This was raised to the Founding Engineer on the issue; the ticket's approved scope is to document them now, so proceed unless told otherwise.
- `user` on the support row is the staff account that released the lock (`by: staffId`), like other `admin` rows. Do not add a page claim about who it is beyond the generic `user` field; do not put a staff name in examples.
- Wording that implies a past format breaks the tone rule. Grep added lines for "previously", "used to", "no longer", "now".
- Anchors: the new `#locking-method-released` and the existing `#receive-events`, `#choose-which-events-you-receive` must resolve; the build reports broken links.
