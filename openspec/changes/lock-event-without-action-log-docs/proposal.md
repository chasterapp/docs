# Proposal

Ticket: Paperclip CHA-1685. Proposed on docs `main` at `294344d`.

## Why

chasterapp/chaster#1866 (merged 2026-11-12 as `57583809953abb6eac5df22af7bb40b7e2fc46eb`) changed the public webhook format:

- `lock_event.created`, and the events returned by `GET /api/extensions/sessions/:sessionId/events`, have no `actionLog`. `role`, `user` (`{ _id, username }` or `null`) and `createdAt` are top-level fields of the event. `payload` keeps its format and redaction. Webhooks tab test events use the same shape.
- Every lock sent to an extension (session payloads, `extension_session.*` webhooks, `lockForUser` of the main page token exchange) has `offerToken: null`.

chasterapp/chaster#1865 (merged 2026-11-11 as `e033481ef3`) caps each extension config at 2 MB.

The public docs still show `actionLog` inside `lock_event.created`, say `eventId` equals `actionLog._id` in the same body, and tell developers to deduplicate on `data.actionLog._id` for lock events. A partner reading them would write a handler that fails on the shipped payload.

## What changes

- `docs/api/extensions-api/extension-communication/lock-events.mdx`: the `lock_event.created` example and field table show `role`, `user` and `createdAt`, with no `actionLog`. The overlap warning deduplicates on `eventId` / `X-Chaster-Event-Id`.
- `docs/api/extensions-api/create-your-extension/webhooks.mdx`, section "Lock events and action logs": diagram, comparison table, the sentence about `data.actionLog`, the warning and the migration steps describe the shipped `lock_event.created` shape.
- `docs/api/changelog.mdx`: one new entry dated the day this docs PR merges, with the `actionLog` removal, the 2 MB config cap, and one neutral line on `lock.offerToken`.

## Capabilities

### New capabilities

None. This change documents shipped behavior and sets `skip_specs: true`.

### Modified capabilities

None.

## Out of scope

- Any chaster server, web, API client or extensions SDK change. A mismatch between these docs and chaster `main` is reported on the issue, not fixed here.
- Older changelog entries (2026-11-04 mentions `data.actionLog` in `lock_event.created`): they describe the format on their date and stay as written.
- `offerToken` anywhere outside the changelog line (the ticket asks for the changelog only; no page mentions it today).
- The 2 MB cap outside the changelog (no page text about config size limits is added; the ticket asks for the changelog entry only).
- Webhook delivery detail `payload` becoming nullable in the console API (#1866 part 3). The page does not describe that field's type, and the `409 payload-unavailable` resend case is already documented.
- `action_log.created`, which is unchanged.
- Publishing the site.

## Impact

Repository: `chasterapp/docs`, default branch `main`. Changes are limited to the three pages above and this OpenSpec change.

Feature switch: none. The server change shipped without a switch.

Sensitive surfaces: public webhook and partner API contract documentation (`lock_event.created`, the lock event stream endpoint, partner session payloads, extension config limits). Every claim must trace to a file on chaster `main` (design, Sources).

Merge: autonomous (owner decision, Vince, 2026-11-11). The Reviewer merges after double review and a passing local build. QA: none (documentation only; the build and the claim trace are the checks).
