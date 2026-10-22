<div align="center">

<img src="assets/codemie-logo.svg" alt="CodeMie" width="96" />

# CodeMie CI Workflows

**Reusable GitHub Actions workflows and CI/CD automation pipelines for CodeMie projects.**

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?style=flat-square)](https://conventionalcommits.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)](LICENSE)

</div>

## Overview

This repository contains reusable GitHub Actions workflows, composite actions, and automation standards shared across CodeMie repositories.

## Workflows

| Workflow | Description |
|---|---|
| `reusable-codeql.yml` | Shared CodeQL analysis, called via `workflow_call`; defaults to JavaScript/TypeScript with `build-mode: none` |
| `reusable-commit-lint.yml` | Shared Conventional Commits and PR title validation, called via `workflow_call` |
| `reusable-deploy-pages.yml` | Shared GitHub Pages build and deployment, called via `workflow_call` |
| `reusable-secrets-detection.yml` | Shared Gitleaks secrets detection with full-history checkout, called via `workflow_call` |

Shared workflows use the `reusable-` prefix and contain the analysis steps.

## Composite Actions

| Action | Description |
|---|---|
| `actions/setup-node-project` | Checks out the caller repository, sets up Node.js with npm caching, and installs dependencies |
| `actions/build-site` | Checks out the caller repository, sets up Node.js with npm caching, installs dependencies, and builds the site |

`setup-node-project` accepts `node-version` (default `'24'`), `ref` (default
empty, using the event's checkout ref), `fetch-depth` (default `'1'`; use `'0'`
for full history), and `install-command` (default `npm ci`).
It requires `contents: read` permission and an npm lockfile in the repository
root. Use it before project-specific checks:

```yaml
jobs:
  checks:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Prepare Node.js project
        uses: codemie-ai/ci-workflows/actions/setup-node-project@<COMMIT_SHA>
      - name: Run checks
        run: npm run typecheck
```

For checks of the PR head commit, pass
`ref: ${{ github.event.pull_request.head.sha }}` through the action's `with`.
The action performs checkout itself with `persist-credentials: false`.
Replace `<COMMIT_SHA>` with a commit containing the action.

`build-site` accepts `node-version` (default `'24'`), `install-command`
(default `npm ci`), and `build-command` (default `npm run build`).
It requires `contents: read` permission and an npm lockfile in the repository
root. Build environment variables can be supplied through `env` on the calling
step. Artifact uploads and deployment remain the responsibility of the caller.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Build website
        uses: codemie-ai/ci-workflows/actions/build-site@<COMMIT_SHA>
        with:
          node-version: '24'
      - name: Upload build artifacts
        uses: actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f # v7.0.0
        with:
          name: site-build
          path: ./build
```

Replace `<COMMIT_SHA>` with a commit containing the action before using this
example. The action delegates preparation to `setup-node-project`; callers do
not need a separate checkout or dependency installation step.

`reusable-deploy-pages.yml` uses the remote action reference because checkout in
a called workflow retrieves the caller repository, not `ci-workflows`.
The references from `reusable-deploy-pages.yml` to `build-site` and from
`build-site` to `setup-node-project` temporarily use `@epmcdme-16232-v3` for
testing before merge. Pin each reference to a commit containing its target
before releasing, and update the pins when the shared actions need to change.

## Usage

Add `.github/workflows/codeql.yml` to your repository:

```yaml
name: CodeQL
...
jobs:
  codeql:
    uses: codemie-ai/ci-workflows/.github/workflows/reusable-codeql.yml@dfb48c2949766afc371ab507f4a2da6251b261ea # v1.0.0 (example)
    with:
      language: javascript-typescript
...
```

Replace the example SHA and version comment with those of the release you want to use.
Update the pinned version through a pull request.

### Secrets Detection

```yaml
jobs:
  secrets-detection:
    name: Secrets Detection
    if: github.event_name == 'pull_request'
    permissions:
      contents: read
      pull-requests: read
    uses: codemie-ai/ci-workflows/.github/workflows/reusable-secrets-detection.yml@<COMMIT_SHA>
```

Replace `<COMMIT_SHA>` with a commit containing the workflow.
The optional `runner` input defaults to `ubuntu-latest`. The Gitleaks version
is managed centrally in the shared workflow, and `GITHUB_TOKEN` is available
automatically; `secrets: inherit` is not required.
Keep job dependencies (`needs`) and event conditions in the caller.

## Releasing

1. Merge changes into `main` and confirm CI has passed.
2. Open **Actions → Release → Run workflow**, select **main**, and enter
   a new version such as `v1.0.0`.
3. Run the workflow: it creates the tag and GitHub Release with notes generated
   by git-cliff from Conventional Commits.

Release notes include changes since the previous stable version tag reachable
from the release commit, or the entire history for the first release. Sections
for features, fixes, documentation, dependencies, CI, and other changes are
configured in `cliff.toml`; PR labels are not required. Breaking changes are
marked explicitly. Non-conventional commits (such as merge commits) are omitted,
so preserve the Conventional Commits format when squash-merging PRs.

git-cliff is executed via the `orhun/git-cliff-action` GitHub Action.
Notes show the version and release date, and each change
links to its PR (when available) and commit. GitHub metadata is fetched using the
workflow token; a New Contributors section is included when there are first-time
contributors.

All workflows share one version: patch for fixes, minor for compatible additions,
major for breaking changes. Only stable `vMAJOR.MINOR.PATCH` versions are accepted;
existing tags cannot be reused. The release job runs only on `main` and does not
check CI results itself.

---

<div align="center">
EPAM AI/Run CodeMie
</div>
