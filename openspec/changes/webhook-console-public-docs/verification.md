# Verification

## Refs

- Docs base: `3bcfa8e437d1df195b3c4e9bbd8d4d0357157200` (`main`).
- Chaster: `78e540ebcd8b048ad530adeadc8b70314308647a` (`origin/main` on 2026-11-05, read from a private scratch clone). `main` has not moved past `78e540eb`, so no source changed since the proposal.

Server paths are relative to `server/src/modules/`.

## Claim trace

| Claim | Page and section | Source (function or constant) |
| --- | --- | --- |
| Headers `X-Chaster-Request-Id`, `X-Chaster-Event`, `X-Chaster-Event-Id`, `X-Chaster-Attempt` | webhooks `#request-headers` | `partner-webhook/helpers/webhook-headers.ts` (`webhookHeaders`) |
| Event id: `data.eventId` (lock events), `data.actionLog._id` (action logs), job id otherwise | webhooks `#request-headers`, `#deduplicate-deliveries` | `partner-webhook/helpers/resolve-delivery-identity.ts` |
| Attempt count 1-based, a resend continues it | webhooks `#request-headers`, `#resend-a-delivery` | `partner-webhook/jobs/call-partner-webhook.job.ts` (`attempt = head?.attemptCount ?? ...`) |
| `action.invoke` has `X-Chaster-Request-Id` only, none of the event headers | webhooks `#request-headers` | `webhookHeaders` is only called from `call-partner-webhook.job.ts` and `webhook-test.service.ts`; `extension-broker/clients/partner-invoke.client.ts` (sets `X-Chaster-Request-Id`) |
| Event id is the event's id, found with search `query`, not `:deliveryId` | webhooks `#request-headers` | `resolve-delivery-identity.ts`; `webhook-console/dto/search-webhook-deliveries.dto.ts` (`query`) |
| Delivery details list the latest 50 attempts | webhooks `#webhooks-api`, changelog | `partner-webhook/repositories/webhook-history.repository.ts` (`MAX_ATTEMPTS_LISTED`, `findAttemptsOf`) |
| **Retrying now** is a current count, not tied to the range | webhooks `#webhooks-tab` | `webhook-console.service.ts` (`stats`: `countRetrying(extension._id, now)`) |
| Failure banner reads the last 24 hours, whatever the range | webhooks `#webhooks-tab` | `web/src/modules/developers/business/webhooks/useActiveWebhookDiagnoses.ts` (`WebhookStatsRangeEnum._24h`) |
| Lock event delivery skips automatic attempts once delivered; resends are sent | lock-events `#delivery` | `call-partner-webhook.job.ts` (`isDelivered`, `resend`) |
| 5 attempts, backoff from 60 s | webhooks `#retries`, endpoint card | `partner-webhook/jobs/call-partner-webhook.options.ts` (`WEBHOOK_JOB_OPTIONS`) |
| 10 s timeout, no redirects | webhooks `#configuring-webhooks`, `#retries` | `partner-webhook/services/webhook-request.service.ts` (`timeout: 10000`, `maxRedirects: 0`) |
| Non-public addresses refused | webhooks `#configuring-webhooks`, changelog | `partner-webhook/helpers/webhook-address-guard.ts` (`BLOCKED_RANGES`, `literalHostRefusal`) |
| `2xx` delivers; other status, timeout, connection error fail | webhooks `#retries` | `call-partner-webhook.job.ts` (`success`, `if (error) throw error`) |
| No automatic attempt once delivered | webhooks `#retries` | `call-partner-webhook.job.ts` (`isDelivered`) |
| Statuses `delivered`, `retrying`, `failed` | webhooks `#delivery-statuses` | `partner-webhook/models/webhook-delivery-status.enum.ts`; `call-partner-webhook.job.ts` (`nextState`) |
| Failed resend keeps a live retry schedule; delivered stays delivered | webhooks `#resend-a-delivery` | `partner-webhook/repositories/webhook-history.repository.ts` (`finishAttempt`, `keepRetrying`) |
| Stored body 4 KB, 512 bytes on automatic `2xx` | webhooks `#webhooks-tab` | `partner-webhook/helpers/capture-response-body.ts`; `call-partner-webhook.job.ts` |
| History kept 7 days | webhooks `#webhooks-tab` | `partner-webhook/models/webhook-history.model.ts` (TTL), `developers.json` `webhooks.endpoint.retention` |
| Failure banner: at least 90% of at least 20 attempts | webhooks `#webhooks-tab` | `webhook-console/services/webhook-console.service.ts` (`DIAGNOSIS_MIN_ATTEMPTS`, `DIAGNOSIS_FAILURE_RATIO`) |
| `Authorization` masked | webhooks `#webhooks-tab`, `#webhooks-api` | `webhook-console/mappers/webhook-console.mapper.ts` (`Basic ••••••••`) |
| Copy as cURL has no credentials | webhooks `#webhooks-tab` | `web/src/modules/developers/business/webhooks/webhook-curl.ts` (`buildCurl`) |
| Seven endpoints, developer token, `developer` scope, `202` on resend, `200` on search and test | webhooks `#webhooks-api`, changelog | `webhook-console/controllers/webhook-console.controller.ts`; `developer-client/guards/developer-client.guard.ts` |
| Search body and response | webhooks `#webhooks-api` | `webhook-console/dto/search-webhook-deliveries.dto.ts`; controller `search` |
| Stats `range` `1h`, `24h` default, `7d` | webhooks `#webhooks-api` | `webhook-console/dto/webhook-stats.dto.ts` |
| Test body, events, response fields | webhooks `#send-a-test-event`, `#webhooks-api` | `webhook-console/dto/send-webhook-test.dto.ts` |
| Test envelope `"test": true`, sent once, kept out of stats | webhooks `#send-a-test-event` | `partner-webhook/services/webhook-test.service.ts` |
| `unknown-event-type` `400`, lock not installed `404` | webhooks `#webhooks-api` | `lock-event-delivery/services/webhook-sample.service.ts` |
| Resend: queued, one attempt, same event id; `test-delivery`; `payload-unavailable` `409` | webhooks `#resend-a-delivery`, `#webhooks-api` | `webhook-console.service.ts` (`resend`); `call-partner-webhook.job.ts` (`resend`, `attempts: 1`) |
| 30 per extension per minute (`429`), `webhook-url-missing`, `webhook-target-not-public` | webhooks `#send-a-test-event` | `webhook-console.service.ts` (`checkSend`, `SENDS_PER_MINUTE`) |
| Subscriptions `GET`/`PUT`, `null` = every event, `invalid-id`, `duplicate-id` | webhooks `#webhooks-api` | `webhook-console/dto/webhook-subscriptions.dto.ts`; `webhook-console.service.ts` (`setSubscriptions`) |
| Console save does not change the revision or trigger review | webhooks `#choose-the-events-you-receive` | `partner-extension/services/partner-extension.service.ts` (`setWebhookSubscriptions` sets only `subscriptions` and `actionLogFeed`) |
| `action_log.created` switch, on unless off | webhooks `#choose-the-events-you-receive` | `action-log-webhook/listeners/create-webhook-on-action-log-created.listener.ts` (`actionLogFeed !== false`) |
| Matching: session list first, then extension; unset = all except own | lock-events `#choose-which-events-you-receive` | `lock-event-delivery/services/lock-event-subscriptions.service.ts` (`matches`) |
| Manifest `["*"]` = unset; `wildcard-not-alone`; omitted first upload `[]`, later kept; never held for review | manifest `#subscriptions`, changelog | `partner-extension/services/partner-extension-manifest.service.ts` (`MANIFEST_SUBSCRIBE_ALL`, subscriptions resolution); `partner-extension.service.ts` (`requestManifestReview` writes subscriptions directly) |
| `GET .../manifest` returns `["*"]` when unset | manifest `#subscriptions` | `partner-extension/mappers/partner-extension-manifest.mapper.ts` |
| Session `PUT` refuses `"*"`; `null` inherits | lock-events `#choose-which-events-you-receive`, manifest `#subscriptions` | `partner-extension/dto/session-subscriptions.dto.ts` (`MANIFEST_ID_PATTERN`) |
| UI labels | webhooks `#webhooks-tab` | `web/src/locales/en/developers.json` (`tabs.webhooks`, `webhooks.*`) |
| Endpoints in the API reference | webhooks `#webhooks-api` | `server/src/scripts/generate-swagger.ts` (`WebhookConsoleModule`) |

