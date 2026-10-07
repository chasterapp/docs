# Implementation verification

## Contract baseline

Refreshed all three default refs and fast-forward pulled the existing issue branch on 2026-10-07. None of the contract refs changed from the proposal:

- Docs: `bd0149089701fc009ec93b3bb330fa771c91b96d`.
- Core: `b377de001321898bc2916cfb6aa0159427c51698`.
- Extensions: `ed8293f967cc62499a116b36494b7e4cebf5a479`.

Source was read with `git show origin/main:<path>` from the registered repository clones. This uses merged source rather than another issue's uncommitted work. The docs issue workspace preflight passed and PR #18 resolves to this branch. GitHub App metadata access passed; HTTPS fetch/pull uses the host credential helper.

## Route and field cross-check

All routes below begin `/api/extensions/sessions/:sessionId`. Examples use synthetic session strings, 24-character synthetic ObjectIds, placeholder bearer/attachment credentials and an `.invalid` private-media URL. No request was sent to the public API.

| Operation                         | Request                                                                                                       | Response                                                                                                                                                                                     | Source checked                                                                                                                                                                                             |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST `/files`                     | Multipart `file`, optional future ISO `expiresAt`                                                             | 201 `fileId`, `attachmentToken`, `expiresAt`                                                                                                                                                 | Core file controller, upload DTO, response DTO, mapper, file/token services; SDK generated types, HTTP wrapper and `tooling/smoke-session-files.ts`                                                        |
| GET `/files/:fileId`              | Developer authentication, same owning session                                                                 | 200 `fileId`, `originalName`, processed-byte `size`, nullable `expiresAt`, temporary `url`                                                                                                   | Core file controller/mapper/service/repository; SDK file smoke assertions                                                                                                                                  |
| DELETE `/files/:fileId`           | Same owner; unreferenced media                                                                                | Empty 204; referenced media 409                                                                                                                                                              | Core file controller/service; SDK smoke deletion assertions                                                                                                                                                |
| POST `/peer-verifications`        | `verificationTypeKey`, `attachmentToken`, `visibility`, `checks`, optional `delay`, `maxVotes`, `punishments` | 201 `_id`, status, source, kind, checks, punishments, timestamps, aggregate counts                                                                                                           | Core creation DTO/service/mapper and generated `api-client/src/api.ts`; SDK generated API, `chaster/verifications.ts`, `chaster/client.ts`, HTTP wrapper and `tooling/smoke-session-peer-verifications.ts` |
| POST `/peer-verifications/search` | Optional `criteria.statuses`, `criteria.verificationTypeKeys`, limit 1..100 (default 20), ObjectId `cursor`   | 200 `results`, `hasMore`, optional `nextCursor`; no total count                                                                                                                              | Core search/history DTOs, history service and mapper; SDK search schema/generated client and HTTP wrapper                                                                                                  |
| Extension declaration             | `verificationTypes: {key,label,description?}[]`                                                               | Omitted preserves, empty clears, null rejects                                                                                                                                                | Core kind model, update DTO/service; portal VerificationTypes form; SDK `define-manifest.ts`, CLI manifest derivation and sync apply/diff                                                                  |
| Verdict callback                  | Origin-only configured callback; terminal review                                                              | `event`, attempt-specific `sentAt`/`requestId`, `data.sessionId`, `extension.slug`, `lockId`, `peerVerificationId`, `verificationTypeKey`, `status`, `endedAt`, `voteCounts`, `checkResults` | Core webhook model, projection, origin listener, transport job and completion service; SDK generated webhooks and `tooling/smoke-peer-verification-verdict.ts`                                             |

Core module paths: `server/src/modules/partner-extension/{controllers,dto,services,mappers,repositories,models}/`, `server/src/modules/peer-verification/{dto,helpers,listeners,services}/` and `server/src/modules/partner-webhook/{models/webhooks,jobs}/`. Generated SDK paths: `packages/extension-server/src/chaster/generated/{chaster-api.ts,webhooks/}`.

### Important mapper and behavior checks

- Creation returns `_id`; webhook `peerVerificationId` is the same identifier. Creation does not expose `maxVotes`; history does, nullable. Presentation source includes server-owned community classification.
- Creation/webhook criteria use `nbVerifiedVotes`, `nbRejectedVotes`, reason `nbVotes`. History maps these to `approved`, `rejected`, reason `count`, and maps `name` to `subcheckName`. History also retains top-level aggregate `nbVerifiedVotes`, `nbRejectedVotes`, reason `nbVotes` and adds `voteCounts`.
- Generic IDs are unique per review; reason slugs are unique per criterion. Two criteria may reuse a slug with different stored text. Built-in families expand into subchecks, and repeated families require explicit IDs.
- `MAX_IMAGE_UPLOAD_SIZE` is 15 × 1024 × 1024 bytes. Both filename extension and decoded JPEG/PNG/GIF format are checked. Multipart oversize is 413; content/quota/expiry validation is 400. Private URLs last at most 120 seconds and cannot outlast expiry.
- Default upload expiry is one hour; successful creation clears it. Reference checks prevent file deletion. Read/history routes use the session guard without the active-lock guard; upload/create use the active-lock guard, whose inactive-lock error is 400.
- Community delay 900..21600 seconds (default 21600), maxVotes 3..100 or omitted. The helper uses a 0.75 threshold and zero-vote approval. Keyholder assignment stores no deadline/quorum; no eligible keyholder is 409. Suspended wearer is 403. Foreign files are 404; bad attachment credentials are 403.
- The creator stores the review before notification and retention, so a failed POST can be ambiguous. Search has no request-correlation guarantee.
- Completion claims/stores the verdict before sequential rejection actions and event emission. Failure can prevent enqueue after partial actions. Bulk lock-end closure has no callback/actions; queued transport does not recheck session liveness. Transport has five attempts, 10-second timeout and exponential backoff starting at 60 seconds; `requestId` is regenerated each attempt.
- Manifest example uses delivered `availableModes: ["unlimited"]`, not lock-creation mode names. The kind declaration is the same array in portal updates and SDK manifests.

