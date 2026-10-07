# Design

## Context

See `proposal.md` for motivation. This Docusaurus 3 repository uses MDX frontmatter, explicit document IDs in `sidebars.json`, and root-relative public routes. Its tone checker is `.claude/hooks/lint-docs.sh`; headings use sentence case and prose avoids em dashes. There are no repository AGENTS.md, DESIGN.md, existing OpenSpec specs or repository-local OpenSpec skills at the proposal baseline. The established Chaster OpenSpec propose procedure was used to create this change.

Verified default refs on 2026-10-07:

- Docs: `bd01490` (the issue branch was advanced to this baseline without changing its name).
- Core: `b377de001321898bc2916cfb6aa0159427c51698`.
- Extensions: `ed8293f967cc62499a116b36494b7e4cebf5a479`.

The approved planning source remains Core `354d6256778b0c7dee5aa639d9f487456dad9ec6`, `docs/projects/extension-verifications/`, including T10 and D01-D06. Implementation facts come from the merged contracts, rather than older planning examples. Refresh default refs before applying and record any relevant contract changes.

### Contract sources

Read these paths at the pinned Core revision:

- `server/src/modules/partner-extension/controllers/partner-session-files.controller.ts`, `services/partner-session-files.service.ts`, `services/partner-file-token.service.ts`, and `dto/partner-{upload-file,file}-response.dto.ts`.
- `server/src/modules/partner-extension/controllers/partner-peer-verifications.controller.ts`, `services/partner-peer-verifications.service.ts`, `mappers/partner-peer-verifications.mapper.ts`, and the creation/search/history/response DTOs under `dto/`.
- `server/src/modules/partner-extension/models/partner-verification-type.model.ts` and the update DTO for declarations.
- `server/src/modules/peer-verification/dto/{peer-verification-source,review-check-result}.dto.ts`, the generic-check model, creator service and verdict completion service.
- `server/src/modules/partner-webhook/models/webhooks/peer-verification-ended.model.ts`, its listener and shared transport job.
- `api-client/src/api.ts`, existing specs `partner-session-files`, `partner-session-review-history`, `developer-verification-kind-authoring`, and the verdict change `originating-peer-verification-verdict`.

At the pinned Extensions revision, compare `packages/extension-server/src/chaster/generated/chaster-api.ts`, `generated/webhooks/`, `chaster/verifications.ts`, `chaster/client.ts`, HTTP client helpers, and manifest validation/sync. Read executable usage in `tooling/smoke-session-files.ts`, `tooling/smoke-session-peer-verifications.ts` and `tooling/smoke-peer-verification-verdict.ts`. These are example references, not a requirement to rerun upstream integration suites or disclose their runtime credentials.

## Goals / non-goals

**Goals:** A reader can declare a kind, upload a private image through their backend, create a standalone review, save the review ID, page through history and safely react to a verdict using the delivered fields.

**Non-goals:** No API/schema/runtime change, new delivery guarantee, quota, cancellation, correlation field, action framework, native extension conversion or live publication. No new application controls, EN/FR UI strings or analytics events are needed for static guides.

## Decisions

### Place standalone guides with extension-author documentation

Add `docs/api/extensions-api/create-your-extension/files.mdx` and `peer-verifications.mdx`, beside custom data and webhooks. Group them under Create your extension in `apiSidebar`. Extend `webhooks.mdx`, add a narrow rejection-action cross-link in `lock-actions.mdx`, and link from authentication/sessions where useful.

Keep `interact-with-extensions/verification-picture.mdx` as the native request-only flow. Add its missing sidebar entry under Interact with extensions and reciprocal links explaining that standalone review creation does not require the native Verification Picture extension. This prevents two similarly named workflows from appearing interchangeable.

Use existing MDX conventions, admonitions, code fences and links. No images or dependencies are necessary. Keep these planning artifacts outside the public `docs/` content tree.

### Document private files as backend resources

Show bearer-authenticated cURL against `https://api.chaster.app/api/extensions/sessions/:sessionId` with synthetic session/file IDs, a synthetic local image path and placeholder secrets. Do not execute examples against the public host. Let cURL set multipart boundaries; do not set a JSON Content-Type for upload.

| Operation | Delivered contract |
| --- | --- |
| POST `/files` | Multipart `file`, optional future ISO `expiresAt`; 201 `fileId`, `attachmentToken`, `expiresAt` |
| GET `/files/:fileId` | 200 `fileId`, `originalName`, processed-byte `size`, nullable `expiresAt`, temporary `url` |
| DELETE `/files/:fileId` | Empty 204 for unattached media; 409 if any review references it |

Explain developer-token authentication for the owning application/session, server-derived partner/session/lock/wearer ownership and active-lock upload. V1 accepts decoded JPEG, PNG and GIF images using the current byte limit and wearer storage-space quota. Confirm the numeric limit from Core constants if stating it.

Default unattached expiry is one hour. Explicit expiry must be future; no new retention cap exists. Temporary GET URLs last at most 120 seconds and cannot outlast file expiry. Attachment tokens are separate signed, session-bound credentials; they grant no public media access and cannot substitute for native upload tokens.

Successful creation clears expiry. Referenced media is retained for ongoing review and history after verdict/lock end under existing deletion/moderation cleanup. GET remains available after lock end while the session exists and authorization succeeds. Expired/deleted/foreign resources return 404; deleted sessions follow session-guard behavior. No browser developer credentials, arbitrary URL import or permanent public media URL.

### Use the delivered creation and history shapes

