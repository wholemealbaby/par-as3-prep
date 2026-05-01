#!/usr/bin/env python3
"""
Sync issues from .issues/*.md files to GitHub Issues and add them to Project ID 3.

This script:
1. Reads all markdown files in the .issues/ directory
2. Parses each section (separated by ---) as a distinct issue
3. Creates or updates GitHub Issues for each section
4. Adds/updates the issues in GitHub Project ID 3

Configuration is loaded from (in priority order):
  1. Environment variables (GITHUB_TOKEN, GITHUB_REPOSITORY, PROJECT_ID)
  2. A .env file at .github/scripts/.env (or custom path via ENV_FILE env var)

Usage:
    GITHUB_TOKEN=<token> GITHUB_REPOSITORY=owner/repo python3 sync_issues.py
    # or with .env file:
    python3 sync_issues.py
"""

import os
import re
import sys
import json
import hashlib
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

# ─── .env File Loader ────────────────────────────────────────────────────────


def load_env_file(env_path: str = ".github/scripts/.env") -> dict:
    """
    Load a .env file and return a dict of key-value pairs.
    Supports:
      - KEY=VALUE lines
      - # comments
      - Quoted values (single and double)
      - Trims whitespace
    """
    env_path = os.environ.get("ENV_FILE", env_path)
    env_file = Path(env_path)
    if not env_file.exists():
        return {}

    env_vars = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue
        # Split on first =
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip surrounding quotes if present
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        env_vars[key] = value
    return env_vars


# ─── Configuration ───────────────────────────────────────────────────────────

# Load .env file first (lowest priority)
_env_file = load_env_file()

# Environment variables override .env (higher priority)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or _env_file.get("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY") or _env_file.get("GITHUB_REPOSITORY", "")
PROJECT_ID = os.environ.get("PROJECT_ID") or _env_file.get("PROJECT_ID", "3")
ISSUES_DIR = Path(os.environ.get("ISSUES_DIR") or _env_file.get("ISSUES_DIR", ".issues"))

if not GITHUB_TOKEN:
    print("❌ GITHUB_TOKEN is required. Set it via environment variable or .env file.")
    sys.exit(1)

if not GITHUB_REPOSITORY:
    print("❌ GITHUB_REPOSITORY is required. Set it via environment variable or .env file.")
    sys.exit(1)

API_BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
}

# ─── Label Color Configuration ───────────────────────────────────────────────
#
# Map label names to bright, bold hex colors (without the leading #).
# Labels not in this map will be created with a default color.
# To customise, add entries here or override via the LABEL_COLORS env variable
# as a JSON object, e.g.:
#   LABEL_COLORS='{"evidence":"00ff88","planning":"ff8800"}'

DEFAULT_LABEL_COLOR = "aabbcc"

LABEL_COLORS = {
    # Evidence pipeline labels
    "evidence": "00ff88",          # Bright green
    "planning": "ff8800",          # Bright orange
    "requirements": "ffdd00",      # Bright yellow
    "test-design": "ff00ff",       # Bright magenta
    "infrastructure": "00ccff",    # Bright cyan
    "ros2": "8844ff",              # Bright purple
    "vision": "ff4488",            # Bright pink
    "metrics": "44ff44",           # Bright lime
    "template": "ffaa00",          # Bright amber
    "documentation": "4488ff",     # Bright blue
    "demo-prep": "ff6644",         # Bright coral
    "pg-requirement": "ff0044",    # Bright red
    "experiment": "aa44ff",        # Bright violet
    # Fallback / generic
    "bug": "ff0000",               # Red
    "enhancement": "0088ff",       # Blue
    "question": "ff8800",          # Orange
}

# Allow override via environment variable
_env_label_colors = os.environ.get("LABEL_COLORS")
if _env_label_colors:
    try:
        overrides = json.loads(_env_label_colors)
        LABEL_COLORS.update(overrides)
        print(f"📋 Loaded {len(overrides)} label color override(s) from LABEL_COLORS env var")
    except json.JSONDecodeError as e:
        print(f"⚠️  Invalid LABEL_COLORS JSON: {e}. Using built-in colors.")

# ─── HTTP Helpers ────────────────────────────────────────────────────────────


def api_request(method, url, data=None):
    """Make an authenticated GitHub API request."""
    if data is not None:
        data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"⚠️  HTTP {e.code} on {method} {url}: {body}")
        return None
    except Exception as e:
        print(f"⚠️  Request failed: {e}")
        return None


