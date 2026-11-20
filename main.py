#!/usr/bin/env python3
"""Entrypoint for the news-image-20261119 v3 entry.

The front page for Thursday 19 November 2026 is drawn by draw.py and
shipped in this repository as entry.png. This program's only job is to
put that file where the grader expects it: /output/entry.png.

It does no drawing, no fetching and no random work, so repeated runs
always produce the same output bytes. When run outside the grader,
set MAKEFUN_OUTPUT_DIR to a writable directory instead of /output:

    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"


def repo_root():
    return Path(__file__).resolve().parent


def output_dir():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT)


def main():
    source = repo_root() / IMAGE_NAME
    if not source.is_file():
        print(f"entry image not found: {source}", file=sys.stderr)
        return 1
    dest = output_dir()
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest / IMAGE_NAME)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
