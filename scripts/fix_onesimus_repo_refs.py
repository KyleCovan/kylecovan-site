#!/usr/bin/env python3
"""Update Onesimus references after KyleCovan/kylecovan-site → kylecovan-com.

The Acasis SSD is not mounted in cloud agents. Run this on Kyle's Mac once the
GitHub rename is done and Onesimus is available:

    python3 scripts/fix_onesimus_repo_refs.py
    python3 scripts/fix_onesimus_repo_refs.py --onesimus /path/to/Onesimus
    python3 scripts/fix_onesimus_repo_refs.py --dry-run

Safe replacements only:
  - KyleCovan/kylecovan-site → KyleCovan/kylecovan-com
  - github.com/KyleCovan/kylecovan-site → github.com/KyleCovan/kylecovan-com

Does NOT touch kylecovan-site.pages.dev or bare Cloudflare project names.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

DEFAULT_ONESIMUS = Path(
    "/Volumes/Acasis Samsung SSD 990 PRO 4TB/kernel journal/Onesimus"
)

OLD_FULL = "KyleCovan/kylecovan-site"
NEW_FULL = "KyleCovan/kylecovan-com"
OLD_HOSTED = "github.com/KyleCovan/kylecovan-site"
NEW_HOSTED = "github.com/KyleCovan/kylecovan-com"

SKIP_DIR_NAMES = {
    ".git",
    ".trash",
    "node_modules",
    ".venv",
    "__pycache__",
    ".obsidian",
}

# Binary / noise extensions we never rewrite.
SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".pdf",
    ".zip",
    ".mp4",
    ".mov",
    ".wav",
    ".mp3",
    ".sqlite",
    ".db",
}


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        yield path


def rewrite(text: str) -> tuple[str, int]:
    """Return (new_text, replacement_count). Order matters: hosted URL first."""
    count = 0
    if OLD_HOSTED in text:
        n = text.count(OLD_HOSTED)
        text = text.replace(OLD_HOSTED, NEW_HOSTED)
        count += n
    if OLD_FULL in text:
        n = text.count(OLD_FULL)
        text = text.replace(OLD_FULL, NEW_FULL)
        count += n
    return text, count


def append_decision(onesimus: Path, dry_run: bool) -> Path | None:
    log = onesimus / "decisions" / "log.md"
    if not log.parent.is_dir():
        return None
    stamp = dt.date.today().isoformat()
    entry = (
        f"\n## {stamp} — GitHub repo rename: kylecovan-site → kylecovan-com\n\n"
        f"- **Decision:** The public GitHub repo for kylecovan.com is now "
        f"`{NEW_FULL}` (was `{OLD_FULL}`).\n"
        f"- **Unchanged:** Cloudflare Pages project `kylecovan-site` and "
        f"`kylecovan-site.pages.dev`; local folder `~/Projects/kylecovan-astro`.\n"
        f"- **Why:** Align the repo name with the domain and the "
        f"`kylecovan-com` build id.\n"
        f"- **Follow-up:** Confirm Cloudflare GitHub App still has access; "
        f"update any clone remotes still on the old URL.\n"
    )
    if dry_run:
        print(f"Would append decision entry to {log}")
        return log
    if log.exists():
        existing = log.read_text(encoding="utf-8")
        if NEW_FULL in existing and "kylecovan-site → kylecovan-com" in existing:
            print(f"Decision already recorded in {log}")
            return log
        log.write_text(existing.rstrip() + "\n" + entry, encoding="utf-8")
    else:
        log.write_text(
            "# Decisions log\n" + entry,
            encoding="utf-8",
        )
    print(f"Appended decision entry to {log}")
    return log


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--onesimus",
        type=Path,
        default=DEFAULT_ONESIMUS,
        help="Path to the Onesimus vault root",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List matches and planned edits without writing",
    )
    args = parser.parse_args()
    root: Path = args.onesimus

    if not root.is_dir():
        print(
            f"Onesimus not found at {root}\n"
            "Mount the Acasis SSD, or pass --onesimus /path/to/Onesimus",
            file=sys.stderr,
        )
        return 1

    files_touched = 0
    replacements = 0
    hits: list[tuple[Path, int]] = []

    for path in iter_text_files(root):
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if OLD_FULL not in original and OLD_HOSTED not in original:
            continue
        updated, count = rewrite(original)
        if count == 0:
            continue
        hits.append((path, count))
        replacements += count
        files_touched += 1
        rel = path.relative_to(root)
        if args.dry_run:
            print(f"Would update {rel} ({count})")
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"Updated {rel} ({count})")

    append_decision(root, args.dry_run)

    print(
        f"{'Dry run: ' if args.dry_run else ''}"
        f"{files_touched} file(s), {replacements} replacement(s) under {root}"
    )
    if not hits and not args.dry_run:
        print("No KyleCovan/kylecovan-site references found (already clean, or never recorded).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
