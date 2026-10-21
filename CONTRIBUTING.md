# Contributing

Contributions are welcome. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before you start.

This repository contains reusable GitHub Actions workflows, composite actions, and automation standards shared across CodeMie projects.

## How to Contribute

1. Fork the repository on GitHub.
2. Clone your fork and create a branch: `git checkout -b my-feature-branch`.
3. Make your change and add or update workflows.
4. Verify your workflow syntax and configuration.
5. Push the branch to your fork and open a pull request against `main`.

## Pull Requests

- PR titles and commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<optional scope>): <description>`, for example `ci: add reusable workflow` or `docs: update contributing guide`.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `revert`, `ci`.
- Keep a PR focused on one change. Describe what changed and why.

## Review Rule

Every PR needs one approval from any collaborator with write access before it can be merged. All CI checks must pass.

## Workflow Testing

- Ensure GitHub Actions workflow syntax is valid.
- Test workflows locally using tools such as [act](https://github.com/nektos/act) or in a personal fork before submitting.
- Validate commit messages against conventional commits configuration (`commitlint.config.js`).

## Internal References and Secrets

CI scans the tree for internal references and for secrets. Do not commit credentials, private hostnames, ticket keys, or personal e-mail addresses. Use placeholders such as `https://your-codemie-host.example.com` in examples and tests.

## Reporting Issues

Use GitHub Issues for bugs and feature requests. For security concerns, report them privately via GitHub Security Advisories under the **Security** tab.
