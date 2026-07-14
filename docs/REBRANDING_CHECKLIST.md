# Repository Rebranding Checklist

> Target public name: **Velantrim Verifiable Memory**
>
> Kernel codename: **Crystal**
>
> Research vision: **Velantrim ExoCortex**
>
> This checklist is operational guidance. It does not rename the repository or package by itself.

## 1. GitHub repository settings — manual owner action

Change the repository name in:

```text
Repository → Settings → General → Repository name
```

Recommended slug:

```text
velantrim-verifiable-memory
```

Recommended GitHub description:

```text
Local-first, verifiable memory and provenance infrastructure for long-running AI agents.
```

Recommended topics:

```text
ai-memory
agent-memory
verifiable-ai
provenance
knowledge-graph
local-first
trustworthy-ai
gdpr
ai-agents
open-source
```

Do not create a new repository under the old slug after the rename, because that may interfere with GitHub redirects from the old URL.

## 2. Public naming hierarchy

Use the following consistently:

```text
Velantrim Verifiable Memory — current public product
Crystal — current memory-kernel codename
Velantrim ExoCortex — long-term research vision
```

Canonical wording is defined in [`PROJECT_IDENTITY.md`](./PROJECT_IDENTITY.md).

The research boundary is defined in [`EXOCORTEX_VISION.md`](./EXOCORTEX_VISION.md).

## 3. README update

Recommended opening:

```markdown
# 🔱 Velantrim Verifiable Memory

### *Verifiable long-term memory and provenance infrastructure for AI agents*

> **Crystal** is the codename of the current memory kernel.
> **Velantrim ExoCortex** is the broader long-term research vision, not a claim
> about the current runtime.
```

Preserve current implementation claims, test baselines and reviewer links. Do not replace technical detail with branding-only language.

## 4. Package and CLI compatibility

Do not automatically rename these identifiers during the public repository rename:

```text
Python distribution: velantrim-exocortex-crystal
CLI: velantrim
CLI: velantrim-api
CLI: velantrim-mcp
environment variables: VELANTRIM_*
Python imports: core.*
database schemas and migration identifiers
```

A package rename should be a separate compatibility decision with:

- a deprecation period;
- upgrade instructions;
- package-index availability check;
- import and CLI compatibility tests;
- release notes;
- rollback plan.

## 5. Repository URLs

After the manual GitHub rename, update repository-owned URLs in a separate PR:

- `README.md` clone commands;
- `pyproject.toml` project URLs;
- badges;
- Docker and release documentation;
- issue templates;
- security-policy links;
- GitHub Pages configuration;
- workflow references;
- external documentation.

Local clones should update `origin`:

```bash
git remote set-url origin https://github.com/velantrian/velantrim-verifiable-memory.git
```

## 6. External references

Update only after the new repository URL is active:

- Reddit posts and profile links;
- Notion project hub;
- grant applications and follow-up correspondence;
- OpenAI, Hub71 and other programme profiles;
- personal GitHub profile README;
- community and contributor documentation;
- demo pages;
- media and outreach materials.

Where an application has already been submitted, preserve the historical submitted name and add the new name as an alias rather than silently rewriting the record.

Recommended transition wording:

> Formerly published as Velantrim ExoCortex — Crystal. The project is now presented as Velantrim Verifiable Memory; Crystal remains the kernel codename and ExoCortex remains the long-term research vision.

## 7. Search and audit before merge

Search for naming references:

```bash
rg -n "Velantrim ExoCortex|Velantrim Crystal|Exo-Cortex Crystal|velantrim-exocortex-crystal" .
```

Classify every match:

- update now — public branding;
- preserve — historical record or technical compatibility identifier;
- research-only — ExoCortex vision;
- package compatibility — separate migration;
- external URL — update after manual repository rename.

Do not perform a blind global replacement.

## 8. CI and validation

A documentation-only branding PR should still verify:

```text
Markdown links resolve
README anchors remain valid
no implementation-status claim changes
no test-count drift introduced
no package or import identifiers changed accidentally
no repository URL changed before the manual rename
```

If executable files or package metadata are changed later, run the full CI suite.

## 9. Release communication

Recommended announcement structure:

1. The engineering purpose is now explicit.
2. Crystal remains the memory-kernel codename.
3. ExoCortex remains the broader research vision.
4. Runtime behaviour and licensing are unchanged by the branding update.
5. Existing links should redirect after GitHub rename, but users should update local remotes.

## 10. Completion criteria

The rebranding is complete when:

```text
[ ] Repository slug changed manually
[ ] GitHub description and topics updated
[ ] README public heading updated
[ ] Current product / codename / research vision are clearly separated
[ ] Repository-owned URLs updated after rename
[ ] Package compatibility decision recorded
[ ] External profiles updated
[ ] CI and link checks green
[ ] No research capability is presented as implemented runtime
```

## Non-goal

This rebranding does not change the technical architecture, grant scope, runtime guarantees, licence, test baseline or implementation maturity. It changes how the existing work is explained to new readers.