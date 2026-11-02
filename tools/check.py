"""Checks the platform files.

    python3 tools/check.py [--previous android.json]

--previous is the published catalogue. With it, the check lists what changed and fails if a player
ID has gone without being named in a player's was: or the platform's retired:.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

from platforms import TOOLS, build, load, problems


def java():
    home = os.environ.get("JAVA_HOME")
    if home and os.path.exists(os.path.join(home, "bin", "java")):
        return os.path.join(home, "bin", "java")
    return shutil.which("java")


def bad_patterns(patterns):
    exe = java()
    if exe is None:
        sys.exit("Java is needed to check file patterns the way Cocoon reads them")
    result = subprocess.run([exe, os.path.join(TOOLS, "RegexCheck.java")], input="\n".join(patterns) + "\n",
                            capture_output=True, text=True)
    if result.returncode not in (0, 1):
        sys.exit(result.stderr.strip())
    return [line for line in result.stdout.splitlines() if line]


def compare(previous, current, docs):
    found, changes = [], []
    before = {p["id"]: p for p in previous["platforms"]}
    after = {p["id"]: p for p in current["platforms"]}
    renamed = {old: p["id"] for p in current["platforms"] for old in p.get("was", [])}
    for pid in sorted(set(after) - set(before)):
        changes.append(f"{pid}: new platform")
    for pid in sorted(set(before) - set(after)):
        if pid in renamed:
            changes.append(f"{pid}: renamed to {renamed[pid]}")
        else:
            found.append(f"{pid}: the platform is gone. If it was renamed, add it to the new platform's was:")
    for pid, old in before.items():
        new = after.get(pid) or after.get(renamed.get(pid))
        if new is None:
            continue
        doc = docs[new["id"]]
        allowed = set(doc.get("retired") or [])
        allowed |= {old_id for item in doc.get("players") or [] for old_id in item.get("was") or []}
        old_players = {p["id"]: p for p in old["players"]}
        new_players = {p["id"]: p for p in new["players"]}
        for player_id in old_players.keys() - new_players.keys():
            if player_id in allowed:
                changes.append(f"{new['id']}: {player_id} retired or renamed")
            else:
                found.append(f"{new['id']}: player {player_id} is gone. If it was renamed, add "
                             f"was: [{player_id}] to it; if it was removed, add it to the platform's retired:")
        for player_id in new_players.keys() - old_players.keys():
            changes.append(f"{new['id']}: new player {player_id}")
        for player_id in new_players.keys() & old_players.keys():
            if new_players[player_id] != old_players[player_id]:
                changes.append(f"{new['id']}: {player_id} changed")
        if [p for p in old_players if p in new_players] != [p for p in new_players if p in old_players]:
            changes.append(f"{new['id']}: players reordered")
        old_rest = {k: v for k, v in old.items() if k != "players"}
        new_rest = {k: v for k, v in new.items() if k != "players"}
        if old_rest != new_rest:
            changes.append(f"{new['id']}: platform details changed")
    return found, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous")
    args = parser.parse_args()

    retroarch, docs = load()
    names = json.load(open(os.path.join(TOOLS, "cocoon.json")))
    found = problems(retroarch, docs, names)
    changes = []
    catalogue = None
    if not found:
        try:
            catalogue = build(retroarch, docs)
        except (KeyError, TypeError, ValueError, StopIteration) as error:
            found.append(f"couldn't build the catalogue: {error!r}")
    if catalogue:
        owner = {}
        for platform in catalogue["platforms"]:
            for player in platform["players"]:
                if player["id"] in owner:
                    found.append(f"{platform['id']}: player ID {player['id']} is also used on {owner[player['id']]}")
                owner.setdefault(player["id"], platform["id"])
        patterns = {p["acceptedFilenameRegex"] for p in catalogue["platforms"]}
        patterns |= {pl["acceptedFilenameRegex"] for p in catalogue["platforms"] for pl in p["players"]
                     if "acceptedFilenameRegex" in pl}
        found += [f"file pattern {line}" for line in bad_patterns(sorted(patterns))]
        if args.previous and os.path.exists(args.previous):
            more, changes = compare(json.load(open(args.previous)), catalogue, docs)
            found += more

    if catalogue:
        players = sum(len(p["players"]) for p in catalogue["platforms"])
        print(f"{len(catalogue['platforms'])} platforms, {players} players.")
    if changes:
        print("\nChanges from the published catalogue:")
        print("\n".join(f"- {c}" for c in changes))
    if found:
        print(f"\n{len(found)} problems:")
        print("\n".join(f"- {f}" for f in found))
        sys.exit(1)


if __name__ == "__main__":
    main()
