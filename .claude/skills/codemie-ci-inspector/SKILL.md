---
name: codemie-ci-inspector
description: Use when auditing GitHub Actions workflows in codemie-ai repositories, checking if repositories use centralized shared workflows (CodeQL, Gitleaks) from ci-workflows, or updating the repository catalog file.
---

# CodeMie CI Inspector

Audits repositories under `codemie-ai` for adherence to organizational CI/CD standards (CodeQL and Gitleaks shared workflows).

## Standards & Patterns

Shared workflows source repo: `codemie-ai/ci-workflows`

- **CodeQL**: `codemie-ai/ci-workflows/.github/workflows/reusable-codeql.yml@main`
- **Gitleaks**: `codemie-ai/ci-workflows/.github/workflows/reusable-secrets-detection.yml@main`

---

## Step 1: Refresh Repository Catalog

When the user asks to update or refresh the repository list:

Dispatch a subagent via `task` (`subagent_type: "general"`) to run:
```bash
python3 .claude/skills/codemie-ci-inspector/scripts/fetch_repos.py
```
This updates `.claude/skills/codemie-ci-inspector/references/repositories.json` for branch `main` and excludes repos from `references/excluded_repositories.json`.

---

## Step 2: Audit Workflows via Subagent

Always execute workflow audits inside a subagent (`task` tool with `subagent_type: "general"`) to avoid polluting the main context.

### Sub-steps for Audit:

#### 2.1. Check CodeQL
Run `check_codeql.py`:
```bash
# For a single repository:
python3 .claude/skills/codemie-ci-inspector/scripts/check_codeql.py <repo-name>
# Output: true / false

# For all repositories:
python3 .claude/skills/codemie-ci-inspector/scripts/check_codeql.py
# Output: JSON mapping repo -> true/false
```

#### 2.2. Check Gitleaks
Run `check_gitleaks.py`:
```bash
# For a single repository:
python3 .claude/skills/codemie-ci-inspector/scripts/check_gitleaks.py <repo-name>
# Output: true / false

# For all repositories:
python3 .claude/skills/codemie-ci-inspector/scripts/check_gitleaks.py
# Output: JSON mapping repo -> true/false
```

#### 2.3. Output Results

- **If a single repository was audited**:
  Return direct `true`/`false` answers using ASCII indicators:
  - CodeQL (shared): `[✓] true` or `[ ] false`
  - Gitleaks (shared): `[✓] true` or `[ ] false`

- **If all repositories were audited**:
  Return a clean summary table using ASCII indicators (`[✓] true` / `[ ] false`):

| Repository | GitHub Workflows | CodeQL (Shared) | Gitleaks (Shared) |
|---|---|---|---|
| `docs` | Yes | `[✓] true` | `[ ] false` |
| `ci-workflows` | Yes | `[✓] true` | `[ ] false` |
| `codemie-code` | Yes | `[ ] false` | `[ ] false` |
