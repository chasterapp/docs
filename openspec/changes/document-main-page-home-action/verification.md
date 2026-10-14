# Implementation verification

## Contract checked on 2026-10-14

`git ls-remote https://github.com/chasterapp/chaster.git refs/heads/main` returned `c90d76aeedcdab65d6411a3f630c9d1e37ab41fd`, unchanged from the proposal. Read the full authorization service and the related metadata plugin, navigation hook and merged requirements with `git show <revision>:<path>` from the existing Chaster clone. No shared checkout or service was changed. The issue workspace preflight passed, the branch was already up to date, and GitHub App metadata access to docs PR #20 passed.

| Contract             | Source and finding                                                                                                                                                                                                           |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `mainToken`          | `createSessionAuth` creates the authorization token and always puts it first in `params`. Existing backend-only API and token authentication guidance remains unchanged.                                                     |
| `extensionSlug`      | Always second, from `partnerPlugin.partnerExtension.slug`; an existing field, not announced as new.                                                                                                                          |
| `homeActionSlug`     | Conditional third field via object spread. `homeActions.some(action => action.slug === homeActionSlug)` requires an exact match. Missing or unknown action omits the property; it is not null and does not fail the request. |
| Session declarations | `PartnerExtensionService` registers `HomeActionPlugin` with `() => extension.metadata.homeActions`.                                                                                                                          |
| Navigation           | `usePartnerExtensionSessionController` reads Chaster's `action` query parameter and passes it to session authorization. Partners read the iframe hash.                                                                       |
| Encoding             | `createSessionAuth` appends `#${encodeURIComponent(JSON.stringify(params))}` to the main iframe URL. The merged requirements cover declared, missing, unknown and URL-significant slugs.                                     |

Source paths and pinned GitHub links are in `design.md`. The public text was checked against those findings. The action slug selects a view and does not authorize operations. Feature switch: none. Sensitive surfaces: public developer content and an authentication-related API contract.

## Release condition

Production release inclusion is not established. The changelog heading `2026-10-14` is the provisional preparation date, not release evidence. Before merge, the Reviewer must record a completed Chaster production release/deployment reference, its deployed revision and proof that it contains `90a4748b3135dd8d4eec207f603efc192b33e844`, then finalize the changelog date. Main branch and PR merge status do not establish production deployment. Implementation and review may continue.

## Checks

- Local dependencies installed with `npm ci --ignore-scripts --no-audit --no-fund`; no dependency files changed.
- No repository formatter script/config exists. Ran the host's Prettier binary with `--write --prose-wrap preserve` on the three edited MDX pages. Preserved original sections outside the requested edits, including the existing admonition delimiter that Prettier indented as a list continuation.
- Targeted `bash .claude/hooks/lint-docs.sh <path>` passed for each of the three pages. Only the changelog's pre-existing launch heading warns about title case.
- `node "$PAPERCLIP_RUN_SCRATCH_DIR/verify-examples.cjs"` passed. The one-off harness extracts and executes the actual documented JS with synthetic `window.location.hash`, checks the encoded URL against the displayed JSON, and asserts exact field values, property order, missing key and `undefined`, action/default view selection and round-trip encoding. Cases: clicked declared action, ordinary open, unknown request's omitted-key payload, and declared `tasks#&" /?=é`. The last value decodes intact and selects the example's default view because its switch only recognizes `action_slug`. Server matching/omission was verified from source, not by reimplementing it in this check.
- `npm run lint:docs`: passed with 15 existing title-case warnings and zero errors. No new heading warnings.
- `openspec validate document-main-page-home-action --strict`: passed with the expected docs-only `skip_specs` notice.
- `git diff --check`: passed.
- Required docs build and built-page inspection pending at this checkpoint.

Build evidence is reusable while the three public page inputs, package lock, site configuration and relevant source contract stay unchanged. Evidence/task-only edits do not invalidate the built pages.
