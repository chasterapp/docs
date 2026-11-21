# Design

## Context

See [proposal.md](./proposal.md) for the outcome and scope. Docs default `main` and this branch both resolve to `4497e7fe9102bae096b248efc67aa2657776ce6f` on 2026-10-08. Safe-ticket-dispatch preflight passed for CHA-1099, its Docs project and this isolated worktree. GitHub App PR metadata access and HTTPS fetch succeeded.

This repository has no AGENTS.md, CLAUDE.md, DESIGN.md, `.claude/rules/`, `docs/reference/`, OpenSpec specs or local OpenSpec skills. Read README.md, package.json, `.claude/hooks/lint-docs.sh`, docusaurus.config.js and all five affected MDX pages. Use the established Core OpenSpec propose procedure, with docs-only `skip_specs: true`, as the existing `extension-file-and-review-guides` change does. That earlier change documents the human API and its verification evidence; leave its artifacts intact.

Docusaurus uses root-relative document routes, frontmatter, Markdown code fences and admonitions. Headings use sentence case; the tone hook rejects em dashes and accepts one file per invocation. `onBrokenLinks: "throw"` and `onBrokenMarkdownLinks: "warn"` require inspection of build warnings. Existing public guides distinguish standalone partner uploads/reviews from native photo requests. Keep that distinction.

### Contract evidence

- Core PR: https://github.com/chasterapp/chaster/pull/981, merge `b8dcc69487d389aab787acc699ec0ddc42a549f6`.
- Verified bundle: Paperclip attachment `5dff3341-ecb4-42fc-9d71-7d382c663e53`; download via `/api/attachments/5dff3341-ecb4-42fc-9d71-7d382c663e53/content?download=1` using managed run authentication into run scratch.
- ZIP SHA-256: `af7210cb7c0ecc885d3f364527696e5e0fafdf2cfac61d3ea889cf355480426c`.
- Bundle source: `989e06d6a889e7cbff7f66a11e21605269a03bfb`. Founding Engineer verified unchanged production source through merge.
- OpenAPI `api.json` SHA-256: `606622d1547ab06788ff3be247c617a9c1bf98d60b6e702a093dbafa2c053d2d`.
- `fixtures.json` SHA-256: `23fdf433456b8a0c43279d15246889287105c30eab719dec2e4736b812c2fd8d`.
- `partner-schemas.json` SHA-256: `a9b77f10df6e54a352bf7ab29124d03eba1c364d5e6149f1ad181c587b08bbb5`.

All four hashes were checked during proposal exploration. `manifest.json.schemaPaths` identifies seven schemas; compare every excerpt to its full OpenAPI component before using it. Read merged Core `PartnerPeerVerificationsService`, the shared eligibility service, partner source/discovery references and `ai-partner-peer-reviews` design. These confirm the pre-media 403, independent creator eligibility recheck, retained source/criteria, null AI deadline/vote cap and conditional unavailable handling.

## Goals / Non-goals

**Goals:** A partner can choose AI using the delivered request contract, warn the wearer, inspect all terminal outcomes and handle callbacks without inventing votes, punishments or retry guarantees.

**Non-goals:** No alternative facade, new provider setting, consent enforcement API, callback recovery mechanism, application controls, runtime contract change or public-site deployment. Do not modify a shared source checkout or the SDK carrier's branch.

## Decisions

### 1. Extend the existing partner review guide

Keep the existing community request/response/history example and its two generic checks with independent IDs and criterion-local `unclear` reasons. Add a dedicated AI section using `fixtures.requests.builtin`, `fixtures.requests.generic` and `fixtures.created.body`. These demonstrate the same creation route, declared kind, signed attachment credential and active-lock ownership rules. AI accepts built-in `task`, `chastity_device`, `bondage` and generic checks; IDs, exact custom reason sets and stored source identity retain their human semantics. Do not invent built-in reason slugs for generic checks.

Explain that current eligible wearer OR current eligible keyholder cohort access permits AI for an otherwise valid active lock. An eligible wearer can use AI without a keyholder. Saved configuration, developer identity or a previous availability response does not grant access. Eligibility is evaluated for each request and again during processing. Do not promise a participant/cohort identity field or permanent entitlement. Preserve suspension/authentication/ownership restrictions.

When neither participant qualifies, creation returns 403 before attachment validation, review creation, expiry/retention changes or queueing. Use the exact error from `fixtures.denied.body`, and explain the observed effects separately, not as response fields. Keep keyholder visibility's 409 and no fallback. AI ignores valid human duration/quorum settings and has no community timer; the created response has `endsAt: null`, and history has `maxVotes: null`.

Model/provider selection is backend operational configuration. Partners submit criteria and visibility, never a provider/model field. Do not name an inference host, promise photo accuracy, or document credentials.

### 2. Preserve each surface's result shape

| Surface | Unavailable reason location | Criterion totals | Reason totals |
| --- | --- | --- | --- |
| Creation / review response | `unavailableReason` when unavailable | `nbVerifiedVotes`, `nbRejectedVotes` | `nbVotes` |
| History row | `results[i].unavailableReason` | `approved`, `rejected` | `count` |
| Verdict callback | `data.unavailableReason` | `nbVerifiedVotes`, `nbRejectedVotes` | `nbVotes` |

History status filters accept `ongoing`, `verified`, `rejected`, `unavailable`; terminal callbacks accept the latter three. `unavailableReason` is optional and only emitted for unavailable. It is `provider_error` after failed/exhausted processing or `eligibility_revoked` when cohort eligibility is lost before completion. These outcomes have zero overall/criterion votes, empty counted rejection reasons, a terminal `endedAt`, no rejection punishment and no automatic approval, rejection, keyholder or community fallback.

