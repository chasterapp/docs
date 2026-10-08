# Verification

## Proposal evidence (2026-10-08)

- CHA-1099 checkout confirmed assigned Proposer ownership, Docs project `703ada2c-6be0-478b-9d94-87465548de11` and execution workspace `1a277048-9941-46b3-ac47-757ef1b74b6c`.
- Safe-ticket-dispatch preflight passed against this issue/cwd. Remote is `https://github.com/chasterapp/docs.git`; branch is `CHA-1099-t03-repository-delivery-public-ai-review-api-and-disclosure-docs`.
- `git ls-remote --symref origin HEAD`, `git fetch origin main`, and `git rev-parse HEAD origin/main` confirm default main and both refs at `4497e7fe9102bae096b248efc67aa2657776ce6f`.
- GitHub App `gh pr list --repo chasterapp/docs --state open --json number,title,headRefName,isDraft` succeeded. No PR on this issue branch existed before proposal creation.
- Read README/package/config/lint hook, all five affected pages, the existing standalone-guide change and canonical T03 at Core `f94b3de4127b0067d5dea881026fcfbfef88faee`. No local specs or OpenSpec skills exist. Used the established Core OpenSpec propose procedure; no runtime requirement delta is needed.
- Downloaded attachment `5dff3341-ecb4-42fc-9d71-7d382c663e53` into run scratch. Python hashlib checks passed for ZIP and all three enclosed hashed files, with the exact values in design.md. Parsed manifest, fixture requests/history/callbacks and seven full OpenAPI schema components. The bundle is the durable input; scratch paths are not handoff dependencies.
- Read merged Core service/shared eligibility, partner source/discovery references and AI partner/shared lifecycle designs. Confirmed eligibility before attachment validation, source identity preservation, three terminal callback statuses, optional reason, and separate history/webhook count names.
- Read SDK origin/main `2cecc6b40c22bee1d6570fc356d1ef3f2e66d594` via git show, rather than its stale working tree. Verified existing verifications.create/search and package-root defineManifest export. Final AI/unavailable SDK compatibility remains a task for CHA-1098 coordination.
- Python normalized-JSON comparison passed for all seven `manifest.schemaPaths` entries against `partner-schemas.json` and full `api.json` components.
- `openspec status --change partner-ai-review-docs`: all three planning artifacts complete, specs explicitly skipped. `openspec validate partner-ai-review-docs --strict`: PASS.
- `npm run lint:docs -- <path>` exited 0 separately for proposal.md, design.md, tasks.md and this verification.md. The heading heuristic emitted two design warnings for numbered headings containing AI/SDK; these are sentence-case headings with acronyms, not title-case prose. `git diff --check`: PASS.

Only OpenSpec proposal artifacts change at this stage. No MDX implementation, docs build, rendering, runtime tests, deployment or feature activation has been performed. Implementation checks and exact command results will be added by Applier under tasks.md.

## Apply evidence (2026-10-08)

Workspace preflight passed for this issue, Docs project and isolated execution workspace. The branch remains unchanged. `git pull --ff-only`, `git fetch origin main` and `git ls-remote --symref origin HEAD` confirm default main at `4497e7fe9102bae096b248efc67aa2657776ce6f`. No AGENTS.md, CLAUDE.md or local apply skill exists; read repository guidance and ran `openspec instructions apply --change partner-ai-review-docs --json`.

Downloaded the fresh contract attachment using run authentication. ZIP and all three file hashes match design.md. The seven manifest schema paths equal the full OpenAPI components. An initial comparison used manifest aliases as excerpt keys; corrected the lookup to the component names and all seven comparisons passed.

Implemented only the five named guides and narrow verification support. AI request examples use the tested built-in and generic requests. History alternatives wrap one unchanged fixture row in an independent final page, so the reused synthetic ID is not presented as two real transitions. The original human payloads, generic IDs, custom reasons and source identity remain unchanged; only search filters gain unavailable.

### Mechanical example map

Run `python3 openspec/changes/partner-ai-review-docs/verify_examples.py <downloaded-bundle-directory>` on the managed host (requires its jsonschema package). The script checks hashes, all seven schema excerpts, nullable OpenAPI shapes, all JSON fences, original human payload preservation and absence of private/provenance fields. It requires nine exact fixture mappings:

| Page / JSON fence       | Bundle fixture                                                   |
| ----------------------- | ---------------------------------------------------------------- |
| peer-verifications / 4  | requests.builtin                                                 |
| peer-verifications / 5  | requests.generic                                                 |
| peer-verifications / 6  | created.body                                                     |
| peer-verifications / 7  | denied.body                                                      |
| peer-verifications / 8  | missingKeyholder.body                                            |
| peer-verifications / 12 | history.results[0], provider_error, in a one-row final page      |
| peer-verifications / 13 | history.results[1], eligibility_revoked, in a one-row final page |
| webhooks / 2            | callbacks.provider_error                                         |
| webhooks / 3            | callbacks.eligibility_revoked                                    |