## Differences from `design.md`

- The design says an extension with "no manifest list" receives every event. The code sets `[]` when the **first** upload omits `subscriptions` (`(extension.revision ?? 0) > 0 ? extension.subscriptions : []`), which also replaces a list saved in the Webhooks tab. The pages say "no manifest uploaded yet and no list saved in the Webhooks tab" (R10), and state the first-upload exception in webhooks `#choose-the-events-you-receive` and the manifest `#subscriptions` info box.
- The `action_log.created` switch is labeled **Legacy feed** in the Subscriptions view (`webhooks.subscriptions.legacy`); the page names it.
- Screenshots skipped (design decision 6 allows it): no image references were added.

## Checks

All on 2026-11-05.

| Command | Input | Result |
| --- | --- | --- |
| `bash .claude/hooks/lint-docs.sh <file>` for the four pages | `6578c2c` | Pass. One existing warning on an untouched 2023 changelog heading. |
| `git diff --check` | `6578c2c` | Pass |
| `npx openspec validate ...` | - | Not available in this repo (no `openspec` package), skipped |
| `npm ci`, then `flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m env NODE_OPTIONS=--max-old-space-size=3072 npm run build` | `6578c2c` | Pass, no broken link or anchor warning (`onBrokenLinks: "throw"`) |
| Same build | `56f9c5a` (Mermaid quote fix) | Pass, no warning |
| `npx docusaurus serve --host 127.0.0.1 --port 4021`, curl and headless Chromium (Playwright) | `56f9c5a` | All 14 webhooks anchors, `manifest#subscriptions`, `lock-events#choose-which-events-you-receive` and `changelog#2026-11-05` exist; the "not available yet" caution is gone; the Mermaid diagram renders `No list, or ["*"]` with no syntax error; deep links scroll the heading to the top. Server stopped afterwards. |

