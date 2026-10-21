<!--
PR title must follow Conventional Commits format:
  <type>(<scope>): <description>

Examples:
  ci(workflows): add codeql language matrix
  fix(actions): correct workflow permissions
  docs(readme): update workflow descriptions

Scope is optional. Use a lowercase description.
-->

## Summary

<!-- Briefly describe the change and why it is needed. Link a related issue if applicable. -->

## Changes

<!-- List the key changes, for example:
- Added or updated a reusable workflow
- Changed workflow inputs, permissions, or configuration
- Updated documentation for consuming repositories

Note any breaking changes for callers.
-->

## Validation

<!-- Describe the checks performed and their results. Link workflow runs if available.
If checks were not run, explain why.

Examples:
- Validated workflow syntax
- Tested the reusable workflow through a caller
- Not run: explain the limitation
-->

## Quality Checks

- [ ] PR title and commit messages follow Conventional Commits
- [ ] Workflow changes have been validated, or limitations are documented
- [ ] All `uses: actions/*` references are pinned to a full commit SHA with the corresponding version in an inline comment (e.g. `# v7.1.0`)
- [ ] Breaking changes for consuming repositories are documented, if applicable
- [ ] No secrets or credentials are included
