---
name: github-actions
description: Use when creating, modifying, reviewing, or debugging GitHub Actions workflows, composite actions, CI/CD pipeline steps, action pinning, logging, or step summaries.
---

Deliver robust, secure, and observable GitHub Actions workflows, composite actions, and CI/CD steps. Prioritize immutable pinned actions, script injection prevention, structured workflow command logs, and clean job summaries.

## Route by operation

Read only the reference required for the task:

| Task | Reference |
|---|---|
| Pin third-party and official actions by full commit SHA with version tag comment (`uses: actions/...@hash # tag`) | `references/action-pinning.md` |
| Prevent script injection; safely pass untrusted GitHub context via environment variables (`env:`) | `references/script-injection.md` |
| Emit workflow annotations (`::error::`, `::warning::`, `::notice::`, `::debug::`); attach file and line numbers; group verbose logs into collapsible sections (`::group::`) | `references/logging.md` |
| Generate Markdown reports on the workflow run page using `$GITHUB_STEP_SUMMARY`; format status tables, checklists, and collapsible `<details>` blocks | `references/step-summary.md` |
