# Reusable Workflow Job Naming

GitHub Actions displays reusable workflow jobs by joining the caller job name and the called job name: `<caller_name> / <called_name>`.

If the reusable workflow already defines a job `name:`, do not add `name:` to the caller job. Otherwise, GitHub duplicates the label and truncates it in the UI (e.g. `C.../ Commit & PR...`).

## Pattern

```yaml
# Good: Caller specifies only the job ID; called workflow provides the display name
jobs:
  commit-lint:
    uses: ./.github/workflows/reusable-commit-lint.yml

# Bad: Setting name on both creates redundant joined labels like "Commit Lint / Commit Lint"
jobs:
  commit-lint:
    name: Commit Lint
    uses: ./.github/workflows/reusable-commit-lint.yml
```
