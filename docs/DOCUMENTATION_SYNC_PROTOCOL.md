# 🔄 Code ↔ Documentation ↔ Notion Sync Protocol

This protocol makes documentation synchronization part of the definition of done for
Velantrim Exo-Cortex Crystal. A change is not complete when the code, public technical
documentation, grant/status material, and project history describe different realities.

## 1. Separation of responsibilities

| Surface | Purpose | Authority |
|---|---|---|
| GitHub `main` code and tests | Executable implementation truth | Highest for implemented behavior |
| `TEST_REPORT.md` and implementation manifest | Verified test/status evidence | Derived from current repository evidence |
| `docs/STATUS.md`, `docs/IMPLEMENTATION_STATUS.md`, ADRs | Current technical contract and decisions | Must match verified `main` |
| README and reviewer documents | Public capability, usage, and safety contract | Must not overstate implementation |
| `docs/ai/*` | Compact current state, component map, risk register, audit method and hand-off | GitHub-native continuity for humans and AI agents |
| Pull request | Proposed change, evidence, review, and limitations | Non-authoritative until merged |
| Notion Project Hub | Deep rationale, technology/function intent, alternatives, grant/roadmap context, and synchronized history | Strategy/history only; never runtime proof |

Notion can preserve detailed explanations that would overload the public repository.
GitHub must still contain enough technical and audit information for an external reviewer
or connectorless AI agent to understand, test, continue, and challenge the work without
access to the private workspace.

## 2. GitHub completeness invariant

Not every AI system has direct Notion access. Therefore:

```text
implemented contract + material audit finding + known risk + exact evidence + next action
must be understandable from GitHub alone.
```

No implementation boundary, safety rule, unresolved engineering risk, decision needed to
continue the work, or proof required for review may exist only in Notion.

This does not require copying every sentence twice. Synchronize the decision-bearing
facts:

- problem and intended outcome;
- selected decision and material alternatives;
- implementation/reality status;
- authority, truth, privacy and safety boundaries;
- exact PR/SHA/test/CI evidence;
- known limitations and required next actions.

Notion remains the richer rationale and historical layer. GitHub remains the complete
public technical and audit layer.

## 3. Documentation impact classes

Every PR must choose one class.

### `NONE`

Only for a change with no effect on behavior, public commands, capability claims,
architecture, risk, grant scope, status, or project intent. A reason is required.

### `GITHUB_ONLY`

Use for a focused technical change whose rationale is adequately captured in the PR and
repository documentation. Examples include a narrow bug fix, corrected status marker,
updated command, test-only proof, or clarified failure mode.

### `GITHUB_AND_NOTION`

Required for:

- a new technology, function, module, adapter, interface, or major capability;
- architecture, TruthGate, Canon, evidence, privacy, security, or authority changes;
- a durable decision with meaningful alternatives or trade-offs;
- changes to grant work packages, roadmap, demonstrators, positioning, or public scope;
- cross-project boundaries involving Titan, Research Mode, or external labs;
- implementation, rejection, replacement, or deferral of a previously documented plan;
- significant changes to user workflows, deployment posture, or operational guarantees;
- a material audit that changes current state, risk, architecture, roadmap, or an
  engineering decision.

## 4. Notion access states

| Status | Meaning |
|---|---|
| `NOT_REQUIRED` | The work is `NONE` or `GITHUB_ONLY` |
| `NOTION_AVAILABLE` | The current actor can read and update the relevant Notion record |
| `HANDOFF_REQUIRED` | The current actor lacks Notion access; a complete GitHub hand-off is required |
| `SYNCED` | A connected actor updated Notion and recorded the safe reference/evidence |
| `BLOCKED_PRIVACY_OR_PERMISSION` | Synchronization cannot be completed safely or the required target/permission is unresolved |

A missing connector is normally `HANDOFF_REQUIRED`, not a reason to abandon the analysis
or hide its findings.

## 5. Mandatory workflow

### Before editing or auditing

1. Read `AGENTS.md`, `docs/ai/README.md`, current state, known risks, the reviewer guide,
   documentation map, relevant ADRs, status files, and affected code/tests.
2. For `GITHUB_AND_NOTION`, read the related Project Hub record when access exists.
3. When Notion access does not exist, inspect
   `docs/ai/NOTION_HANDOFF.md` for pending items and continue from GitHub evidence.
4. Verify the exact `main` baseline and keep research/roadmap claims separate from
   implemented runtime behavior.

### During the work

1. Capture the problem, intended outcome, assumptions, alternatives, and boundaries.
2. Use exact status terms: proposed, implemented, tested, wired, enabled, observed.
3. Update docs in the same branch as the code whenever the technical contract changes.
4. Record material analysis in GitHub even when it does not immediately change runtime:
   current state, component map, risks, work log, ADR/RFC, or another appropriate public
   surface.

### Before review — Notion available

