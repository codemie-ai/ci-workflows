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

Shared workflows use the `reusable-` prefix and contain the analysis steps.

---

<div align="center">
EPAM AI/Run CodeMie
</div>
