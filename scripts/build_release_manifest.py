#!/usr/bin/env python3
"""Build the manifest for the exported arXiv artifact package."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path


MANIFEST_NAME = "manifest.json"
EXCLUDED_PATHS = {
    Path("manifest.json"),
    Path("paper/paper.pdf"),
    Path("paper/paper.aux"),
    Path("paper/paper.log"),
    Path("paper/paper.out"),
    Path("paper/paper.bbl"),
    Path("paper/paper.blg"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def package_files(root: Path) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if not path.is_file():
            continue
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        if ".git" in relative.parts or ".qa" in relative.parts:
            continue
        if path.name in {".DS_Store"} or relative in EXCLUDED_PATHS:
            continue
        files.append(path)
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Exported package root")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify the existing manifest instead of rebuilding it",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    if args.verify:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        entries = manifest["files"]
        if manifest["file_count"] != len(entries):
            raise SystemExit("manifest file_count mismatch")
        actual = {path.relative_to(root).as_posix() for path in package_files(root)}
        listed = {entry["path"] for entry in entries}
        if actual != listed:
            raise SystemExit("manifest path set mismatch")
        for entry in entries:
            path = root / entry["path"]
            if path.stat().st_size != entry["bytes"]:
                raise SystemExit(f"size mismatch: {entry['path']}")
            if sha256(path) != entry["sha256"]:
                raise SystemExit(f"hash mismatch: {entry['path']}")
        print(f"manifest_ok: {len(entries)} files")
        return
    files = [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in package_files(root)
    ]
    manifest = {
        "package": "evidence-closure-rag-arxiv-v1",
        "schema_version": 2,
        "date": date.today().isoformat(),
        "license": "MIT",
        "file_count": len(files),
        "files": files,
    }
    output = root / "manifest.json"
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{output}: {len(files)} files")


if __name__ == "__main__":
    main()