def graphql_query(query, variables=None):
    """Execute a GitHub GraphQL query."""
    url = f"{API_BASE}/graphql"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"⚠️  GraphQL HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"⚠️  GraphQL request failed: {e}")
        return None


# ─── Label Sync ──────────────────────────────────────────────────────────────


def get_existing_labels():
    """Fetch all labels for the repository."""
    url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/labels?per_page=100"
    result = api_request("GET", url)
    if result is None:
        return {}
    return {label["name"]: label for label in result}


def ensure_labels_exist(required_labels):
    """
    Ensure all required labels exist in the repository with the configured colors.
    Creates or updates labels to have bright, bold colors.
    """
    existing = get_existing_labels()
    repo_labels_url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/labels"

    for label_name in required_labels:
        color = LABEL_COLORS.get(label_name, DEFAULT_LABEL_COLOR)
        description = f"Label: {label_name}"

        if label_name in existing:
            # Update if color differs
            existing_color = existing[label_name].get("color", "")
            if existing_color != color:
                print(f"  🎨 Updating label color: '{label_name}' ({existing_color} → {color})")
                api_request(
                    "PATCH",
                    f"{repo_labels_url}/{urllib.parse.quote(label_name, safe='')}",
                    {"color": color, "description": description},
                )
            else:
                print(f"  ✅ Label '{label_name}' already has color #{color}")
        else:
            # Create the label
            print(f"  🎨 Creating label: '{label_name}' with color #{color}")
            api_request(
                "POST",
                repo_labels_url,
                {"name": label_name, "color": color, "description": description},
            )


# ─── Issue Parsing ───────────────────────────────────────────────────────────


def parse_issues_from_markdown(filepath):
    """
    Parse a markdown file into a list of issue dicts.

    Each section separated by `---` is treated as a separate issue.
    The first section (before any ---) is treated as the file header and skipped.
    """
    text = Path(filepath).read_text(encoding="utf-8")
    sections = re.split(r"\n---+\n", text)

    issues = []
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue

        # Skip the header section (first section, typically # Title ...)
        if i == 0:
            continue

        issue = parse_single_issue(section, filepath)
        if issue:
            issues.append(issue)

    return issues


def parse_single_issue(section, source_file):
    """Parse a single issue section into a structured dict."""
    lines = section.split("\n")

    # Extract title (first ## heading)
    title = ""
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            title = m.group(1).strip()
            break

    if not title:
        return None

    # Extract issue ID from title (e.g., "EP-01 · ..." -> "EP-01")
    issue_id_match = re.match(r"^([A-Z]+-\d+)", title)
    issue_id = issue_id_match.group(1) if issue_id_match else ""

    # Extract labels
    labels = []
    labels_match = re.search(r"\*\*Labels:\*\*\s*(.+?)(?:\n|$)", section)
    if labels_match:
        raw = labels_match.group(1)
        labels = re.findall(r"`([^`]+)`", raw)

    # Extract assignee
    assignee = ""
    assignee_match = re.search(r"\*\*Assignee:\*\*\s*(.+?)(?:\n|$)", section)
    if assignee_match:
        assignee = assignee_match.group(1).strip()

    # Extract milestone
    milestone = ""
    milestone_match = re.search(r"\*\*Milestone:\*\*\s*(.+?)(?:\n|$)", section)
    if milestone_match:
        milestone = milestone_match.group(1).strip()

    # Extract priority
    priority = ""
    priority_match = re.search(r"\*\*Priority:\*\*\s*(.+?)(?:\n|$)", section)
    if priority_match:
        priority = priority_match.group(1).strip()

    # Build the issue body
    body_parts = []
    body_parts.append(f"**Source:** `{source_file}` | **Issue ID:** {issue_id}")
    body_parts.append("")
    body_parts.append(f"**Priority:** {priority}" if priority else "")
    body_parts.append(f"**Milestone:** {milestone}" if milestone else "")
    body_parts.append(f"**Assignee:** {assignee}" if assignee else "")
    body_parts.append("")

    # Add the rest of the section content (skip the metadata header lines)
    in_metadata = True
    for line in lines:
        stripped = line.strip()
        # Skip the title line
        if re.match(r"^##\s+", line):
            continue
        # Skip metadata lines (Labels:, Assignee:, Milestone:, Priority:)
        if in_metadata and re.match(r"^\*\*(Labels|Assignee|Milestone|Priority):", stripped):
            continue
        # Once we hit a non-metadata heading, stop skipping
        if stripped.startswith("###") or stripped.startswith("- [") or stripped.startswith("|"):
            in_metadata = False

        if not in_metadata:
            body_parts.append(line)

    body = "\n".join(body_parts).strip()

    # Generate a stable fingerprint for deduplication
    fingerprint = hashlib.sha256(
        (title + str(source_file) + issue_id).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "title": title,
        "body": body,
        "labels": labels,
        "assignee": assignee,
        "milestone": milestone,
        "priority": priority,
        "issue_id": issue_id,
        "source_file": str(source_file),
        "fingerprint": fingerprint,
    }


