#!/usr/bin/env python3
"""
Fetch all repositories for codemie-ai on branch 'main' and check if GitHub Actions workflows exist.
Skips repositories specified in references/excluded_repositories.json.
Saves to references/repositories.json with fields:
- name
- url
- default_branch ("main")
- has_github_workflows (boolean)
"""

import json
import os
import subprocess
import sys

ORG = "codemie-ai"
BRANCH = "main"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "..", "references", "repositories.json")
EXCLUSIONS_FILE = os.path.join(SCRIPT_DIR, "..", "references", "excluded_repositories.json")

def load_exclusions():
    if os.path.exists(EXCLUSIONS_FILE):
        try:
            with open(EXCLUSIONS_FILE) as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except Exception as e:
            print(f"Warning: failed to read {EXCLUSIONS_FILE}: {e}", file=sys.stderr)
    return set()

def main():
    excluded = load_exclusions()
    print(f"Loaded {len(excluded)} exclusions: {list(excluded)}", file=sys.stderr)
    print(f"Fetching repositories for {ORG} via gh CLI...", file=sys.stderr)
    cmd = ["gh", "repo", "list", ORG, "--limit", "100", "--json", "name,url"]
    try:
        raw_repos = json.loads(subprocess.check_output(cmd, text=True))
    except Exception as e:
        print(f"Error fetching repos: {e}", file=sys.stderr)
        sys.exit(1)

    catalog = []
    total = len(raw_repos)
    for idx, r in enumerate(raw_repos, start=1):
        name = r["name"]
        if name in excluded:
            print(f"[{idx}/{total}] Skipping excluded repository: {name}", file=sys.stderr)
            continue

        print(f"[{idx}/{total}] Checking workflows for {name} on branch {BRANCH}...", file=sys.stderr)
        wf_res = subprocess.run(
            ["gh", "api", f"repos/{ORG}/{name}/contents/.github/workflows?ref={BRANCH}"],
            capture_output=True,
            text=True
        )
        has_wf = False
        if wf_res.returncode == 0:
            try:
                data = json.loads(wf_res.stdout)
                if isinstance(data, list) and any(f.get("type") == "file" for f in data):
                    has_wf = True
            except Exception:
                pass

        catalog.append({
            "name": name,
            "url": r["url"],
            "default_branch": BRANCH,
            "has_github_workflows": has_wf
        })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(catalog, f, indent=2)

    print(f"Saved {len(catalog)} repositories to {OUTPUT_FILE}", file=sys.stderr)

if __name__ == "__main__":
    main()
