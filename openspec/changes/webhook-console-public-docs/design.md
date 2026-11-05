# Design

## Context

See `proposal.md` for motivation. This Docusaurus 3 repository uses MDX frontmatter, explicit document IDs in `sidebars.json` and root-relative routes. Its tone checker is `.claude/hooks/lint-docs.sh` (`npm run lint:docs`): sentence-case headings, no em dashes. Mermaid diagrams are supported (`@docusaurus/theme-mermaid`).

Verified refs on 2026-11-05:

- Docs: `3bcfa8e437d1df195b3c4e9bbd8d4d0357157200` (`main`, includes #22 to #26).
- Chaster: `78e540ebcd8b048ad530adeadc8b70314308647a` (`main`, includes T01 #1713, T02 #1718, T05 #1722, T03 #1721).

Read chaster from a private scratch clone (`git clone --depth 30 --filter=blob:none https://github.com/chasterapp/chaster`), never the shared human checkout `/home/chasterdev/projects/chaster`.

### Sources

Server paths are relative to `server/src/modules/` on chaster `main`. Every claim on the pages must come from this table or from another file the Applier reads and adds to it.

| Fact | Source |
| --- | --- |
| Header names and values; `X-Chaster-Event-Id` only when the delivery has an id | `partner-webhook/helpers/webhook-headers.ts` |
| Event id per event: `data.eventId` for `lock_event.created`, `data.actionLog._id` for `action_log.created`, the queue job id otherwise | `partner-webhook/helpers/resolve-delivery-identity.ts` |
| Attempt number is the delivery's count (1-based); a resend continues it | `partner-webhook/jobs/call-partner-webhook.job.ts` (`attempt = head?.attemptCount ...`), `partner-webhook/models/webhook-history.model.ts` (comment on the attempt field) |
| 5 attempts, exponential backoff from 60 s | `partner-webhook/jobs/call-partner-webhook.options.ts` |
| 10 s timeout, redirects not followed, raw body read up to 4 KB | `partner-webhook/services/webhook-request.service.ts` (`timeout: 10000`, `maxRedirects: 0`) |
| Non-public addresses refused at connection time (loopback, private, link-local, carrier-grade NAT, multicast, reserved, IPv6 equivalents) | `partner-webhook/helpers/webhook-address-guard.ts` |
| Success is a `2xx`; anything else, a timeout or a connection error is a failed attempt | `call-partner-webhook.job.ts` (`success = statusCode >= 200 && < 300`, `if (error) throw error`) |
| Delivery statuses `delivered`, `retrying`, `failed` and when each is set | `partner-webhook/models/webhook-delivery-status.enum.ts`; `call-partner-webhook.job.ts` (`nextState`) |
| An automatic attempt is skipped once the delivery is `delivered` (every event with an id) | `call-partner-webhook.job.ts` (`isDelivered`) |
| A failed resend does not end a running retry schedule; a delivered delivery stays delivered | `partner-webhook/repositories/webhook-history.repository.ts` (`finishAttempt`, `keepRetrying`) |
| Stored response body: up to 4 KB, 512 bytes on automatic `2xx` | `partner-webhook/helpers/capture-response-body.ts`, `call-partner-webhook.job.ts` |
| History kept 7 days | `partner-webhook/models/webhook-history.model.ts` (TTL); already on the page |
| Developer endpoints, guards, `developer` scope, status codes (`200`, `202` on resend) | `webhook-console/controllers/webhook-console.controller.ts`; `developer-client/guards/developer-client.guard.ts` (developer token accepted) |
| Search body: `limit` 1 to 100 (default 50), `cursor`, `status`, `event`, `eventType`, `query` (exact event id or lock id); response `results`, `hasMore`, `nextCursor` | `webhook-console/dto/search-webhook-deliveries.dto.ts`, controller `search` |
| Delivery detail fields; `Authorization` shown masked | `webhook-console/dto/webhook-delivery.dto.ts`, `webhook-console/mappers/webhook-console.mapper.ts` |
| Stats `range` `1h`, `24h` (default), `7d` and response fields | `webhook-console/dto/webhook-stats.dto.ts` |
| Test event body `{ event, type, lockId? }`, events `lock_event.created` and `action_log.created`, response fields | `webhook-console/dto/send-webhook-test.dto.ts` |
| Test envelope has `"test": true` at the root, sent once, never retried, kept out of stats | `partner-webhook/services/webhook-test.service.ts` |
| Test sample: unknown type `400 unknown-event-type`; a lock where the extension is not installed `404` | `lock-event-delivery/services/webhook-sample.service.ts` |
| Resend: queued, one attempt, same event id, new `requestId` and `sentAt`; test deliveries cannot be resent (`400 test-delivery`); `409 payload-unavailable` | `webhook-console/services/webhook-console.service.ts` (`resend`), `call-partner-webhook.job.ts` (`resend`) |
| Resend and test: 30 per extension per minute (`429`), `400 webhook-url-missing`, `400 webhook-target-not-public` | `webhook-console.service.ts` (`checkSend`, `SENDS_PER_MINUTE`) |
| Subscriptions `GET`/`PUT` body `{ subscriptions: string[] \| null, actionLogFeed: boolean }`; `null` means every event except your own; ids checked with the manifest id format (`invalid-id`, `duplicate-id`), so `"*"` is refused | `webhook-console/dto/webhook-subscriptions.dto.ts`, `webhook-console.service.ts` (`setSubscriptions`), `partner-extension/services/partner-extension.service.ts` (`setWebhookSubscriptions`) |
| `action_log.created` switch: on unless turned off; session subscriptions do not affect it | `action-log-webhook/listeners/create-webhook-on-action-log-created.listener.ts` (`actionLogFeed !== false`) |
| Matching rule: session list first, then extension list; no list means every event except your own (typed or not, hidden or not) | `lock-event-delivery/services/lock-event-subscriptions.service.ts` (`matches`) |
| Manifest `["*"]` means unset; `"*"` with another entry is `400 wildcard-not-alone`; omitted on the first upload is `[]`, omitted later keeps the current value; subscriptions apply at once, never held for review | `partner-extension/services/partner-extension-manifest.service.ts` (lines around `MANIFEST_SUBSCRIBE_ALL`), `partner-extension.service.ts` (`requestManifestReview`, pending approval drops `fields.subscriptions`) |
| `GET .../manifest` returns `["*"]` when unset | `partner-extension/mappers/partner-extension-manifest.mapper.ts` |
| Session `PUT` refuses `"*"` (id pattern); `null` inherits the extension setting | `partner-extension/dto/session-subscriptions.dto.ts`, `lock-event-subscriptions.service.ts` |
| UI labels (tab, buttons, views, filters, statuses) | `web/src/locales/en/developers.json` (`tabs.webhooks`, `webhooks.*`) and `web/src/modules/developers/components/webhooks/` |
| Endpoints are in the public API reference | `server/src/scripts/generate-swagger.ts` (`WebhookConsoleModule` in `includedModules`) |

If the shipped code disagrees with this design, the code wins: write the page from the code and note the difference on the issue.

## Goals and non-goals

**Goals:** a partner can tell a retry from a new event and dedupe on headers; knows what each delivery status means and when Chaster gives up; can debug from the Webhooks tab (or the API) without asking us; knows how to turn `action_log.created` off and how lock event subscriptions are set from three places (manifest, Webhooks tab, session).

**Non-goals:** no new page, no per-field reference of the stats response (the API reference has it), no admin features, no publish.

## Decisions

### 1. `webhooks.mdx`

Keep the document ID, title, existing anchors (`#event-types`, `#retries`, `#lock-events-and-action-logs`, `#peer-review-verdicts`, `#actions-and-delivery-limits`) and the peer review section unchanged. Changes, in page order:

1. **Configuring webhooks.** Add after the URL step: the URL must resolve to a public address (requests to private, loopback or link-local addresses fail), and Chaster does not follow redirects (a `3xx` is a failed attempt). Keep basic auth.
2. **Request headers** (new H3 under "Handling webhooks", anchor `#request-headers`). A table:

   | Header | Value |
   | --- | --- |
   | `X-Chaster-Event` | The event name, same as `event` in the body. |
   | `X-Chaster-Event-Id` | The id of the delivery, the same on every attempt and resend. `lock_event.created`: `data.eventId`. `action_log.created`: `data.actionLog._id`. Other events: an id Chaster assigns to the delivery. |
   | `X-Chaster-Attempt` | `1` on the first attempt, then `2`, `3`... A resend continues the count. |
   | `X-Chaster-Request-Id` | New on every attempt, same as `requestId` in the body. Use it for diagnostics only. |

   Then: the body is unchanged. `action.invoke` calls are not notifications and do not carry these headers (link to Handling invocations).
3. **Deduplicate deliveries** (new H3, anchor `#deduplicate-deliveries`). Deduplicate on the pair `X-Chaster-Event` + `X-Chaster-Event-Id`. `action_log.created` and `lock_event.created` for the same history entry share the same `X-Chaster-Event-Id`: dedupe on the id alone to react once per history entry. Never dedupe on `requestId` or `X-Chaster-Request-Id`. Keep the body alternatives already on the page (`data.eventId`, `data.actionLog._id`) and the note that `extension_session.updated` repeats legitimately for one session (each update is its own delivery with its own id).
4. **Retries** (keep anchor `#retries`). 5 attempts in total, 10 s timeout each, backoff from 60 s (about 1, 2, 4 and 8 minutes between attempts). A `2xx` delivers; any other status (including `3xx`), a timeout or a connection error is a failed attempt. Once delivered, Chaster sends no further automatic attempt for that delivery. Retries keep the event id and get a new request id and `sentAt`. Keep "retries do not guarantee every event is enqueued or delivered".
5. **Delivery statuses** (new H3, `#delivery-statuses`). `delivered`: an attempt got a `2xx`; final. `retrying`: the last attempt failed and another is scheduled. `failed`: the fifth attempt failed, or a test event or resend failed with no retry pending; Chaster gives up. A resend can still deliver a failed delivery. Test deliveries are `delivered` or `failed`, never retried.
6. **Webhooks tab** (replace "Debugging" and its "not available yet" caution; new H2 `## Webhooks tab`, keep a `#debugging` anchor only if some page links to it; none does on `3bcfa8e`). Open the Developer Interface, select the extension, then the **Webhooks** tab. Describe with the UI labels from `developers.json`:
   - **Endpoint** card: URL, authentication, `Timeout 10 s`, `5 attempts, exponential from 1 min`, `History kept 7 days`, **Send test event**.
   - Time range `1 h`, `24 h`, `7 d`: attempts, success rate, p95 response time, **Retrying now**, and the **Delivery attempts** chart.
   - The failure banner when one event type keeps failing (at least 90% of at least 20 attempts in the range), with the hint to answer `2xx` to event types you ignore or unsubscribe.
   - **Deliveries** view: filters (status, event, type), search by event id or lock id, **Live**, **Load older**. The delivery panel: attempts timeline, request headers (`Authorization` masked), payload, response status, body (first 4 KB; first 512 bytes on automatic `2xx`), duration, error, the related delivery for the same history entry, **Copy as cURL** (no credentials), **Copy payload**, **Resend now**.
   - **Subscriptions** view: decision 1.8.
   - Response bodies are stored only for public addresses (always true outside local development, see 1.1). Keep "History kept 7 days" and the "reach out to us" line.
7. **Resend and test events** (new H3s under the tab section, `#resend-a-delivery`, `#send-a-test-event`).
   - Resend: any delivery still in history, except test deliveries. One attempt, queued, same payload `data` and event id, new `requestId` and `sentAt`, attempt count continues. A resend duplicates an event you may already have processed: dedupe on the event id. A failed resend does not stop a retry schedule still running.
   - Test event: `lock_event.created` or `action_log.created`, with an event type. Optional lock where the extension is installed; otherwise a generated sample lock. Sent immediately; the result (status, duration, body) shows in the dialog. The body has `"test": true` at the root (show a short envelope example): handlers should answer `2xx` and not act on it. Never retried, not counted in the stats.
   - Both: only to a webhook URL that resolves to a public address (`400 webhook-target-not-public`), need a webhook URL (`400 webhook-url-missing`), and are limited to 30 per extension per minute (`429`).
8. **Choose which events you receive** (new H3 `#choose-the-events-you-receive` in the tab section, or H2 if it reads better).
   - `action_log.created` switch: on by default; when off, the extension receives no `action_log.created` for any lock. Session subscriptions do not affect it. Other events are unchanged.
   - Lock event subscriptions: three states, **every event except your own**, **none** (empty list), or a list of event types. Saved at once, applies to new events, does not trigger a manifest review and does not change the manifest revision. The manifest and this view write the same setting; the last write wins, and a manifest upload without `subscriptions` keeps it. Ids your extension no longer finds in the catalog stay listed until you remove them. Link to Lock events for session overrides.
9. **Webhooks API** (new H2 `#webhooks-api`). Same authentication as the other developer endpoints (developer token, `developer` scope; link to the Extensions API authentication page). List:
   - `POST /api/developers/extensions/:extensionId/webhooks/deliveries/search`: newest first; body fields and response from Sources.
   - `GET /api/developers/extensions/:extensionId/webhooks/deliveries/:deliveryId`: one delivery with all its attempts.
   - `GET /api/developers/extensions/:extensionId/webhooks/stats?range=1h|24h|7d`.
   - `POST /api/developers/extensions/:extensionId/webhooks/deliveries/:deliveryId/resend`: `202`, `{ "deliveryId" }`.
   - `POST /api/developers/extensions/:extensionId/webhooks/test`: `{ "event", "type", "lockId" }`; response `deliveryId`, `eventId`, `statusCode`, `durationMs`, `responseBody`, `error`.
   - `GET` / `PUT /api/developers/extensions/:extensionId/webhooks/subscriptions`: `{ "subscriptions": [...] | null, "actionLogFeed": true }`; `null` means every event except your own; `"*"` is refused here. `GET` also returns the event types you can choose, with their 24 h volume and success rate.
   Point to the [API reference](https://api.chaster.app/api) for full schemas.
10. **Lock events and action logs** (keep anchor). Keep the table and the warning. Update:
    - "An extension without a manifest or session subscription list" becomes "An extension whose subscriptions are not set (no manifest list, `["*"]`, or **every event** in the Webhooks tab) and no session list".
    - Migration steps: 1. choose event types in the manifest or the Subscriptions view; 2. turn `action_log.created` off in the Subscriptions view, or keep it and dedupe on `X-Chaster-Event-Id`; 3. session lists override the extension setting.
11. **Event types** list: add "can be turned off" to the `action_log.created` bullet with a link to 1.8.

### 2. `manifest.mdx`

- "Upload a manifest": "A list you omit becomes empty" gets the exception: `subscriptions` follows the rule below.
- `#subscriptions` (keep anchor): the capability ids of the event types your extension receives as `lock_event.created`. Then, replacing the current warning:
  - `["*"]`: every event of the lock except your own, typed or not, visible or hidden, including event types added later. `"*"` must be the only entry, or the upload returns `400` with `wildcard-not-alone` at `subscriptions[i]`.
  - A list: only those event types; untyped events never match. `[]` receives no lock events.
  - Omitted: on the first upload, the list is empty (no lock events). On later uploads, the current setting is kept, including a change made in the Webhooks tab.
  - Subscriptions apply as soon as the upload succeeds and are never held for manifest review.
  - Reading the manifest (`GET`, the Manifest tab) returns `["*"]` when nothing is set, so the JSON uploads back unchanged.
  - You can also change subscriptions in the Webhooks tab, or for one session. Sessions do not accept `"*"`; send `null` to return to the extension setting. Link to `lock-events#choose-which-events-you-receive`.
  Use `:::info` for the first-upload rule (it is the one that silently stops deliveries) instead of the old `:::warning`.
- The simplest-manifest example may add a second example `{ "subscriptions": ["*"] }`.

### 3. `lock-events.mdx`

- `#choose-which-events-you-receive` (keep anchor). Diagram: same shape, with the first branch labeled "No list, or `["*"]`" and the question node "session list first, then extension setting". Bullets:
  - **Every event except your own** (no manifest list, `["*"]` in the manifest, or every event in the Webhooks tab): every event of the lock, typed or not, visible or hidden, including types added later.
  - **A list** (manifest or Webhooks tab): only those types; untyped events never delivered; empty list delivers nothing.
  - **Per session**: unchanged `PUT` text, plus: `"*"` is not accepted; `null` returns to the extension setting.
  Keep the `lock.capabilities-changed` sentence and the warning; in the warning, mention that `action_log.created` can be turned off.
- `#delivery`: "Deduplicate on `eventId`" adds "(also sent as the `X-Chaster-Event-Id` header)"; link retries to `webhooks#retries` (5 attempts unchanged).

### 4. `changelog.mdx`

New `## 2026-11-05` above `2026-11-04`, house style (bold group headings, nested bullets, "Documentation:" links):

- **New features**: Webhooks tab (deliveries, attempts, response bodies, stats, resend, test events); `X-Chaster-Event`, `X-Chaster-Event-Id`, `X-Chaster-Attempt` headers; `action_log.created` can be turned off; subscriptions editable without a manifest upload; `subscriptions: ["*"]`; new endpoints (the seven from 1.9, one line each).
- **Changes** (use the existing **Minor changes** heading style, or **Breaking changes** if the Applier judges the redirect and private-address rules breaking; recommendation: **Breaking changes**, because a partner whose URL redirects stops receiving events):
  - Webhook requests no longer follow redirects, and URLs resolving to non-public addresses are refused.
  - A manifest upload without `subscriptions` keeps the current setting once a manifest exists (before: it emptied the list). Subscriptions are applied at once, never held for review.

### 5. Wording and style

Second person, present tense, sentence-case headings, no em dashes, `:::info`/`:::warning` for gotchas, UI labels in bold exactly as in `developers.json`. Synthetic ids in examples (24-character hex like `6731b2c4e5f0a1b2c3d4e5f6`, as the pages already use). No real user, lock or extension data.

### 6. Screenshots

The ticket asks for screenshots following chaster's `.claude/skills/update-docs` conventions (match existing `static/img/` style, crop to the region, kebab-case names such as `webhooks-tab-overview.png`, run `npm run compress:images`). Capture them from a private chaster stack in a scratch clone (`node scripts/prepare-worker.mjs --all`, then `scripts/worker-dev.mjs`, per chaster `docs/reference/operations/agent-environments.md`), with synthetic deliveries, and stop the stack afterwards. Suggested captures: the tab overview, the delivery panel, the Subscriptions view. Do not show a real webhook password, user or personal URL.

If a private stack cannot run within the run budget, ship the text without images (no broken image references, the build must pass) and say so on the issue and in the PR description. Screenshots are not part of the definition of done on the issue.

## Risks and trade-offs

- **Pages describe behavior that may not be deployed yet.** Merging does not publish the site. The changelog date is the merge date of T03, as the ticket asks.
- **Behavior change for redirects and private addresses.** Documented as a changelog change so partners whose endpoint redirects can fix it.
- **Webhook page grows long.** Accepted: the ticket asks to extend #22's pages, not to add parallel ones. Clear H2s keep it navigable; the API section points to the OpenAPI reference instead of repeating schemas.
