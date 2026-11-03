# Comments in workflows and actions

Comments in YAML are for a human who scans the file. Keep them short.

## Rules

- One line, at most two. Say what the constraint is, not the whole story.
- If the reason is non-obvious, add a link to the source (docs, issue, README section) instead of explaining it.
- Do not repeat what the code already says (`# Checkout the repo` above `actions/checkout`).
- Do not describe the history of the change or the debugging path. That belongs in the commit message or PR.
- Long rationale belongs in the README of the repository that owns the workflow, not in the caller's YAML.
- The `# vX.Y.Z` tag after a pinned SHA is required and is not a comment to remove.

## Example

Bad:

```yaml
# Call the PyPI action directly. It builds a Docker image from github.action_repository, so it breaks
# when it is invoked from another composite action: the image is looked up in ci-workflows, not in pypa.
- uses: pypa/gh-action-pypi-publish@<SHA> # v1.14.3
```

Good:

```yaml
# Call directly, do not wrap in a composite action: https://github.com/codemie-ai/ci-workflows#pypi-publish-trusted-publishing
- uses: pypa/gh-action-pypi-publish@<SHA> # v1.14.3
```