# ─── GitHub Issue Sync ───────────────────────────────────────────────────────


def get_existing_issues():
    """Fetch all open issues for the repository."""
    url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues?state=all&per_page=100"
    issues = []
    page = 1
    while url:
        print(f"  📋 Fetching issues page {page}...")
        result = api_request("GET", url)
        if result is None:
            break
        issues.extend(result)
        # Check for next page in Link header (simplified: just try next page)
        page += 1
        url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues?state=all&per_page=100&page={page}"
        if len(result) < 100:
            break
    return issues


def find_matching_issue(existing_issues, parsed_issue):
    """
    Find an existing issue that matches a parsed issue.
    Matches by title or by fingerprint embedded in the issue body.
    """
    fingerprint_tag = f"<!-- issue-fingerprint: {parsed_issue['fingerprint']} -->"

    for issue in existing_issues:
        # Check by fingerprint tag in body
        body = issue.get("body", "") or ""
        if fingerprint_tag in body:
            return issue

        # Check by title match
        if issue["title"].strip() == parsed_issue["title"].strip():
            return issue

    return None


def create_issue(parsed_issue):
    """Create a new GitHub Issue."""
    fingerprint_tag = f"<!-- issue-fingerprint: {parsed_issue['fingerprint']} -->"
    body = f"{fingerprint_tag}\n\n{parsed_issue['body']}"

    data = {
        "title": parsed_issue["title"],
        "body": body,
        "labels": parsed_issue["labels"],
    }

    print(f"  ➕ Creating issue: {parsed_issue['title']}")
    result = api_request(
        "POST",
        f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues",
        data,
    )
    return result


def update_issue(existing, parsed_issue):
    """Update an existing GitHub Issue if content changed."""
    fingerprint_tag = f"<!-- issue-fingerprint: {parsed_issue['fingerprint']} -->"
    new_body = f"{fingerprint_tag}\n\n{parsed_issue['body']}"

    # Check if anything changed
    existing_body = (existing.get("body") or "").strip()
    existing_title = existing.get("title", "").strip()
    existing_labels = [l["name"] for l in existing.get("labels", [])]

    needs_update = False
    if existing_title != parsed_issue["title"].strip():
        needs_update = True
    if existing_body != new_body.strip():
        needs_update = True
    if set(existing_labels) != set(parsed_issue["labels"]):
        needs_update = True

    if not needs_update:
        print(f"  ✅ No changes for: {parsed_issue['title']}")
        return existing

    data = {
        "title": parsed_issue["title"],
        "body": new_body,
        "labels": parsed_issue["labels"],
    }

    print(f"  🔄 Updating issue: {parsed_issue['title']}")
    result = api_request(
        "PATCH",
        f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues/{existing['number']}",
        data,
    )
    return result


# ─── GitHub Project (Classic) Sync ──────────────────────────────────────────


