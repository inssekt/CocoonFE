"""Builds the catalogue Cocoon downloads.

    python3 tools/build.py --out dist [--previous published]

Writes android.json and manifest.json to --out. --previous is a folder holding the published
manifest.json: the version goes up by one whenever android.json changes.
"""

import argparse
import hashlib
import json
import os

from platforms import build, load


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--previous")
    args = parser.parse_args()

    retroarch, docs = load()
    data = json.dumps(build(retroarch, docs), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()

    version = 1
    published = os.path.join(args.previous, "manifest.json") if args.previous else None
    if published and os.path.exists(published):
        old = json.load(open(published))
        version = old["version"] if old.get("sha256") == digest else old["version"] + 1

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "android.json"), "wb") as f:
        f.write(data)
    manifest = {"format": 1, "version": version, "file": "android.json", "size": len(data), "sha256": digest}
    with open(os.path.join(args.out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(f"android.json version {version}, {len(data)} bytes, sha256 {digest}")


if __name__ == "__main__":
    main()