### Review round 1 rework

Fixes R1 to R6, R8 and R9 from the review comment, on the four pages. R7 kept as written (real traffic always resolves an id). Chaster `main` is still `78e540eb`.

| Command | Input | Result |
| --- | --- | --- |
| `bash .claude/hooks/lint-docs.sh <file>` for the four pages | `62b4738` | Pass. Same existing 2023 changelog warning. |
| `git diff --check` | `62b4738` | Pass |
| Same build under the heavy-check lock | `62b4738` | Pass, `[SUCCESS] Generated static files in "build".`, no broken link or anchor warning |

### Review round 2 rework

R10: "no manifest uploaded yet and no list saved in the Webhooks tab" in webhooks `#lock-events-and-action-logs` and lock-events `#choose-which-events-you-receive`. Source: `partner-extension-manifest.service.ts` (a first upload without `subscriptions` sets `[]`).

| Command | Input | Result |
| --- | --- | --- |
| `bash .claude/hooks/lint-docs.sh <file>` for the four pages | `ff88c8f` | Pass. Same existing 2023 changelog warning. |
| `git diff --check` | `ff88c8f` | Pass |
| Same build under the heavy-check lock | `ff88c8f` | Pass, `[SUCCESS] Generated static files in "build".`, no broken link or anchor warning |

Rerun the build only if a page under `docs/` changes.
