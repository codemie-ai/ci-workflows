# Preventing Script Injection

Never interpolate GitHub context directly inside inline scripts (`run:`). Always pass context expressions through `env:` and reference them as shell variables.

## Pattern

```yaml
# Good: Passed safely via environment variable
- name: Process PR title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    echo "Processing: $PR_TITLE"

# Bad: Direct interpolation allows arbitrary command execution
- run: echo "Processing: ${{ github.event.pull_request.title }}"
```
