# Design

## Context

See `proposal.md`. Docusaurus 3, MDX pages, root-relative links, Mermaid via `@docusaurus/theme-mermaid`. Tone checker: `.claude/hooks/lint-docs.sh` (`npm run lint:docs`): sentence-case headings, no em dashes. Ticket rules: describe current behavior only, no "previously" / "before" / "used to" phrasing, no em dashes.

Verified refs on 2026-11-12:

- Docs: `294344d` (`main`, includes #27).
- Chaster: `57583809953abb6eac5df22af7bb40b7e2fc46eb` (`main`, includes #1865 at `e033481ef3` and #1866).

Read chaster from a private scratch clone (`git clone --depth 30 --filter=blob:none https://github.com/chasterapp/chaster`) or `gh api`, never the shared human checkout `/home/chasterdev/projects/chaster`.

### Sources

Paths are relative to `server/src/modules/` on chaster `main`. Every claim must come from this table or from another file the Applier reads and adds to the trace.

| Fact | Source |
| --- | --- |
| `LockEventDto` fields: `eventId`, `seq`, `type`, `source`, `payload`, `correlationId`, `causationId`, `role`, `user`, `createdAt`; no `actionLog` | `lock-event-delivery/dto/lock-event.dto.ts` |
| `role` values `user`, `keyholder`, `extension`, `admin` | `action-log/models/action-log-role.enum.ts` |
| `user` is `{ _id, username }` when the row's user is a populated document, else `null`; `createdAt` is the row's creation time | `lock-event-delivery/mappers/lock-event.mapper.ts` (`toDto`); populate in `lock-event-delivery/repositories/` and the fan-out job (confirm when `user` is `null`) |
| Same DTO for the webhook, `GET /api/extensions/sessions/:sessionId/events`, and console test samples | `lock-event-delivery/jobs/fan-out-lock-event.job.ts`, `partner-extension/controllers/partner-lock-events.controller.ts`, `lock-event-delivery/services/webhook-sample.service.ts` |
| `X-Chaster-Event-Id` is `data.eventId` for `lock_event.created` and `data.actionLog._id` for `action_log.created` (unchanged) | `partner-webhook/helpers/resolve-delivery-identity.ts` |
| `action_log.created` still carries `data.actionLog` with rendered history text | `action-log-webhook/` listener, `action-log/services/action-log.service.ts` |
| Partner locks have `offerToken: null` | `partner-extension-helper/partner-extension.helper.ts` (`lockForPartner`), callers in `partner-authorization/services/partner-main-authorization.service.ts` (`lockForUser`) and `lock-creation/services/lock-extension-sync.service.ts` (`extension_session.deleted`) |
| Config cap: 2 × 1024 × 1024 bytes of `JSON.stringify(config)` in UTF-8; `400` with message `The <slug> extension configuration is too large (maximum 2 MB).` | `extension/helpers/extension-config-size.ts` |
| Where the cap applies (partner-facing): configuration token save, session `config` update, extension default config, lock creation and lock extension edits | callers of `assertExtensionConfigSize` in #1865: `partner-configuration/services/partner-configuration.service.ts`, `extension-party/repositories/extension-party.repository.ts` (`writeFields`, `replaceConfig`, `create`), `partner-extension/services/partner-extension.service.ts`, `extension/extension.service.ts`, `lock-creation/services/lock-creation.service.ts`, `extension-validation/services/extension-validation.service.ts` |

If the code disagrees with this design, the code wins: write the page from the code and note the difference on the issue.

## Decisions

### 1. `lock-events.mdx`, section "Receive events"

- JSON example: remove the `actionLog` block. After `causationId`, add `"role": "keyholder"`, `"user": { "_id": "<24-hex id>", "username": "<synthetic name>" }` and `"createdAt": "2026-11-04T12:00:00.000Z"` (before `sentAt`). Keep field order as the DTO, with `sessionId` first. Use obviously synthetic values.
- Field table: drop the `actionLog` row. `eventId` row: "Stable id of the event, also sent as the `X-Chaster-Event-Id` header." Add rows:
  - `role`: who created the event: `user` (the wearer), `keyholder`, `extension` or `admin`. Confirm the meaning of `user` against the action log model before writing "the wearer".
  - `user`: the user who created the event, `{ "_id", "username" }`, or `null` (state the cases the code produces).
  - `createdAt`: when the event was written, as an ISO 8601 date.
- Warning at the end of "Choose which events you receive": a visible history entry is sent in both webhooks with the same id: `eventId` in `lock_event.created`, `actionLog._id` in `action_log.created`, and the same `X-Chaster-Event-Id` header. The rest of the warning stays, with "deduplicate on `X-Chaster-Event-Id`" replacing "deduplicate on `actionLog._id`".
- "Read the event stream": the sentence "events in the same format as the `data` of `lock_event.created` (without `sessionId`)" stays true; no change.

### 2. `webhooks.mdx`, section "Lock events and action logs"

- Mermaid node B: `lock_event.created<br/>eventId, seq, type, payload...` (no `data.actionLog`).
- Table: rename the last row label to "Fields in `data`" (or keep "Entry" if it reads better). `action_log.created`: `actionLog`. `lock_event.created`: `eventId`, `seq`, `type`, `payload`, `source`, `correlationId`, `causationId`, `role`, `user`, `createdAt`.
- Replace the sentence "`data.actionLog` has the same format in both events, and `data.eventId` equals `data.actionLog._id`" with: `data.eventId` of `lock_event.created` equals `data.actionLog._id` of `action_log.created` for the same history entry, and both deliveries carry the same `X-Chaster-Event-Id`. `lock_event.created` has no `actionLog` and no rendered history text: use `action_log.created` to display history entries. Confirm the "no rendered text" claim against the DTO.
- Warning: replace "reacts to any webhook that contains `data.actionLog` without checking `event`" with "does not check `event`": such a handler reacts to both deliveries of each visible history entry, and to hidden events. Rephrase "**To keep your current behavior**" without implying a past state, for example "**To react once per history entry with `action_log.created`**".
- Migration steps: add a step that `role`, `user` and `createdAt` are top-level fields of `data`, and the event's own fields are in `payload`.
- "Request headers" and "Deduplicate deliveries" already say `data.eventId` for `lock_event.created` and `data.actionLog._id` for `action_log.created`: re-read them, no change expected.

### 3. `changelog.mdx`

New entry at the top, `## <YYYY-MM-DD>` = the day this docs PR merges. The Applier writes the apply day; whoever merges updates the heading if the merge happens on another UTC day. Same style as the 2026-11-05 entry (bold group headings, nested bullets, "Documentation:" links).

**Breaking changes**

- `lock_event.created` and the events of `GET /api/extensions/sessions/:sessionId/events` have no `actionLog`
  - `role`, `user` and `createdAt` are top-level fields of the event. `payload` is unchanged
  - Test events from the Webhooks tab have the same format
  - Deduplicate with `action_log.created` on `X-Chaster-Event-Id`: it is `data.eventId` in `lock_event.created` and `data.actionLog._id` in `action_log.created`
  - Documentation: [Lock events](/api/extensions-api/extension-communication/lock-events#receive-events)
- Each extension config is limited to 2 MB
  - Measured on its JSON encoding. A larger config is refused with `400`
  - List the partner-facing places it applies (configuration token save, session `config` update, default config), from the Sources trace. Mention stored configs above the cap only if the code gives a clear, partner-relevant rule
  - No "Documentation:" link unless a page describes the cap

**Minor changes**

- One neutral line: `lock.offerToken` is always `null` in the locks sent to extensions (session payloads, webhooks and `lockForUser`).

Earlier entries are not edited.

## Risks

- Wording that implies a past format breaks the ticket rule. Grep the changed lines for "previously", "before", "used to", "now", "no longer" in page text; the changelog may say "have no `actionLog`" but not "no longer".
- Anchors: `#receive-events`, `#lock-events-and-action-logs`, `#request-headers` must still resolve; the build reports broken links.
