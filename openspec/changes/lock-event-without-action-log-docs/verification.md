# Verification

Refs: docs `294344d` (`origin/main`), chaster `57583809953abb6eac5df22af7bb40b7e2fc46eb` (`main` at 2026-11-12, includes #1865 `e033481ef3` and #1866). `git log 57583809953..origin/main` on chaster is empty, so nothing moved after the proposal. Read from a private scratch clone, not the shared checkout.

## Claim trace

Paths are under `server/src/modules/` on chaster `main`.

| Claim | Page, section | Chaster source |
| --- | --- | --- |
| `lock_event.created` data has `eventId, seq, type, source, payload, correlationId, causationId, role, user, createdAt`, no `actionLog` | lock-events "Receive events" (example, table); webhooks "Lock events and action logs" (table) | `lock-event-delivery/dto/lock-event.dto.ts` (`LockEventDto`) |
| `role` is one of `user`, `keyholder`, `extension`, `admin` | lock-events field table | `action-log/models/action-log-role.enum.ts` |
| `role: user` is the wearer | lock-events field table | `logs-notifier/services/action-log-notification.service.ts:50` (`notifyWearer: role !== ActionLogRole.User`) |
| `user` is `{ _id, username }`, or `null` when the row has no populated user | lock-events field table | `lock-event-delivery/mappers/lock-event.mapper.ts` (`toDto`, `isDocument(row.user)`); `ActionLog.user` is optional (`action-log/models/action-log.model.ts`); fan-out and catch-up populate `user` (`action-log.service.ts` `findById`, `lock-event.repository.ts` `findCatchUp`) |
| `createdAt` is the row creation time | lock-events field table | `LockEventMapper.toDto` (`createdAt: row.createdAt`) |
| Same shape for the webhook, `GET /api/extensions/sessions/:sessionId/events`, and Webhooks tab test events | changelog | `jobs/fan-out-lock-event.job.ts`, `partner-extension/controllers/partner-lock-events.controller.ts`, `lock-event-delivery/services/webhook-sample.service.ts` (all call `LockEventMapper.toDto`) |
| `X-Chaster-Event-Id` is `data.eventId` (`lock_event.created`) and `data.actionLog._id` (`action_log.created`) | lock-events warning; webhooks section; changelog | `partner-webhook/helpers/resolve-delivery-identity.ts` |
| `lock_event.created` has no rendered history text (no text field in the DTO) | webhooks section | `LockEventDto` |
| `lock.offerToken` is `null` in locks sent to extensions | changelog | #1866 commit message and `partner-extension-helper/partner-extension.helper.ts` `lockForPartner` |
| 2 MB cap on `JSON.stringify(config)` in UTF-8, refused with `400` (`BadRequestException`) | changelog | `extension/helpers/extension-config-size.ts` |
| Cap applies on configuration token save, session `config` update, extension default config | changelog | `partner-configuration/services/partner-configuration.service.ts` `update` and `updateOneByTokenAndDeveloperClient`; `extension-party/repositories/extension-party.repository.ts` (`writeFields`); `partner-extension/services/partner-extension.service.ts` (`defaultConfig`) |

Open points settled:

- `user` is `null` when the stored row has no user document (for example an event created without a user, or a user that cannot be populated). The page says "or `null` when the event has no user".
- `role: user` means the wearer, per the notification service.
- The cap also covers lock creation and extension edits, and lock/template token creation intentionally skips it (`partner-configuration-creation.service.ts` comment). The changelog lists only the three partner-facing places and does not describe stored oversized configs.

## Checks

- `bash .claude/hooks/lint-docs.sh` on the three pages: exit 0 (one existing title-case warning at `changelog.mdx:290` on an untouched old entry).
- `git diff --check`: clean.
- Wording grep on added lines (previously, used to, no longer, before, now): no hit. Em dash count in added lines: 0.
