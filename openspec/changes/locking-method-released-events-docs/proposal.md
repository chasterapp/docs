# Proposal

Ticket: Paperclip CHA-1871 (device platform T37, epic E01). Proposed on docs `main` at `d5be533`, chaster `main` at `4470c67de9fbb8ad402fe2c7742ed4514591c195` (includes chasterapp/chaster#2215, T21).

## Why

chasterapp/chaster#2215 added two history entries that release a lock's locking method (a combination, a partner extension or a device):

- `locking_method_released`: the wearer recovers a deserted lock after the 7 days.
- `locking_method_released_by_support`: Chaster staff release the locking method.

Both are written in the default prefix, so partners receive them as `lock_event.created` webhooks with `type` set to the same name (`extension-manifest/data/event-type-aliases.ts`). A partner with no subscription list receives them. A partner with an explicit list receives them only if the list names them. The public reference does not mention either type, so a partner whose extension holds the lock (a partner locking method) cannot know it must react to them.

## What changes

- `docs/api/extensions-api/extension-communication/lock-events.mdx`: a new section next to "Receive events" documenting both types: what triggers each, `role`, the two payload fields (`cause`, `lockingMethodKind`) and their values, a `data` example per type copied from the T21 tests, and the subscription note.
- `docs/api/changelog.mdx`: one new entry dated the day this docs PR merges, linking to the new section.

## Capabilities

### New capabilities

None. This change documents shipped behaviour and sets `skip_specs: true`.

### Modified capabilities

None.

## Out of scope

- Any chaster server, web, API client or extensions SDK change. A mismatch between this page and chaster `main` is reported on the issue, not fixed here.
- The internal `DEVICES` feature switch, device pairing, the TTLock connector and every other device platform surface. The page names no internal switch.
- The staff action itself (admin route, moderation audit) beyond "Chaster support released the locking method".
- `webhooks.mdx`, `manifest.mdx` and `introduction.mdx`: their subscription text already covers lists in general; no change.
- Older changelog entries.
- Publishing the site.

## Impact

Repository: `chasterapp/docs`, default branch `main`. Changes are limited to the two pages above and this OpenSpec change.

Feature switch: none for the docs. The server writes both rows only while `DEVICES` is on (see design, Risks).

Sensitive surfaces: public partner API contract documentation (`lock_event.created` types and payloads, subscription behaviour). Every claim must trace to a file on chaster `main` (design, Sources).

Merge: autonomous after independent two-model review, a passing local Docusaurus build and green checks on the exact head (the repository has no GitHub Actions workflow; see design). QA: none (public reference text, no product behaviour; the build and the field check verify it). The epic parent checks the reference in its integrated acceptance (J8).
