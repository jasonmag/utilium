#!/usr/bin/env python3
"""
Generate a tree-style listing of files and folders and write it to a text file.

Usage:
    python tree_to_text.py /path/to/root --output tree.txt --include-hidden --max-depth 3 --exclude node_modules --exclude .git --exclude-path 'build/*'
"""

import argparse
import os
from fnmatch import fnmatch
from typing import Generator, Iterable, Optional


def iter_tree(
    root: str,
    include_hidden: bool = False,
    max_depth: Optional[int] = None,
    excludes: Optional[list[str]] = None,
    exclude_paths: Optional[list[str]] = None,
) -> Generator[str, None, None]:
    """Yield an ASCII tree of the directory structure starting at root."""
    root_abs = os.path.abspath(root)
    root_label = os.path.basename(root_abs) or root_abs
    yield root_label

    def walk(dir_path: str, prefix: str, depth: int, rel_path: str) -> Iterable[str]:
        if max_depth is not None and depth > max_depth:
            return

        try:
            entries = sorted(entry for entry in os.listdir(dir_path))
        except OSError as err:
            yield f"{prefix}[error opening directory: {err}]"
            return

        def should_skip(name: str, current_rel: str) -> bool:
            if not include_hidden and name.startswith("."):
                return True
            if excludes:
                return any(fnmatch(name, pattern) for pattern in excludes)
            if exclude_paths:
                return any(fnmatch(current_rel, pattern) for pattern in exclude_paths)
            return False

        entries = [
            entry for entry in entries if not should_skip(entry, os.path.join(rel_path, entry))
        ]

        total = len(entries)
        for index, entry in enumerate(entries):
            full_path = os.path.join(dir_path, entry)
            connector = "`-- " if index == total - 1 else "|-- "
            yield f"{prefix}{connector}{entry}"

            if os.path.isdir(full_path):
                extension = "    " if index == total - 1 else "|   "
                yield from walk(
                    full_path,
                    prefix + extension,
                    depth + 1,
                    os.path.join(rel_path, entry),
                )

    yield from walk(root_abs, prefix="", depth=1, rel_path="")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a tree-style listing of a directory to a text file"
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="tree.txt",
        help="Where to write the listing (default: tree.txt)",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include files and folders starting with '.'",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Limit recursion depth (1 = only children of root)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Glob-style name to skip (can repeat, e.g., --exclude node_modules --exclude '*.pyc')",
    )
    parser.add_argument(
        "--exclude-path",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Glob-style relative path to skip (can repeat, e.g., --exclude-path 'build/*' --exclude-path 'src/**/dist')",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not os.path.isdir(args.root):
        raise SystemExit(f"Path is not a directory: {args.root}")

    lines = list(
        iter_tree(
            args.root,
            include_hidden=args.include_hidden,
            max_depth=args.max_depth,
            excludes=args.exclude,
            exclude_paths=args.exclude_path,
        )
    )
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"Wrote tree for '{args.root}' to '{args.output}'")


if __name__ == "__main__":
    main()
