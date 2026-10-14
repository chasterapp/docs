# Design

## Context

See `proposal.md` for the reader's goal. This repository uses Docusaurus 3, MDX frontmatter, root-relative links and a shell-based documentation tone checker. It has no repository `AGENTS.md`, `DESIGN.md`, reference guides, local OpenSpec skills or existing capability specs. The existing docs-only OpenSpec change establishes the `skip_specs: true` pattern. The Chaster OpenSpec propose procedure supplies the artifact workflow.

The docs baseline is `4497e7f`. On 2026-10-14, the verified Chaster main revision was `c90d76aeedcdab65d6411a3f630c9d1e37ab41fd`. [PR #892](https://github.com/chasterapp/chaster/pull/892) merged at 13:14:20 UTC as `90a4748b3135dd8d4eec207f603efc192b33e844`.

Source references at that main revision:

- [PartnerMainAuthorizationService](https://github.com/chasterapp/chaster/blob/c90d76aeedcdab65d6411a3f630c9d1e37ab41fd/server/src/modules/partner-authorization/services/partner-main-authorization.service.ts): read the complete service, especially `createSessionAuth`.
- [PartnerExtensionService](https://github.com/chasterapp/chaster/blob/c90d76aeedcdab65d6411a3f630c9d1e37ab41fd/server/src/modules/partner-extension/services/partner-extension.service.ts): its `HomeActionPlugin` reads `extension.metadata.homeActions`.
- [Extension session controller hook](https://github.com/chasterapp/chaster/blob/c90d76aeedcdab65d6411a3f630c9d1e37ab41fd/web/src/modules/extensions/business/usePartnerExtensionSessionController.ts): reads Chaster's `action` query parameter and passes it to session authorization.
- [Merged main-page hash requirements](https://github.com/chasterapp/chaster/blob/c90d76aeedcdab65d6411a3f630c9d1e37ab41fd/openspec/changes/pass-home-action-slug-to-extension-iframe/specs/partner-extension-main-page-auth/spec.md): covers declared, missing, unknown and URL-significant slugs.

## Goals / non-goals

**Goals:** A partner can decode the whole hash, identify the clicked action and show a default view when the action field is missing. All three pages describe the same delivered contract.

**Non-goals:** Change session authorization, introduce a partner query parameter, add an SDK helper or prescribe a routing framework. No data model, API schema, locale, analytics or application UI changes.

## Decisions

### Explain the hash fields together

Keep the existing "Parse the main page token" heading and its anchor. Describe the hash as `encodeURIComponent(JSON.stringify(params))`, parsed with `JSON.parse(decodeURIComponent(window.location.hash.substring(1)))`. Use a compact field table:

| Field | Presence and meaning |
| --- | --- |
| `mainToken` | Always included; identifies the current main-page authorization and continues to be passed to the partner backend. |
| `extensionSlug` | Always included; the partner extension's slug, already sent before this change. |
| `homeActionSlug` | Optional; the clicked home action's slug, included only when it exactly equals a current declared home action for this session. |

The serialized property order is `mainToken`, `extensionSlug`, then `homeActionSlug` when present. When there is no clicked action or the supplied slug does not match, the last key is absent, not `null`. Decoding therefore gives `undefined` for `params.homeActionSlug` in those cases. The extension still opens normally.

Update the encoded iframe URL example using synthetic `arandomtoken`, `smart-lock-opener` and `action_slug` values, and show the corresponding decoded JSON to make the long encoded URL understandable. Generate the encoded fragment from that exact JSON instead of editing percent escapes by hand. Also show the decoded ordinary-open payload with only the first two fields. This directly explains omission without adding a second long encoded URL.

Extend the existing JavaScript example to read all three fields and demonstrate selecting the action view or a default view when `homeActionSlug` is missing. Use a small explicit branch or switch for the example's declared action; a default branch can also handle a value the partner no longer recognizes. Explain that view selection belongs in the partner's app. Keep the snippet valid standalone JavaScript without requiring unprovided framework helpers.

The slug is navigation context, not proof of permission to perform an operation. Preserve the existing backend-only API calls and `mainToken` authentication guidance. Chaster's internal `?action=` route is not the partner iframe interface; the partner reads its hash.

### Connect metadata declarations to the main page

In "Home actions", name `homeActionSlug` in the `slug` description and add a short explanation that one main page can choose its view based on the clicked action. Link to `/api/extensions-api/create-your-extension/main-page#parse-the-main-page-token`. State that the forwarded value must match the session's declared `homeActions`; direct opens and unknown slugs omit the field.

Do not change unrelated metadata endpoint prose or examples. Existing sidebar entries already cover both pages.

### Announce only the newly added field

Add a dated changelog entry explaining optional `homeActionSlug`, its relation to the clicked declared home action, and the default behavior when absent. Link to the parsing section and Home actions section. Do not label `extensionSlug` as newly introduced.

If the production release date is not yet known, the draft may use the preparation date provisionally. Before merge, set the entry's date to the verified production release date. Do not invent release inclusion from the merge time or from a changelog heading.

## Risks / trade-offs

- Contract drift: the Applier refreshes main and records its exact revision and field cross-check in `verification.md`. The pinned source above is proposal evidence, not a substitute for a fresh check.
- Misleading optionality: verify declared action, missing action and unknown action payloads, including absence rather than `null`. Also check that decode preserves a slug with URL-significant characters.
- Example encoding errors: run the documented JavaScript against the encoded example and ordinary-open payload, asserting field values and the chosen fallback view. A one-off Node check is sufficient; no new testing dependency is needed.
- MDX or link failures: run the issue's required `npm run lint:docs` and `npm run build` after the three pages change, inspect introduced warnings and check rendered code blocks and anchor links.
- Shared-host contention: checkpoint and push before building; announce that the host lock may wait. Run only the docs build under `flock --verbose /tmp/chaster-recovery-heavy-check.lock`, with a 3 GiB heap cap and a bounded timeout. No Chaster server, frontend or test-suite run is needed.

## Migration plan

No runtime migration or deployment is part of this issue. Implement and review the docs on the same issue branch and draft PR.

The Reviewer must verify a completed Chaster production release whose deployed revision contains `90a4748b3135dd8d4eec207f603efc192b33e844`, and record the release/deployment reference, deployed revision and commit-inclusion evidence before merging. A merged PR, main branch revision, preview image or preproduction release does not prove this condition.

Production release inclusion was not established during proposal work. If it remains unverified after review, the Reviewer routes the release-evidence dependency to the Founding Engineer using the normal issue waiting procedure. Implementation and review do not need to wait for that evidence. Reverting the docs has no runtime or stored-data effect.
