#!/usr/bin/env python3
"""Summarize a directory with file counts, sizes, and a compact tree."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def human_size(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def relative_depth(root: Path, current: Path) -> int:
    rel = current.relative_to(root)
    if rel == Path("."):
        return 0
    return len(rel.parts)


def walk_directory(root: Path, max_depth: int | None = None) -> tuple[int, int, int]:
    files = 0
    dirs = 0
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(root):
        depth = relative_depth(root, Path(dirpath))
        if max_depth is not None and depth >= max_depth:
            dirnames[:] = []
        dirs += len(dirnames)
        files += len(filenames)
        for name in filenames:
            path = Path(dirpath) / name
            try:
                total_bytes += path.stat().st_size
            except OSError:
                continue
    return files, dirs, total_bytes


def print_tree(root: Path, max_entries: int = 40, max_depth: int | None = None) -> None:
    shown = 0
    for dirpath, dirnames, filenames in os.walk(root):
        depth = relative_depth(root, Path(dirpath))
        if max_depth is not None and depth >= max_depth:
            dirnames[:] = []
        dirnames.sort()
        filenames.sort()
        rel = Path(dirpath).relative_to(root)
        indent = "  " * (0 if rel == Path(".") else len(rel.parts))
        label = "." if rel == Path(".") else rel.name
        print(f"{indent}{label}/")
        shown += 1
        for name in filenames:
            if shown >= max_entries:
                print("  ...")
                return
            print(f"{indent}  {name}")
            shown += 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a directory tree.")
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--json", action="store_true", help="Print a JSON summary")
    parser.add_argument("--max-depth", type=int, default=None, help="Limit directory walk depth")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}")
        return 1

    files, dirs, total_bytes = walk_directory(root, args.max_depth)
    if args.json:
        print(json.dumps({
            "path": str(root),
            "files": files,
            "directories": dirs,
            "total_bytes": total_bytes,
            "max_depth": args.max_depth,
        }, indent=2))
        return 0

    print(f"Path: {root}")
    print(f"Files: {files}")
    print(f"Directories: {dirs}")
    print(f"Total size: {human_size(total_bytes)}")
    print()
    print_tree(root, max_depth=args.max_depth)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
