import json
import os
import re
import subprocess

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
ANDROID = os.path.join(ROOT, "android")

ACTIONS = {"view": "android.intent.action.VIEW", "main": "android.intent.action.MAIN"}
CATEGORIES = {"default": "android.intent.category.DEFAULT", "launcher": "android.intent.category.LAUNCHER"}
FLAGS = {
    "clear-task": "--activity-clear-task",
    "clear-top": "--activity-clear-top",
    "no-history": "--activity-no-history",
    "new-task": "--activity-new-task",
    "grant-read": "--grant-read-uri-permission",
}
TYPED_EXTRAS = {"bool": "--ez", "int": "--ei", "long": "--el", "uri": "--eu", "list": "--esa", "ints": "--eia"}
ANY_FILE = r"^(?!(?:\._|\.).*).*$"

PLATFORM_KEYS = {"name", "description", "was", "idPrefix", "ignore", "regex", "folders", "cocoon", "scrape",
                 "storefronts", "extra", "retroarch", "players", "retired"}
COCOON_KEYS = {"icon", "folder"}
SCRAPE_KEYS = {"screenscraper", "igdb", "launchbox", "arcade", "retroachievements", "retroachievementsName",
               "libretro", "thegamesdb", "arcadeitalia", "order"}
PLAYER_KEYS = {"name", "id", "was", "app", "action", "category", "game", "data", "type", "files", "regex",
               "extras", "flags", "resumes", "extra", "am"}
CORE_KEYS = {"name", "id", "builds", "files", "launch", "activity", "extras", "flags"}
GROUP_KEYS = CORE_KEYS | {"retroarch"}
RETROARCH_KEYS = {"builds", "activity", "launches", "cores"}


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def load(directory=ANDROID):
    paths = sorted(os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".yaml"))
    result = subprocess.run(["ruby", os.path.join(TOOLS, "yaml_to_json.rb"), *paths],
                            capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr.strip())
    docs = json.loads(result.stdout)
    return docs.pop("retroarch"), docs


def files_regex(files):
    return r"^(.*)\.(?:" + "|".join(str(ext).replace(".", r"\.") for ext in files) + r")$"


def ignore_regex(ignore):
    if not ignore:
        return ANY_FILE
    return r"^(?!(?:\._|\.).*).*(?<!" + "|".join(ignore) + r")$"


def extra_line(key, value):
    if isinstance(value, dict):
        (kind, raw), = value.items()
        if kind == "bool":
            text = "true" if raw is True else "false" if raw is False else str(raw)
        elif kind in ("list", "ints"):
            text = ",".join(str(v) for v in raw)
        else:
            text = str(raw)
        return f"{TYPED_EXTRAS[kind]} {key} {text}"
    return f"-e {key} {'' if value is None else value}".rstrip()


def app_lines(player):
    if "am" in player:
        return [line.strip() for line in player["am"].split("\n") if line.strip()]
    lines = [f"-n {player['app']}"]
    game, action, data, game_extra = player.get("game"), player.get("action"), player.get("data"), None
    if game in ("uri", "path"):
        data = "{file.%s}" % game
        if action is None:
            action = "view"
    elif isinstance(game, dict):
        game_extra = (game["extra"], "{file.uri}" if game.get("as") == "uri" else "{file.path}")
    if action and action != "none":
        lines.append(f"-a {ACTIONS.get(action, action)}")
    for category in as_list(player.get("category")):
        lines.append(f"-c {CATEGORIES.get(category, category)}")
    if data is not None:
        lines.append(f"-d {data}")
    if "type" in player:
        lines.append(f"-t {player['type']}")
    if game_extra:
        lines.append(f"-e {game_extra[0]} {game_extra[1]}")
    for key, value in (player.get("extras") or {}).items():
        lines.append(extra_line(key, value))
    for flag in player.get("flags") or []:
        lines.append(FLAGS[flag])
    return lines


def app_player(item, prefix):
    player = {"id": item.get("id") or f"{prefix}.{item['app'].split('/', 1)[0]}", "name": item["name"]}
    if item.get("was"):
        player["was"] = as_list(item["was"])
    regex = item.get("regex") or (files_regex(item["files"]) if "files" in item else None)
    if regex:
        player["acceptedFilenameRegex"] = regex
    player["amStartArguments"] = "\n".join(app_lines(item))
    extra = dict(item.get("extra") or {})
    if item.get("resumes") is False:
        extra["cantResume"] = True
    if extra:
        player["extra"] = extra
    return player


