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
| `reusable-knip.yml` | Shared Knip analysis for finding unused files, dependencies, and exports, called via `workflow_call` |
| `reusable-secrets-detection.yml` | Shared Gitleaks secrets detection with full-history checkout, called via `workflow_call` |

Shared workflows use the `reusable-` prefix and contain the analysis steps.

## Composite Actions

| Action | Description |
|---|---|
| `.github/actions/publish-pypi` | Downloads a distribution artifact and publishes it to PyPI with Trusted Publishing |

Composite actions run as steps inside the caller's job.

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
    name: Security
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
Checkout always fetches full history (`fetch-depth: 0`); callers must not pass
a `fetch-depth` input.

### Knip Check

```yaml
jobs:
  knip:
    name: Knip
    if: github.event_name == 'pull_request'
    permissions:
      contents: read
    uses: codemie-ai/ci-workflows/.github/workflows/reusable-knip.yml@<COMMIT_SHA>
    with:
      working-directory: sdk/codemie-nodejs # optional, defaults to '.'
      node-version: '20'                    # optional, defaults to '20'
```

The workflow installs dependencies and runs the Knip check:
- Runs `npm ci` with npm cache enabled (requires `package-lock.json` in the working directory).
- Runs `npm run knip:check`.
- Execution timeout can be configured via `timeout-minutes` (defaults to 10).

### PyPI Publish (API token)

```yaml
jobs:
  publish:
    name: Publish to PyPI
    needs: build
    permissions:
      contents: read
      id-token: write
    uses: codemie-ai/ci-workflows/.github/workflows/reusable-publish-pypi.yml@<COMMIT_SHA>
    secrets:
      PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
    with:
      artifact-name: python-dist
      packages-dir: dist/ # optional, defaults to 'dist/'
```

The publish job runs in the `release` environment (input `environment`).
A reusable workflow only sees secrets the caller passes, even when the secret
exists only in that environment, so the caller must pass `PYPI_API_TOKEN`.
The secret is required: a caller that does not pass it fails at startup.
The workflow publishes with the token only and has no Trusted Publishing
fallback. PyPI rejects Trusted Publishing from reusable workflows, so use the
`publish-pypi` action below for Trusted Publishing.

### PyPI Publish (Trusted Publishing)

```yaml
jobs:
  publish:
    name: Publish to PyPI
    needs: build
    runs-on: ubuntu-latest
    environment: release
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: codemie-ai/ci-workflows/.github/actions/publish-pypi@<COMMIT_SHA>
        with:
          artifact-name: python-dist
          packages-dir: dist/ # optional, defaults to 'dist/'
```

PyPI does not accept reusable workflows as Trusted Publishers: the OIDC token
of a reusable workflow names `ci-workflows` in `job_workflow_ref`, and PyPI
rejects it with `invalid-publisher`. This action runs inside the caller's job,
so the token names the caller's workflow file.
- Register a Trusted Publisher on PyPI for each project with the caller's
  repository, workflow file name (for example `publish.yml`) and environment
  (for example `release`).
- The calling job must set `environment` and `id-token: write`.
- The build job must upload the distributions as an artifact named
  `artifact-name`.

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