## Verification results

Implementation checks and the build/navigation evidence are recorded below as completed. Evidence is reusable only while the relevant public MDX, sidebar, package/config inputs and pinned upstream contracts remain unchanged; evidence/task-only edits do not invalidate the built pages.

- `npm run lint:docs`: passed. Existing title-case warnings remain in untouched Findom, reference, changelog, pillory, guidelines, OAuth and install pages. Targeted lint on the two new pages and webhook page passed without warnings.
- `node "$PAPERCLIP_RUN_SCRATCH_DIR/verify-examples.cjs"`: passed. Parsed all nine JSON fences, compiled literal `satisfies` checks against the exact generated SDK API/webhook interface dependency closure using TypeScript strict/noEmit, and checked six cURL snippets with `bash -n`. The scratch harness also confirmed the three new sidebar IDs resolve to MDX files. The manifest declaration was checked against `defineManifest` and generated extension-mode values.
- Formatter: this repository has no formatter script/config; ran the host's Prettier binary with `--write --prose-wrap preserve` on all touched MDX, sidebar JSON and this evidence file. No new dependency was added. A borrowed dependency-directory symlink caused a site-wide `DocItem` context error during static rendering; it was removed and replaced by local `npm ci` dependencies, followed by `npm run clear`. No tracked dependency inputs changed.
- `openspec validate extension-file-and-review-guides --strict`: passed (`skip_specs: true`, no runtime behavior changes).
- `git diff --check`: passed.

- History paging examples use `limit: 1`, matching the single-row page with `hasMore: true`.

### Build and built-page checks

- Final tested commit: `2001caa6021696595958387c22ffde3357910ef1`. Command: `NODE_OPTIONS=--max-old-space-size=3072 flock --verbose /tmp/chaster-recovery-heavy-check.lock timeout --kill-after=30s 10m npm run build`. Passed, generated 66 indexed documents and static pages. No broken-link/Markdown-link warnings or rendering errors; only existing Docusaurus/Browserslist maintenance notices. Lock acquired immediately. The final run started after the paging correction was pushed.
- The initial borrowed dependency-directory run compiled MDX but failed site-wide static rendering with `TypeError: Cannot read properties of undefined (reading 'id')` in `DocItem`, including untouched/home pages. The single repair, local `npm ci` followed by `npm run clear`, resolved it. Both local builds passed; the last one verifies the stable corrected source. No service infrastructure was changed.
- Served the final `build` with `npm run serve -- --host 127.0.0.1 --port 4020`. Playwright loaded all seven touched public routes and checked every article link under `/api/extensions-api/` via local HTTP and generated fragment IDs. All returned 200, all fragments existed, and no browser page errors occurred. Expanded sidebar groups showed both author pages and the native interaction page.
- Browser clicks passed: private files → standalone peer reviews → native Verification Picture request → standalone peer reviews. Native introductory copy explicitly describes the request-only flow. The rendered history examples contain `limit: 1`, not stale `limit: 20` snippets.
- Rendered code-block counts: files 6, peer reviews 9, webhooks 1, native request 1, authentication 2, sessions 1, lock actions 8. All are nonempty. At 1280 × 720, the review page has no horizontal page overflow; code blocks are 703 pixels wide with automatic horizontal scrolling. The file-page accessibility snapshot includes intact multipart commands, bearer/attachment placeholders and response fields, with code-copy/word-wrap controls.
- Closed the browser and stopped the temporary preview with Ctrl-C. Ports 3000/3001 were not used.

| Built route under `/api/extensions-api/`        | Result                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------------- |
| `create-your-extension/files`                   | 200; upload/read/delete examples and error fragment link render            |
| `create-your-extension/peer-verifications`      | 200; declarations, create response, cursor history and verdict link render |
| `create-your-extension/webhooks`                | 200; typed event and delivery-limits anchors resolve                       |
| `interact-with-extensions/verification-picture` | 200; reciprocal standalone links and native-only distinction render        |
| `authentication`                                | 200; backend credentials and new guide links render                        |
| `sessions`                                      | 200; new guide/history links render                                        |
| `create-your-extension/lock-actions`            | 200; rejection-action and callback-limits links render                     |

The final evidence/task-only commit preserves the tested public input trees. A public MDX/sidebar/package/config edit or relevant upstream contract change invalidates this evidence. Live publication was not performed; QA remains none. Normal Simplifier and Reviewer stages, including fresh exact-head CI, remain required.
