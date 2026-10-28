# Task: Add reusable-release-version-check.yml to ci-workflows

- **Repository:** `codemie-ai/ci-workflows`
- **Status:** [x] Completed

## Steps

1. **Create Branch:**
   ```bash
   git checkout main && git pull origin main
   git checkout -b epmcdme-16232-v4
   ```

2. **Add Script & Reusable Workflow:**
   - Add `scripts/release/check_version.py` to `ci-workflows` (can be copied from `codemie-cdk/scripts/release/check_version.py`).
   - Create `.github/workflows/reusable-release-version-check.yml`:
     - Inputs:
       - `ecosystem`: `npm` or `pypi`
       - `package-name`: name of package
       - `tag`: release tag (e.g. `cdk-v0.2.1` or `node-v0.1.0`)
       - `tag-prefix`: optional prefix
       - `base-version`: baseline version from manifest
       - `verify-tag-on-main`: boolean (default `true`)
     - Verifies git tag points to SHA and exists on `main`.
     - Validates version against registry using `check_version.py`.
     - Outputs validated version.

3. **Commit & PR:**
   ```bash
   git add scripts/release/check_version.py .github/workflows/reusable-release-version-check.yml
   git commit -m "EPMCDME-16232: add reusable release version check workflow"
   git push origin epmcdme-16232-v4
   gh pr create --title "ci(workflows): add reusable release version check workflow" --body "Centralizes git tag and package registry version verification."
   ```