Start with a `verificationTypes` declaration `{ key, label, description? }`: unique extension-local keys matching `^[a-z0-9-_]{1,40}$`, label 1..60 characters and optional description up to 300. Cover portal/manifest setup and omitted/empty/null update semantics: omitted preserves, `[]` clears, `null` rejects. Removing/renaming a kind affects future creation; stored reviews retain their kind and criteria labels. `verificationTypes` is distinct from each review's `verificationType` response.

The creation example uses `verificationTypeKey`, returned `attachmentToken`, `visibility: all_members`, optional `delay` and `maxVotes`, two generic checks with distinct IDs, and `punishments: [{ name: "add_time", params: 3600 }]`. Reusing a reason slug on different checks is valid; show different reason text to explain criterion-local counts. Each generic check includes `name`, `id`, `title`, `description` and a nonempty `rejectionReasons` array of unique `{slug, text}` entries. Titles/descriptions are plain text with 60/300 bounds. Built-in families remain supported; repeated built-in families require explicit IDs.

201 returns `_id`, status, `source`, `verificationType`, checks, punishments, timestamps and aggregate check counts. Save `_id`; do not label it `peerVerificationId` in the creation response. Source presentation is server-owned, including community classification. `punishments` uses the existing seven LockAction variants and defaults to `[]`. Chaster executes the snapshotted list on rejection; no Penalties extension is required and the partner must not repeat those actions in its callback.

Community delay is 900..21600 seconds, default 21600. Optional maxVotes is 3..100; omitted means no vote cap. At least 75% approval passes; timeout with zero votes passes without fabricating criterion approvals. Keyholder review has no timeout and ignores valid community timing/quorum settings. Missing/ineligible keyholder is 409, with no community fallback or automatic success. Suspended wearer is 403. Invalid schemas, undeclared kinds, checks/actions are 400; foreign media is 404; invalid/expired attachment credentials are 403. Use the active-lock guard's actual error rather than inventing a status.

Search uses POST `/peer-verifications/search`, optional `criteria: {statuses, verificationTypeKeys}`, default limit 20 (1..100) and optional ObjectId `cursor`. Omitted/empty filters include all statuses/kinds, including retired keys. Results are scoped to both partner and session, sorted by descending `_id`, and return `{results, hasMore, nextCursor?}` without total count. Send `nextCursor` only when `hasMore`; do not use session-search `paginationLastId`/`count` conventions here.

History remains readable after lock end while the session exists; deleted sessions return 404. Each row includes `source`, `verificationType`, timestamps, nullable `maxVotes`, checks, punishments, vote totals and criterion-local reason counts. It excludes media credentials and voter identities. Creation has no idempotency key or exact request correlation: an ambiguous POST can have created a row, so inspect history before retrying and do not claim search identifies the request exactly.

### Preserve the webhook's distinct result shape and delivery limits

Add one complete synthetic `peer_verification.ended` envelope to `webhooks.mdx`: `event`, `sentAt`, attempt-specific `requestId`, and `data` with creating `sessionId`, `extension.slug`, `lockId`, `peerVerificationId`, `verificationTypeKey`, terminal `status`, `endedAt`, `voteCounts` and `checkResults`.

| Surface | Criterion totals | Reason totals |
| --- | --- | --- |
| Creation and webhook `ReviewCheckResultDto` | `nbVerifiedVotes`, `nbRejectedVotes` | `rejectionReasons[].nbVotes` |
| History `PartnerPeerVerificationCheckResultDto` | `approved`, `rejected` | `rejectionReasons[].count` |

Preserve `checkId`, `name`, `checkIndex`, `subcheckName` as emitted by each mapper; history's `name` is its subcheck name. Do not invent per-check verdicts. Generic check identity and its stored reason text keep identical slugs from different criteria separate.

Delivery targets only the creating partner/session at its configured callback URL, never every extension on the lock. Explain existing authentication and prompt 2xx acknowledgment. Partners deduplicate durable work by `(peerVerificationId, event)`, not `requestId`, which changes on retry. Payloads contain no media URLs/bytes/tokens or voter identities.

Verdict is stored before rejection actions; actions run sequentially before event emission. Action failure or interruption may leave partial actions and prevent enqueue. There is no added recovery or exactly-once delivery promise. Lock-end bulk closure emits no verdict callback and runs no rejection actions; already queued/retried callbacks may arrive after lock/session termination. The handler must tolerate that and avoid blindly resolving a deleted session. History is the inspection fallback, not a delivery-repair API. Scope any corrections to shared webhook prose to claims required by this new event.

## Risks / trade-offs

- Schema drift: revalidate the generated Core and Extensions contracts, mappers and examples at application time; record refs and a field cross-check in `verification.md`.
- Misleading delivery guarantees: retain the explicit limitations above and distinguish overall zero-vote approval from answered criterion counts.
- MDX/navigation failure: lint, build and inspect the built new pages and their sidebar/cross-links. The config throws on broken links; Markdown warnings still need inspection.
- Sensitive examples: only synthetic IDs, placeholder tokens/private URLs and benign synthetic media; never copy a live response or fixture credential into docs/evidence.
- Shared-host contention: checkpoint and push before the docs build; serialize it with the host heavy-check lock and a bounded timeout. Do not start services on ports 3000/3001.

## Migration plan

No data migration or runtime rollout. Normal review and exact-head verification precede repository merge. Documentation deployment is outside this slice's acceptance. Reverting the documentation source has no effect on stored reviews or API behavior.
