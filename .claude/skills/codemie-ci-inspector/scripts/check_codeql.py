#!/usr/bin/env python3
"""
Check if a repository (or all repositories in repositories.json) uses the shared CodeQL workflow:
codemie-ai/ci-workflows/.github/workflows/reusable-codeql.yml@main

Usage:
  python3 check_codeql.py <repo-name>   -> prints true or false
  python3 check_codeql.py               -> prints JSON with true/false for all repos
"""

import base64
import json
import os
import subprocess
import sys

ORG = "codemie-ai"
SHARED_PATTERN = "codemie-ai/ci-workflows/.github/workflows/reusable-codeql.yml"
LOCAL_PATTERN = ".github/workflows/reusable-codeql.yml"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CATALOG_PATH = os.path.join(SCRIPT_DIR, "..", "references", "repositories.json")

def check_repo(repo_name):
    cmd = ["gh", "api", f"repos/{ORG}/{repo_name}/contents/.github/workflows?ref=main"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return False

    try:
        files = json.loads(res.stdout)
    except Exception:
        return False

    for f in files:
        if f.get("type") == "file":
            fres = subprocess.run(["gh", "api", f["url"]], capture_output=True, text=True)
            if fres.returncode != 0:
                continue
            try:
                content = base64.b64decode(json.loads(fres.stdout)["content"]).decode("utf-8", errors="ignore")
                if SHARED_PATTERN in content or (repo_name == "ci-workflows" and LOCAL_PATTERN in content):
                    return True
            except Exception:
                continue

    return False

def main():
    if len(sys.argv) > 1:
        repo_name = sys.argv[1]
        print("true" if check_repo(repo_name) else "false")
        return

    if not os.path.exists(CATALOG_PATH):
        print(f"Catalog not found: {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH) as f:
        catalog = json.load(f)

    results = {}
    for item in catalog:
        name = item["name"]
        if not item.get("has_github_workflows", False):
            results[name] = False
        else:
            results[name] = check_repo(name)

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
