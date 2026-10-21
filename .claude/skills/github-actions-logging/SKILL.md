---
name: github-actions-logging
description: >-
  Best practices for GitHub Actions workflow commands (log levels), log grouping,
  and job summaries ($GITHUB_STEP_SUMMARY). Use when creating or editing GitHub Actions
  workflows, bash steps in CI/CD pipelines, or reporting build/test/lint results.
---

# GitHub Actions Logging, Groups, and Job Summaries

Standards and copy-paste patterns for writing clean, structured output in GitHub Actions workflows.

## 1. Log Levels (Workflow Commands)

Use GitHub workflow commands instead of plain `echo` when reporting status, warnings, or errors. They create visual annotations in GitHub Checks and PR interfaces.

### Syntax

```bash
# Error: highlights red, creates PR annotation
echo "::error::Validation failed: schema is invalid"

# Warning: highlights yellow, creates PR annotation
echo "::warning::Deprecated configuration detected, update to v2"

# Notice: neutral info callout in GitHub UI
echo "::notice::Using repository configuration: commitlint.config.js"

# Debug: visible only when ACTIONS_STEP_DEBUG is true
echo "::debug::Current payload: $PAYLOAD"
```

### With File and Line Annotations

```bash
echo "::error file=config.json,line=12,col=5::Syntax error"
echo "::warning file=Dockerfile,line=3::Base image tag is floating"
```

---

## 2. Collapsible Log Groups

Wrap verbose command outputs (npm installs, git logs, diffs, build traces) into collapsible blocks to keep job logs readable.

### Syntax

```bash
echo "::group::Installed tool versions"
git --version
node --version
npm --version
echo "::endgroup::"
```

### Pattern for Verbose Commands

```bash
echo "::group::Run linter details"
npx eslint . --format stylish || { echo "::endgroup::"; exit 1; }
echo "::endgroup::"
```

---

## 3. Job Summaries ($GITHUB_STEP_SUMMARY)

`$GITHUB_STEP_SUMMARY` renders GitHub-flavored Markdown directly on the run summary page.
Always append line by line with `>> $GITHUB_STEP_SUMMARY`.

### Standard Summary Pattern

```yaml
- name: Validation summary
  if: always()
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
    JOB_STATUS: ${{ job.status }}
  run: |
    echo "### Validation Results" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "- **PR Title:** \`$PR_TITLE\`" >> $GITHUB_STEP_SUMMARY
    echo "- **Branch:** \`${{ github.head_ref || github.ref_name }}\`" >> $GITHUB_STEP_SUMMARY
    if [ "$JOB_STATUS" = "success" ]; then
      echo "- **Result:** Passed" >> $GITHUB_STEP_SUMMARY
    else
      echo "- **Result:** Failed" >> $GITHUB_STEP_SUMMARY
    fi
```

### Table Summary Pattern

```bash
echo "### Security Scan Summary" >> $GITHUB_STEP_SUMMARY
echo "" >> $GITHUB_STEP_SUMMARY
echo "| Target | Critical | High | Status |" >> $GITHUB_STEP_SUMMARY
echo "|---|---|---|---|" >> $GITHUB_STEP_SUMMARY
echo "| Dockerfile | 0 | 0 | Passed |" >> $GITHUB_STEP_SUMMARY
echo "| Dependencies | 0 | 1 | Warning |" >> $GITHUB_STEP_SUMMARY
```

---

## Security & Best Practices

1. **Avoid Script Injection:** Never interpolate untrusted GitHub context directly inside bash commands. Always pass values via `env:` variables:
   - Correct: `env: PR_TITLE: ${{ github.event.pull_request.title }}` then `echo "$PR_TITLE"`
   - Incorrect: `echo "${{ github.event.pull_request.title }}"`
2. **Always append:** Always use `>> $GITHUB_STEP_SUMMARY` (not `>`), otherwise previous step summaries are overwritten.
3. **Use `if: always()`:** Put summary steps under `if: always()` so reports are generated even when previous steps fail.
