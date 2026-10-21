# Job Summaries ($GITHUB_STEP_SUMMARY)

`$GITHUB_STEP_SUMMARY` renders GitHub-flavored Markdown directly on the GitHub Actions workflow run summary page.

## Key Rules

1. **Always append (`>>`)**: Never use single `>` redirection, or you will overwrite summaries from previous steps.
2. **Prevent Script Injection**: Do not interpolate untrusted context into inline scripts. Pass variables through `env:`.
3. **Execute reliably**: Use `if: always()` on summary steps so reports render even when earlier steps fail.

## Basic Summary Pattern

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
      echo "- **Result:** :white_check_mark: Passed" >> $GITHUB_STEP_SUMMARY
    else
      echo "- **Result:** :x: Failed" >> $GITHUB_STEP_SUMMARY
    fi
```

## Table Summary Pattern

```yaml
- name: Generate report table
  if: always()
  run: |
    cat <<'EOF' >> $GITHUB_STEP_SUMMARY
    ### Test & Lint Status

    | Check | Status | Details |
    |---|---|---|
    | Commitlint | :white_check_mark: Passed | Conventional commits verified |
    | Linter | :white_check_mark: Passed | 0 errors, 0 warnings |
    | Unit Tests | :x: Failed | 2 failed out of 45 |
    EOF
```

## Collapsible Details in Summaries

Use HTML `<details>` and `<summary>` tags for long reports or logs:

```yaml
- name: Add debug output to summary
  if: always()
  run: |
    cat <<'EOF' >> $GITHUB_STEP_SUMMARY
    <details>
    <summary>Click to view raw test logs</summary>

    ```text
    ... full verbose test output ...
    ```

    </details>
    EOF
```