Keep declared `checks[].rejectionReasons` even when counted result reasons are empty. Preserve `checkId`, `checkIndex`, `subcheckName`, source and stored kind. Keep human verified/rejected examples with no unavailable reason. AI real verdicts use the same human result semantics and can execute configured rejection punishments. Partner response/callback examples expose no private feedback or machine-voter/provider/model/prompt provenance.

Add unavailable examples in both partner review history and webhooks. The bundle reuses one synthetic review ID for alternate terminal test outcomes; present them as independent alternatives, not two transitions for one real review. Use complete callback envelopes from `fixtures.callbacks.provider_error` and `.eligibility_revoked`, not a reason at the envelope root. Compare any edited illustrative history pagination wrapper separately from its unchanged fixture row.

### 3. Explain bounded processing and safe partner handling

Distinguish Chaster's bounded AI processing retries from webhook delivery retries and partner creation retries. Processing failure can end unavailable; a validated rejection is a verdict, not an instruction to retry. Explain bounded retries without a timing SLA or a fresh inference budget promised to partners. Keep the existing webhook retry schedule and deduplication by `(peerVerificationId, event)`, not attempt-specific requestId. Preserve action-before-callback and lock/session termination limitations.

Keep the existing ambiguous-POST caution prominent: no creation idempotency/correlation key exists; a failed/disconnected request may have persisted a review. Save a returned ID, inspect history when uncertain and assess duplication before deciding whether to submit again. History cannot prove exact request correlation. Do not suggest blind automatic POST retry, action replay or automatic audience changes.

### 4. Put the disclosure beside AI capture and selection guidance

Use a caution admonition that states AI review is experimental, the image is sent to an external AI service, AI can make mistakes, and a rejected review can trigger configured punishments. Tell partners to display an equivalent warning before their own photo capture/submission. Chaster cannot enforce a third-party interface warning. Do not imply AI unavailability itself causes punishment.

Add focused AI guidance to `docs/extensions/verification-picture.mdx` and `tasks.mdx`, retaining existing human options and explaining request-time eligibility regardless of saved settings. Native loss of availability does not grant human fallback or automatic validation; describe unavailable as a processing outcome, not a failed check. Avoid inventing control labels or a new UI.

The native request endpoint's body remains `{ "actor": "extension" }`. Update its interaction guide to explain that it requests a photo through the native extension's configured review mode, and distinguish it from partner-created AI reviews. Include/link the disclosure without adding visibility/model fields to that request. Avoid broad edits to the general Verification feature page, which is outside this carrier's named scope.

### 5. Verify against core and the existing SDK

Mechanically parse every JSON fence in modified pages. Build an explicit example-to-fixture map for AI requests, creation, denied error, history alternatives and callbacks. Compare normalized JSON values to the bundle; validate other examples against the corresponding OpenAPI request/response schemas or document their intentional illustrative wrapper. Compare all seven excerpt schemas with full OpenAPI, check enum values and absence of private/provenance fields, and preserve legacy verified/rejected semantics. Record commands and example mappings in this change's verification record; a prose claim alone does not establish compatibility.

SDK baseline evidence: Extensions `origin/main` at `2cecc6b40c22bee1d6570fc356d1ef3f2e66d594` has `src/chaster/verifications.ts` reexporting `src/verifications/definitions.ts`, `HttpChasterClient.verifications.create(sessionId, input)` and `.search(sessionId, query)`, and the supported package-root `defineManifest` export. Use the existing facade and supported imports for any new SDK snippet. Retain the current manifest snippet. Do not invent a helper or hand-edit generated types. CHA-1098 owns additive AI/unavailable SDK changes; before final signoff, obtain its actual PR/head or merge and scoped serialization/parser evidence using the same OpenAPI hash. This coordination does not block independent docs implementation.

Before the docs build or any generator/heavy check, inspect status, commit all issue-owned files and push. Announce possible contention; use `flock --verbose /tmp/chaster-recovery-heavy-check.lock npm run build` in this Docs worktree. This Docusaurus build is permitted. Run `npm run lint:docs -- <path>` separately for each modified MDX page. Review all warnings, fix newly introduced broken links and inspect built HTML/navigation for disclosure placement and both unavailable examples. Save portable rendered evidence as an issue artifact or committed verification record. Do not serve on ports 3000/3001 or run deploy commands.

## Risks / Trade-offs

- Older strict SDK consumers reject unavailable: require CHA-1098 compatibility evidence and keep partner AI disabled until compatible deliveries exist.
- Surface-specific count aliases can drift: use the tested fixture map and OpenAPI comparison, retaining legacy examples.
- AI mistakes can trigger punishments: make the warning visible at the integration/capture guidance and retain human judgment about capture.
- Stored AI configuration can outlive access: explain per-request eligibility, pre-media 403 and unavailable processing explicitly.
- Retry advice can create duplicate reviews: retain the ambiguous POST limitation and separate three kinds of retry.
- Public disclosures and contracts are sensitive: flag them in the PR and every handoff; Reviewer applies the user-authored merge policy.

## Migration plan

Only source documentation changes ship through this PR. Reviewer returns actual merge SHA, core hash and verification to the still-open T03 Founding Engineer owner after this carrier completes. No package publication, website deployment, partner adoption or feature activation is performed here. Those acts remain separate.

## Open questions

None that change the approved scope. CHA-1098's final compatibility evidence is collected during verification before signoff.
