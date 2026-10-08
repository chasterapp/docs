# Tasks

## 1. Confirm the contract

- [ ] 1.1 Run workspace preflight for CHA-1099 and fetch Docs default main without changing the issue branch. Re-read repository guidance and download the contract bundle into run scratch. Verify all hashes in design.md and equality of its seven schema excerpts with the full OpenAPI; record refs, commands and results in verification.md.
- [ ] 1.2 Build an example-to-fixture map covering built-in/generic AI requests, 201 response, 403 error/effects, keyholder 409, both unavailable history alternatives and all human/AI callback variants. Verify each surface's reason placement/count aliases and identify independent alternate outcomes with the reused synthetic review ID.

## 2. Extend partner guides

- [ ] 2.1 Update create-your-extension/peer-verifications.mdx with built-in/generic AI requests and ongoing response, current wearer OR keyholder eligibility, per-request evaluation, null AI timing/quorum, pre-media 403, unchanged keyholder 409, backend model selection, no fallback and bounded processing/ambiguous POST guidance. Preserve generic IDs/custom reasons/source and existing human examples. Verify the JSON map against fixtures/OpenAPI and run npm run lint:docs -- docs/api/extensions-api/create-your-extension/peer-verifications.mdx.
- [ ] 2.2 Add unavailable history alternatives and status-filter examples for both reasons, zero counts/empty counted reasons, terminal endedAt and no punishment on unavailable. Verify row-level unavailableReason, history aliases, all-status pagination and exclusion of private feedback/provenance against fixtures/schemas; lint the peer-verifications page again after edits.
- [ ] 2.3 Update create-your-extension/webhooks.mdx with complete fixture-backed unavailable envelopes for both reasons, data.unavailableReason, zero counts, unchanged verified/rejected semantics, no fallback and Chaster-owned punishment behavior. Retain retry/deduplication and action/delivery limitations. Verify all callback fields against bundled fixtures/OpenAPI and run npm run lint:docs -- docs/api/extensions-api/create-your-extension/webhooks.mdx.

## 3. Explain capture and disclosure

- [ ] 3.1 Add an experimental external AI warning and configured punishment risk to the partner review guide, requiring an equivalent warning before partner-owned capture/submission. Keep unavailable separate from rejection. Verify the warning's four required facts by inspection and lint the page.
- [ ] 3.2 Update interact-with-extensions/verification-picture.mdx with native configured review-mode/disclosure guidance and the standalone AI distinction, keeping its actor-only request contract. Verify no visibility/model field or unsupported import is added, cross-links resolve, and run npm run lint:docs -- docs/api/extensions-api/interact-with-extensions/verification-picture.mdx.
- [ ] 3.3 Update docs/extensions/verification-picture.mdx and tasks.mdx with focused AI eligibility, experimental external processing, possible mistakes/punishment risk and unavailable/no-fallback guidance. Preserve human behavior and avoid invented UI labels. Verify the disclosure appears beside relevant mode/capture guidance and run npm run lint:docs -- docs/extensions/verification-picture.mdx and npm run lint:docs -- docs/extensions/tasks.mdx as separate commands.

## 4. Verify compatibility and rendering

- [ ] 4.1 Mechanically parse every JSON fence in all modified MDX pages; compare mapped examples to the tested bundle and remaining examples to corresponding OpenAPI shapes. Record counts, mappings, zero-count/reason/private-field checks and commands/results in verification.md. Verify retained human payloads and source/custom reason identity; run git diff --check and openspec validate partner-ai-review-docs --strict.
- [ ] 4.2 Obtain CHA-1098's actual PR/head or merge and scoped AI serialization/unavailable parser evidence using the same core hash. Verify every SDK snippet uses existing verifications.create/search and supported package exports; record compatible runtime commit evidence without inventing npm publication. Continue independent checks while this evidence is pending; surface any observed mismatch to Founding Engineer.
- [ ] 4.3 Inspect git status, commit all issue-owned changes and push before the Docusaurus build. Announce possible contention, then run NODE_OPTIONS=--max-old-space-size=3072 flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m npm run build. Record tested commit/exit status and inspect warnings; fix every newly introduced broken route/fragment/Markdown link, checkpoint before any necessary repeat. No deployment or ports 3000/3001.
- [ ] 4.4 Inspect the built HTML and navigation for all five pages, readable examples, both unavailable reasons and prominent disclosure/punishment language. Capture portable rendered evidence (static inspection or a temporary server on an available port outside 3000/3001, stopped afterward). Record page paths/results in verification.md and register any screenshot/report deliverable as an issue artifact.

## 5. Hand off this delivery

- [ ] 5.1 Push final documentation/evidence, update this same draft PR's apply marker and final scope, and reassign this same issue/branch/PR to Simplifier using one combined PATCH. Verify work-product linkage, head SHA, core hash and sensitive-surface/evidence links in the handoff. Preserve QA: none and current user-authored merge policy; Reviewer later closes this carrier after merge and returns its actual merge/verification to the still-open T03 owner once.
