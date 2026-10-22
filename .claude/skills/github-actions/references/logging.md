# GitHub Actions Logging and Log Grouping

Workflow commands format output in the GitHub Actions runner, creating visual annotations on Pull Requests and Checks pages.

Official docs: [Workflow commands for GitHub Actions](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/workflow-commands-for-github-actions)

## Log Levels (Workflow Commands)

Use GitHub workflow commands instead of plain `echo` for statuses, warnings, and errors.

```bash
# Error: highlights red, creates PR check failure annotation
echo "::error::Validation failed: schema is invalid"

# Warning: highlights yellow, creates PR warning annotation
echo "::warning::Deprecated configuration detected, update to v2"

# Notice: neutral info callout in GitHub UI
echo "::notice::Using repository configuration: commitlint.config.js"

# Debug: visible only when ACTIONS_STEP_DEBUG repository secret is set to true
echo "::debug::Current payload: $PAYLOAD"
```

### File and Line Annotations

Link messages directly to specific files, lines, and columns in the PR diff:

```bash
echo "::error file=config.json,line=12,col=5::Syntax error in JSON file"
echo "::warning file=Dockerfile,line=3::Base image tag is floating"
```

Supported parameters:
- `file`: Path relative to workspace root
- `line`: Line number
- `endLine`: Ending line number for ranges
- `col`: Column number
- `endColumn`: Ending column number
- `title`: Short title for the annotation (e.g. `title=Linting error`)

Example with title:
```bash
echo "::error file=src/index.ts,line=42,title=Type Error::Variable 'data' implicitly has 'any' type"
```

## Collapsible Log Groups

Wrap verbose command outputs (package installs, git logs, diffs, build traces) into collapsible sections.

### Basic Syntax

```bash
echo "::group::Installed tool versions"
git --version
node --version
npm --version
echo "::endgroup::"
```

### Safe Execution with Error Handling

Ensure `::endgroup::` is executed even if the command fails, preventing broken log formatting:

```bash
echo "::group::Run linter details"
if ! npx eslint . --format stylish; then
  echo "::endgroup::"
  echo "::error::Linting failed"
  exit 1
fi
echo "::endgroup::"
```