def core_settings(core, retroarch, *layers):
    default = retroarch["cores"][core]
    settings = {"name": core, "id": core, "builds": list(retroarch["builds"]), "launch": "standard"}
    settings.update(default if isinstance(default, dict) else {"files": default})
    for layer in layers:
        settings.update(layer or {})
    return settings


def retroarch_players(item, prefix, platform_cores, retroarch):
    group = {k: v for k, v in item.items() if k != "retroarch"}
    cores = []
    for entry in as_list(item["retroarch"]):
        core, inline = next(iter(entry.items())) if isinstance(entry, dict) else (entry, {})
        cores.append((core, core_settings(core, retroarch, platform_cores.get(core), group, inline)))
    players = []
    for build, about in retroarch["builds"].items():
        for core, s in cores:
            if build not in s["builds"]:
                continue
            app = about["app"]
            extras = dict(retroarch["launches"][s["launch"]]["extras"])
            for key, value in (s.get("extras") or {}).items():
                if value is None:
                    extras.pop(key, None)
                else:
                    extras[key] = value
            lines = [f"-n {app}/{s.get('activity', retroarch['activity'])}"]
            lines += [f"-e {k} {str(v).replace('{app}', app).replace('{core}', core)}".rstrip() for k, v in extras.items()]
            lines += [FLAGS[f] for f in s.get("flags", retroarch["launches"][s["launch"]]["flags"])]
            players.append({
                "id": f"{prefix}.{build}.{s['id']}",
                "name": f"{about['name']} - {s['name']}",
                "acceptedFilenameRegex": files_regex(s["files"]),
                "amStartArguments": "\n".join(lines),
            })
    return players


def expand(platform_id, doc, retroarch):
    prefix = doc.get("idPrefix", platform_id)
    players = []
    for item in doc.get("players") or []:
        if "retroarch" in item:
            players += retroarch_players(item, prefix, doc.get("retroarch") or {}, retroarch)
        else:
            players.append(app_player(item, prefix))
    scrape = doc.get("scrape") or {}
    extra = dict(doc.get("extra") or {})
    if "folders" in doc:
        extra["folderAliases"] = doc["folders"]
    if "storefronts" in doc:
        extra["pcStorefronts"] = doc["storefronts"]
    platform = {"id": platform_id, "name": doc["name"]}
    if doc.get("description"):
        platform["description"] = doc["description"]
    platform["acceptedFilenameRegex"] = doc.get("regex") or ignore_regex(doc.get("ignore"))
    if scrape.get("retroachievements") is not None:
        platform["retroAchievementsConsoleIds"] = as_list(scrape["retroachievements"])
    if extra:
        platform["extra"] = extra
    if doc.get("was"):
        platform["was"] = as_list(doc["was"])
    platform["cocoon"] = doc.get("cocoon") or {}
    if scrape:
        platform["scrape"] = scrape
    platform["players"] = players
    return platform


def build(retroarch, docs):
    return {"format": 1, "platforms": [expand(pid, docs[pid], retroarch) for pid in sorted(docs)]}


# Checks