Result: PASS, 17 parsed JSON fences, nine exact fixture mappings, six schema-valid callback variants. Human and AI verified/rejected callback data are equal in the bundle. Remaining examples validate against CreatePartnerPeerVerificationDto, PartnerPeerVerificationResponseDto, PartnerPeerVerificationHistoryPageDto, SearchPartnerPeerVerificationsDto, PeerVerificationEnded and PartnerVerificationPictureRequestDto. The settings declaration is an intentionally partial settings fragment, checked for exact unchanged content. The actor-only native body is unchanged. The error effects assert pre-media 403 and retained keyholder 409; effects are described as behavior rather than response fields.

Unavailable history has row-level reason, terminal endedAt, zero overall/criterion counts and empty counted reasons, while declared generic reasons remain. Callback reason is inside data and count aliases remain surface-specific. No new SDK snippet was added; the existing package-root defineManifest import and local extension import are preserved. Final SDK AI serialization/parser evidence from CHA-1098 is still pending; its issue was in proposal at the initial read. No npm publication or AI activation is claimed.

### Source checks

- `npm run lint:docs -- <path>`: PASS separately for each of the five changed MDX guides, no warnings.
- No formatter is configured in package.json or repository files. Ran `npx --yes prettier --write <five named MDX paths>` with no dependency/lockfile changes.
- `git diff --check`: PASS.
- `openspec validate partner-ai-review-docs --strict`: PASS.
- Capture warnings contain all four facts: experimental AI, image sent to an external AI service, possible mistakes and configured punishment risk. Partner guidance requires an equivalent warning before partner-owned capture/submission. Native warning placement is beside mode guidance. Unavailable is explicitly separate from rejection and does not trigger rejection punishments or fallback.

Build and rendered HTML inspection follow this pushed checkpoint. These results apply to the current five MDX inputs and bundle hashes; edits to payloads, disclosure or links invalidate the respective checks.

### Build, links and rendered disclosure

- Tested public source commit: `af3679338a504fa9f3ffdf805daa57c6f4333a3d`. Command: `NODE_OPTIONS=--max-old-space-size=3072 flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m npm run build`. Final result: exit 0, generated static output and indexed all 66 documents. Lock acquired immediately. No broken route/fragment/Markdown-link warnings. Existing Docusaurus upgrade and Browserslist maintenance notices only.
- Initial symlinked shared dependencies compiled but failed rendering 63 existing routes with `TypeError: Cannot read properties of undefined (reading 'id')` in DocItem. One local repair removed the symlink, ran locked `npm ci --no-audit --no-fund` (exit 0, 1384 packages), then `npm run clear`. The subsequent locked build passed. Tracked dependency/configuration inputs are unchanged; shared services and shared dependencies were not modified.
- Parsed final HTML article content, code blocks, caution styling, current-page sidebar links and all local article route/fragment targets. All five routes below passed. Partner and native capture guidance contains all four disclosure facts inside a caution admonition; the webhook page renders both unavailable envelopes and data-level reason. No service was started and ports 3000/3001 were not used.
- Portable report uploaded and registered as an artifact work product: [rendered HTML checks](/api/attachments/f726c47d-8a5d-45a1-a911-1da1eba39c34/content). Static inspection verifies generated content and structure, not browser layout.

| Built route                                                       | Nonempty code blocks | Checked local article links | Result |
| ----------------------------------------------------------------- | -------------------- | --------------------------- | ------ |
| /api/extensions-api/create-your-extension/peer-verifications      | 16                   | 15                          | PASS   |
| /api/extensions-api/create-your-extension/webhooks                | 3                    | 15                          | PASS   |
| /api/extensions-api/interact-with-extensions/verification-picture | 1                    | 13                          | PASS   |
| /extensions/verification-picture                                  | 0                    | 15                          | PASS   |
| /extensions/tasks                                                 | 0                    | 17                          | PASS   |

These results remain valid through evidence-only edits. Changes to the five public pages, package/configuration, linked targets or the upstream contract require corresponding rechecks.

### Pending SDK compatibility

[CHA-1098](/CHA/issues/CHA-1098) has [draft Extensions PR #55](https://github.com/chasterapp/extensions/pull/55). Observed head `cb6438e75834c95d3b3a44b49d2d133279bfd579` still lacks a posted completed AI serialization/unavailable parser verification. Its latest stage handoff is propose to apply. Requested the concrete PR/head, scoped results and shared OpenAPI hash there in comment `2ac56bce-3432-4e98-9772-4da5c8a99ce5`; independent Docs implementation/build/render checks are complete.

Task 4.2 and final Simplifier handoff 5.1 remain open until that compatibility evidence is available. This is an existing repository dependency, not a request for new permission. Docs remains on its one draft PR. Partner AI activation, publication and deployment are separate from these source changes.
