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
| Pull request | Proposed change, evidence, review, and limitations | Non-authoritative until merged |
| Notion Project Hub | Deep rationale, technology/function intent, alternatives, grant/roadmap context, and synchronized history | Strategy/history only; never runtime proof |

Notion can preserve detailed explanations that would overload the public repository.
GitHub must still contain enough technical information for an external reviewer to
understand, test, and audit the change without access to the private workspace.

## 2. Documentation impact classes

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
- significant changes to user workflows, deployment posture, or operational guarantees.

## 3. Mandatory workflow

### Before editing

1. Read `AGENTS.md`, `docs/REVIEWER_GUIDE.md`, the documentation map, relevant ADRs,
   current status files, and affected code/tests.
2. For `GITHUB_AND_NOTION`, read the related Project Hub record when access exists.
3. Verify the exact `main` baseline and keep research/roadmap claims separate from
   implemented runtime behavior.

### During the change

1. Capture the problem, intended outcome, assumptions, alternatives, and boundaries.
2. Use exact status terms: proposed, implemented, tested, wired, enabled, observed.
3. Update docs in the same branch as the code whenever the technical contract changes.

### Before review

1. Update every affected GitHub surface, which may include:
   - `README.md` and aligned localized README files;
   - `TEST_REPORT.md`;
   - `docs/STATUS.md`;
   - `docs/IMPLEMENTATION_STATUS.md`;
   - `docs/status/implementation-manifest.json`;
   - `docs/DOCUMENTATION_MAP.md`;
   - an ADR, security/privacy document, reviewer guide, quick start, or grant document.
2. Complete the `Documentation synchronization` block in the PR template.
3. For `GITHUB_AND_NOTION`, create or update the Notion record with the required deep
   context and link it by a safe title, internal reference, or public URL.
4. If Notion is unavailable, set the status to `BLOCKED`, keep the PR draft, and do not
   claim full completion.

### After merge

Update the Notion record with:

- merged PR number and merge commit SHA;
- final test/CI evidence and verified checkpoint;
- differences between the plan and delivered implementation;
- remaining limitations and follow-up work;
- grant or roadmap status changes, if any.

## 4. Required Notion record structure

A substantial record should include:

1. **Problem / opportunity**
2. **Why this matters for Crystal**
3. **Intended technology or function**
4. **Selected decision and rationale**
5. **Alternatives rejected or deferred**
6. **Implementation summary**
7. **Truth, Canon, evidence, privacy, and authority boundaries**
8. **Grant/public-scope impact**
9. **Tests, CI, PR, issue, and exact SHA evidence**
10. **Reality status** — proposed / implemented / tested / wired / enabled / observed
11. **Known limitations**
12. **Next actions**

## 5. Public/private boundary

Crystal is public. Never copy private workspace notes, personal information, secrets,
private datasets, or inaccessible Notion content into GitHub. A PR can reference a safe
Notion page title or internal identifier instead of publishing a private URL.

The reverse boundary is different: Notion may link to public GitHub PRs, issues, commits,
ADRs, and reports, and may contain longer rationale that is intentionally omitted from
the compact public documentation.

## 6. Completion rule

```text
verified code and tests
  + public GitHub technical/status documentation
  + aligned capability and grant claims
  + Notion rationale/history when required
  + final PR, SHA, evidence, limitations, and follow-up
= synchronized change
```

A Notion plan is not implementation proof. A merged PR with stale status or public docs
is not complete. A checked box without the corresponding record is not synchronization.