def problems(retroarch, docs, names):
    found = []

    def unknown(where, value, allowed):
        if not isinstance(value, dict):
            found.append(f"{where}: expected a mapping")
            return
        for key in value:
            if key not in allowed:
                found.append(f"{where}: unknown field {key}")

    def strings(where, value):
        if not isinstance(value, list) or not all(isinstance(v, str) and v for v in value):
            found.append(f"{where}: expected a list of names")

    def check_extras(where, extras):
        if not isinstance(extras, dict):
            found.append(f"{where}: expected a mapping")
            return
        for key, value in extras.items():
            if isinstance(value, dict):
                if len(value) != 1 or next(iter(value)) not in TYPED_EXTRAS:
                    found.append(f"{where} > {key}: a typed extra is one of {', '.join(TYPED_EXTRAS)}")
            elif value is not None and not isinstance(value, (str, int)):
                found.append(f"{where} > {key}: expected text")

    def check_flags(where, flags):
        for flag in as_list(flags):
            if flag not in FLAGS:
                found.append(f"{where}: unknown flag {flag}")

    unknown("retroarch", retroarch, RETROARCH_KEYS)
    builds = retroarch.get("builds") or {}
    launches = retroarch.get("launches") or {}
    cores = retroarch.get("cores") or {}
    for core, value in cores.items():
        if isinstance(value, dict):
            unknown(f"retroarch > cores > {core}", value, CORE_KEYS)
            if "files" not in value:
                found.append(f"retroarch > cores > {core}: needs files")
        else:
            strings(f"retroarch > cores > {core}", value)

    def check_core(where, settings):
        unknown(where, settings, GROUP_KEYS)
        for build in as_list(settings.get("builds")):
            if build not in builds:
                found.append(f"{where}: unknown build {build}")
        if "launch" in settings and settings["launch"] not in launches:
            found.append(f"{where}: unknown launch {settings['launch']}")
        if "files" in settings:
            strings(f"{where} > files", settings["files"])
        if "extras" in settings:
            check_extras(f"{where} > extras", settings["extras"])
        check_flags(where, settings.get("flags"))

    for pid, doc in docs.items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", pid):
            found.append(f"{pid}: file names are lower-case letters, digits and dashes")
        unknown(pid, doc, PLATFORM_KEYS)
        if not isinstance(doc, dict):
            continue
        if not isinstance(doc.get("name"), str) or not doc["name"]:
            found.append(f"{pid}: needs a name")
        cocoon = doc.get("cocoon") or {}
        unknown(f"{pid} > cocoon", cocoon, COCOON_KEYS)
        if "icon" in cocoon and cocoon["icon"] not in names["icons"]:
            found.append(f"{pid}: Cocoon has no icon called {cocoon['icon']}")
        folder = cocoon.get("folder")
        if isinstance(folder, list):
            if len(folder) != 2 or not all(re.fullmatch(r"#[0-9A-Fa-f]{6}", str(c)) for c in folder):
                found.append(f"{pid}: a folder gradient is two colours like \"#86A7FD\"")
        elif folder is not None and folder not in names["folders"]:
            found.append(f"{pid}: Cocoon has no folder colour called {folder}")
        if "scrape" in doc:
            unknown(f"{pid} > scrape", doc["scrape"], SCRAPE_KEYS)
        for key in ("was", "ignore", "folders", "retired"):
            if key in doc:
                strings(f"{pid} > {key}", as_list(doc[key]))
        for core, settings in (doc.get("retroarch") or {}).items():
            if core not in cores:
                found.append(f"{pid} > retroarch: {core} isn't in retroarch.yaml")
            check_core(f"{pid} > retroarch > {core}", settings)
        players = doc.get("players")
        if not isinstance(players, list):
            found.append(f"{pid}: needs a list of players")
            continue
        for i, item in enumerate(players, 1):
            where = f"{pid} > players > {i}"
            if not isinstance(item, dict):
                found.append(f"{where}: expected a mapping")
                continue
            if "retroarch" in item:
                check_core(where, {k: v for k, v in item.items()})
                for entry in as_list(item["retroarch"]):
                    core, inline = next(iter(entry.items())) if isinstance(entry, dict) else (entry, {})
                    if core not in cores:
                        found.append(f"{where}: {core} isn't in retroarch.yaml")
                    if inline:
                        check_core(f"{where} > {core}", inline)
                continue
            unknown(where, item, PLAYER_KEYS)
            if not isinstance(item.get("name"), str) or not item["name"]:
                found.append(f"{where}: needs a name")
            if ("app" in item) == ("am" in item):
                found.append(f"{where}: needs either app or am")
            if "am" in item and "id" not in item:
                found.append(f"{where}: a player written with am needs an id")
            if "app" in item and not re.fullmatch(r"[\w.]+/[\w.$]+", str(item["app"])):
                found.append(f"{where}: app is package/activity")
            game = item.get("game")
            if game is not None and game not in ("uri", "path") and not (
                    isinstance(game, dict) and isinstance(game.get("extra"), str) and set(game) <= {"extra", "as"}):
                found.append(f"{where}: game is uri, path or {{ extra: KEY }}")
            if "files" in item:
                strings(f"{where} > files", item["files"])
            if "extras" in item:
                check_extras(f"{where} > extras", item["extras"])
            check_flags(where, item.get("flags"))
            if "resumes" in item and item["resumes"] is not False:
                found.append(f"{where}: resumes only takes no")
    return found