def add_issue_to_project(issue_number):
    """
    Add an issue to GitHub Project (classic) ID 3 using the GraphQL API.

    Uses the addProjectCard mutation to add the issue to the project.
    First, we need to find the column ID for the project.
    """
    # Step 1: Get project columns
    print(f"  📋 Fetching project {PROJECT_ID} columns...")
    columns_url = f"{API_BASE}/projects/{PROJECT_ID}/columns"
    columns = api_request("GET", columns_url)
    if columns is None:
        print(f"  ⚠️  Could not fetch project columns. Project may not exist or token lacks access.")
        return False

    if not columns:
        print(f"  ⚠️  No columns found in project {PROJECT_ID}")
        return False

    # Use the first column (typically "To do")
    target_column = columns[0]
    column_id = target_column["id"]
    column_name = target_column["name"]
    print(f"  📋 Using column: '{column_name}' (ID: {column_id})")

    # Step 2: Get the issue's content ID (needed for GraphQL)
    issue_url = f"{API_BASE}/repos/{GITHUB_REPOSITORY}/issues/{issue_number}"
    issue_data = api_request("GET", issue_url)
    if issue_data is None:
        print(f"  ⚠️  Could not fetch issue #{issue_number}")
        return False

    content_id = issue_data.get("id")
    if not content_id:
        print(f"  ⚠️  No content ID for issue #{issue_number}")
        return False

    # Step 3: Check if issue is already in the project
    cards_url = f"{API_BASE}/projects/columns/{column_id}/cards"
    cards = api_request("GET", cards_url)
    if cards:
        for card in cards:
            card_content_url = card.get("content_url", "")
            if card_content_url and str(issue_number) in card_content_url:
                print(f"  ✅ Issue #{issue_number} already in project column '{column_name}'")
                return True

    # Step 4: Add card to project column
    print(f"  ➕ Adding issue #{issue_number} to project column '{column_name}'...")
    result = api_request(
        "POST",
        f"{API_BASE}/projects/columns/{column_id}/cards",
        {"content_id": content_id, "content_type": "Issue"},
    )
    if result:
        print(f"  ✅ Added issue #{issue_number} to project")
        return True
    else:
        print(f"  ⚠️  Failed to add issue #{issue_number} to project")
        return False


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    print("=" * 60)
    print(f"📂 Syncing issues from {ISSUES_DIR}/ to {GITHUB_REPOSITORY}")
    print(f"📋 Project ID: {PROJECT_ID}")
    print("=" * 60)

    # Find all markdown files in .issues/
    md_files = sorted(ISSUES_DIR.glob("*.md"))
    if not md_files:
        print(f"❌ No markdown files found in {ISSUES_DIR}/")
        sys.exit(0)

    print(f"\n📄 Found {len(md_files)} markdown file(s): {[f.name for f in md_files]}")

    # Parse all issues from all files
    all_parsed_issues = []
    for md_file in md_files:
        print(f"\n--- Parsing: {md_file} ---")
        issues = parse_issues_from_markdown(md_file)
        print(f"  📝 Found {len(issues)} issue(s)")
        all_parsed_issues.extend(issues)

    if not all_parsed_issues:
        print("❌ No issues parsed from markdown files")
        sys.exit(0)

    print(f"\n📊 Total parsed issues: {len(all_parsed_issues)}")

    # Collect all unique labels across all issues and ensure they exist with bright colors
    all_labels = set()
    for parsed in all_parsed_issues:
        all_labels.update(parsed["labels"])
    if all_labels:
        print(f"\n--- Ensuring labels exist with bright colors ---")
        print(f"  🏷️  Labels to sync: {sorted(all_labels)}")
        ensure_labels_exist(all_labels)
    else:
        print("\n  ℹ️  No labels found in parsed issues")

    # Fetch existing issues from GitHub
    print("\n--- Fetching existing issues from GitHub ---")
    existing_issues = get_existing_issues()
    print(f"  📋 Found {len(existing_issues)} existing issues")

    # Sync each parsed issue
    print("\n--- Syncing issues ---")
    synced_count = 0
    created_count = 0
    updated_count = 0
    skipped_count = 0

    for parsed in all_parsed_issues:
        print(f"\n  🔍 Processing: {parsed['title']}")
        match = find_matching_issue(existing_issues, parsed)

        if match:
            # Issue exists — update it
            result = update_issue(match, parsed)
            if result:
                updated_count += 1
                issue_number = result.get("number", match["number"])
                # Ensure it's in the project
                add_issue_to_project(issue_number)
            else:
                skipped_count += 1
        else:
            # Issue doesn't exist — create it
            result = create_issue(parsed)
            if result:
                created_count += 1
                issue_number = result.get("number")
                print(f"  ✅ Created issue #{issue_number}")
                # Add to project
                add_issue_to_project(issue_number)
            else:
                skipped_count += 1

        synced_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("📊 SYNC SUMMARY")
    print("=" * 60)
    print(f"  Total issues parsed:    {len(all_parsed_issues)}")
    print(f"  Created:                {created_count}")
    print(f"  Updated:                {updated_count}")
    print(f"  Skipped (errors):       {skipped_count}")
    print(f"  Synced to Project #{PROJECT_ID}:   {synced_count - skipped_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
