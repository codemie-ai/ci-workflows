# Pinning Actions to Commit SHA

Always pin third-party and official GitHub Actions to a full 40-character commit SHA with a version tag comment.

## Pattern

```yaml
# Good: Pinned by full SHA with version tag comment
- name: Checkout repository
  uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

- name: Setup Node.js
  uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af # v4.1.0
  with:
    node-version: 20

# Bad: Using mutable tags or branch names
- uses: actions/checkout@v4
- uses: actions/checkout@main
```