1. Update every affected GitHub surface, which may include:
   - `README.md` and affected English technical/status documents;
   - localized README files only in a dedicated localization PR;
   - `TEST_REPORT.md`;
   - `docs/STATUS.md`;
   - `docs/IMPLEMENTATION_STATUS.md`;
   - `docs/status/implementation-manifest.json`;
   - `docs/DOCUMENTATION_MAP.md`;
   - `docs/ai/CURRENT_STATE.md`;
   - `docs/ai/COMPONENT_MAP.md`;
   - `docs/ai/KNOWN_RISKS.md`;
   - `docs/ai/WORK_LOG.md`;
   - an ADR, security/privacy document, reviewer guide, quick start, or grant document.
2. Complete the `Documentation synchronization` block in the PR template.
3. Create or update the Notion record with the required deep context.
4. Record a safe page title, internal reference, or public URL in the PR.
5. Set synchronization to `SYNCED` before a `GITHUB_AND_NOTION` implementation PR is
   marked ready for review.

### Before review — Notion unavailable

1. Do not stop a valid audit or implementation solely because the connector is missing.
2. Complete all required public GitHub documentation and evidence.
3. Add a structured item to
   [`docs/ai/NOTION_HANDOFF.md`](./ai/NOTION_HANDOFF.md) containing the problem,
   findings, decision, alternatives, boundaries, changed files, exact SHA/CI evidence,
   limitations, intended Notion record title, and next actions.
4. Set PR fields to:
   - `Notion access: UNAVAILABLE`;
   - `Notion synchronization: HANDOFF_REQUIRED`;
   - `GitHub hand-off: docs/ai/NOTION_HANDOFF.md#...`.
5. Do not claim that Notion was updated.
6. Keep a `GITHUB_AND_NOTION` implementation PR draft until a connected actor completes
   synchronization. Analysis-only findings may remain in the queue without blocking
   unrelated engineering, but the hand-off must remain visible.

Use `BLOCKED_PRIVACY_OR_PERMISSION` only when the structured hand-off itself cannot be
completed safely, the target record cannot be identified, or required access is denied.

### Connected actor completion

A human or AI agent with Notion access must:

1. verify the GitHub hand-off against the current PR, SHA, tests and repository state;
2. create or update the relevant Notion page;
3. add the safe Notion reference to the PR and hand-off item;
4. change `HANDOFF_REQUIRED` to `SYNCED`;
5. preserve the public/private boundary;
6. after merge, add final merge SHA, CI evidence, deviations, limitations and next
   actions to Notion.

### After merge

Update the Notion record with:

- merged PR number and merge commit SHA;
- final test/CI evidence and verified checkpoint;
- differences between the plan and delivered implementation;
- remaining limitations and follow-up work;
- grant or roadmap status changes, if any.

Also close or mark the corresponding GitHub hand-off item `SYNCED` so agents without
Notion can see that synchronization was completed.

## 6. Required Notion record structure

A substantial record should include:

1. **Problem / opportunity**
2. **Why this matters for Crystal**
3. **Intended technology or function**
4. **Selected decision and rationale**
5. **Alternatives rejected or deferred**
6. **Implementation or audit summary**
7. **Truth, Canon, evidence, privacy, and authority boundaries**
8. **Grant/public-scope impact**
9. **Tests, CI, PR, issue, and exact SHA evidence**
10. **Reality status** — proposed / implemented / tested / wired / enabled / observed
11. **Known limitations**
12. **Next actions**

The GitHub hand-off uses the same decision-bearing structure so a connected actor can
synchronize Notion without reconstructing the analysis from scratch.

## 7. Public/private boundary

Crystal is public. Never copy private workspace notes, personal information, secrets,
private datasets, or inaccessible Notion content into GitHub. A PR can reference a safe
Notion page title or internal identifier instead of publishing a private URL.

The reverse boundary is different: Notion may link to public GitHub PRs, issues, commits,
ADRs, reports, AI work-log entries and hand-off records, and may contain longer rationale
that is intentionally omitted from compact public documentation.

## 8. Completion rule

```text
verified code and tests
  + complete public GitHub technical/audit documentation
  + aligned capability and grant claims
  + Notion rationale/history when required
  + connectorless hand-off when direct Notion access is absent
  + final PR, SHA, evidence, limitations, and follow-up
= synchronized change
```

A Notion plan is not implementation proof. A merged PR with stale status or public docs
is not complete. A connectorless analysis hidden only in chat is not a durable hand-off.
A checked box without the corresponding record is not synchronization.

## 9. Active language and localization policy

English is the authoritative actively maintained GitHub documentation language while
Crystal engineering remains in motion.

Existing translated top-level README files are retained as frozen snapshots. They may lag
mutable test counts, SHAs and capability details. Ordinary runtime, architecture and
status PRs must not update them automatically.

A later dedicated final localization pass must:

1. start from a frozen English verified checkpoint;
2. update every supported language coherently;
3. preserve stable API/code identifiers;
4. run link and claim-boundary checks;
5. record its own exact CI evidence.

The `docs-status` job validates current English authority surfaces and the declared freeze
policy; it does not require stale translations to mirror every mutable checkpoint.
