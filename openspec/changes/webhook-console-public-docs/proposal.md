# Proposal

## Why

Chaster now records every webhook delivery, shows it in a new **Webhooks** tab of the Developer Interface, and lets developers resend a delivery, send a test event, choose their lock event subscriptions and turn `action_log.created` off. Every notification also carries three new headers (`X-Chaster-Event`, `X-Chaster-Event-Id`, `X-Chaster-Attempt`) so partners can tell a retry from a new event. A manifest can now subscribe to everything with `subscriptions: ["*"]`, and omitting `subscriptions` in a later upload keeps the current setting instead of emptying it.

The public docs still say the debug section "is not available yet", tell developers to deduplicate on body fields only, and warn that a manifest without `subscriptions` stops deliveries, which is no longer the rule. Partners need pages that match the shipped server so they can debug their own integration without asking on Discord.

## What changes

- `docs/api/extensions-api/create-your-extension/webhooks.mdx`: replace the "Debugging" placeholder with the Webhooks tab; add request headers and deduplication; rewrite retries with the 5-attempt schedule and what counts as a failure; add delivery statuses, resend, test events, the `action_log.created` switch and subscriptions, and the `webhooks` developer API endpoints; update "Lock events and action logs" to use the switch and the shared event id.
- `docs/api/extensions-api/extension-communication/manifest.mdx`: rewrite the `#subscriptions` section and its warning to the D02 rule, document `subscriptions: ["*"]`, and fix the "A list you omit becomes empty" sentence for `subscriptions`.
- `docs/api/extensions-api/extension-communication/lock-events.mdx`: update `#choose-which-events-you-receive` (diagram and bullets) for `["*"]`, the Webhooks tab and session `null`; mention the headers in "Delivery".
- `docs/api/changelog.mdx`: new `2026-11-05` entry (the day T03, chasterapp/chaster#1721, merged).
- Screenshots of the Webhooks tab in `static/img/`, captured from a private dev stack, if capture is possible (see design, decision 6).

## Capabilities

### New capabilities

None. This change documents shipped behavior and sets `skip_specs: true`.

### Modified capabilities

None. No API or runtime requirement changes.

## Out of scope

- No server, web or API client change. Any mismatch found between these docs and chaster `main` is reported on the issue, not fixed here.
- No new docs page and no `sidebars.json` change: the work extends the pages from chasterapp/docs#22.
- `action.invoke` (broker calls) keeps its own headers and page; only a one-line note that the new headers do not apply to it.
- Stats internals (rollup buckets, diagnosis thresholds beyond the one sentence the banner needs) and admin-only access.
- Publishing the site.

## Impact

Repository: `chasterapp/docs`, default branch `main`. Changes are limited to the four pages above, optional images in `static/img/`, and this OpenSpec change.

Feature switch: none. The server shipped without a switch (project `design.md`, Rollout and rollback).

Sensitive surfaces: none per the ticket. It documents a public webhook and API contract, so every claim must trace to a file on chaster `main` (design, Sources).

Merge: autonomous (owner decision on CHA-1540, 2026-11-05). QA: none; the docs build and the claim trace are the checks.

Canonical scope: chaster `main` `78e540eb`, `docs/projects/webhook-console/epics/E01-webhook-console/T04-public-docs.md`, with `design.md`, decisions D02, D03, D04 and `mockup.html`. T03 (#1721) and T05 (#1722) are merged.
