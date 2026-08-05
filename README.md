# Cocoon Shell

<div align="center">

[![Cocoon 3 banner](https://cocoon-shell.com/images/news/3.0/banner.webp)](https://cocoon-shell.com/news/cocoon-3/)

**A customisable Android frontend for retro gaming handhelds.**

[![Platform](https://img.shields.io/badge/platform-Android-green.svg)](https://www.android.com/)
[![Discord](https://img.shields.io/discord/1445504354563002429)](https://discord.gg/cocoon)

[Download](https://github.com/inssekt/CocoonFE/releases/latest) · [Wiki](https://cocoon-shell.com/wiki/) · [Themes](https://cocoon-shell.com/themes/) · [News](https://cocoon-shell.com/news/) · [Feedback](https://github.com/inssekt/CocoonFE/discussions)

</div>

## About

Cocoon is an emulation frontend (similar to EmulationStation & Pegasus) which acts as an application to organise your library and launch games through Emulators. Cocoon is not an emulator, not a device, and does not contain any copyrighted material at all.

Our current scope is strictly for Android.

<p align="center">
  <img src="https://cocoon-shell.com/images/news/3.0/preview1.webp" alt="Cocoon 3 home screen in light mode" width="49%">
  <img src="https://cocoon-shell.com/images/news/3.0/preview2.webp" alt="Cocoon 3 home screen in dark mode" width="49%">
</p>

## Features

### Library and Layout

- **Customisable grid:** Each zoom level has its own saved layout. Page Mode provides a fixed grid made from discrete, swipeable pages, with control over the number of rows and columns.
- **Widgets:** Place Cocoon’s clock, Recently Played, Last Played, music player, image pin, Picnic, Log, and Random Game widgets alongside your games, or use a native Android widget from any app.
- **Single and dual screen:** Single-row layouts are available in Standard, Carousel, and Cover Flow styles. Cocoon supports single and dual-screen devices including the AYN Thor, Anbernic RG DS, and AYANEO Pocket DS.
- **External displays:** Cocoon moves cleanly between single and dual-screen layouts, and a docked setup can use up to five rows to make the most of the larger display.
- **Search and organisation:** Search the game library, multi-select games, and bulk move or remove them. Games can live in multiple folders through shortcuts.

### Game Details and Play

- **Game info:** The info screen has three tabs: Game Info, Achievements, and Activity Log. Game Info includes a description, gameplay or trailer video, screenshots, and HowLongToBeat badges.
- **Achievements:** The Achievements tab shows recently earned RetroAchievements, completion progress, and Steam achievements.
- **Activity:** The Activity Log tab breaks your tracked playtime into useful stats and a graph of your playing habits throughout the week.
- **Now Playing:** On dual-screen devices, Now Playing displays game art, session info, and quick access to the dock.
- **Sessions:** Cocoon tracks playtime down to the second. Sessions pause when Cocoon loses focus of the game and resume automatically when the game comes back into focus.

### Tools and Integrations

- **Pods:** Pods are mini apps for single and dual-screen devices. Log tracks playtime and game statistics, while Picnic organises screenshots by game.
- **Scraping:** Scraping sources include LaunchBox, IGDB, HowLongToBeat, ScreenScraper, and SteamGridDB. Sources can be arranged by priority, with control over the included media types.
- **Status and social:** Quickly toggle Wi-Fi, Bluetooth, Do Not Disturb, and more without leaving Cocoon. You can see Discord friends and their game activity, Steam friends with game activity and messages, plus Android conversations from Discord and any other supported messaging app.

<p align="center">
  <img src="https://cocoon-shell.com/images/news/3.0/hltbgameinfo.webp" alt="Game info tab with HowLongToBeat times, screenshots, and game details" width="32%">
  <img src="https://cocoon-shell.com/images/news/3.0/achievementstab.webp" alt="Recent achievements shown beside the selected game" width="32%">
  <img src="https://cocoon-shell.com/images/news/3.0/logtab.webp" alt="Activity Log tab showing playtime and a weekly graph" width="32%">
</p>

## Themes

Silk Pod is Cocoon’s community theme and asset store. Browse, download, and install themes and asset packs made by other users, or submit your own.

Themes are modular and dynamically loaded. Choose individual colours, wallpapers, icons, smart folder artwork, sound effects, and music from different themes to create your own combination.

The [Theme Studio](https://cocoon-shell.com/themes/create/) provides a live dual-screen preview and exports ready-to-use ZIPs for Cocoon or Silk Pod. The Glass surface material includes controls for blur, refraction, tint, and rim highlight.

<p align="center">
  <img src="https://cocoon-shell.com/images/news/3.0/silk2.webp" alt="Browsing and previewing a theme in Silk Pod" width="70%">
</p>

## Installation

[<img src="https://raw.githubusercontent.com/ImranR98/Obtainium/refs/heads/main/assets/graphics/badge_obtainium.png" alt="Get it on Obtainium" height="55">](https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/%7B%22id%22%3A%22rip.moth.cocoonshell%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2Finssekt%2FCocoonFE%22%2C%22author%22%3A%22inssekt%22%2C%22name%22%3A%22CocoonFE%22%2C%22preferredApkIndex%22%3A0%2C%22additionalSettings%22%3A%22%7B%5C%22includePrereleases%5C%22%3Atrue%2C%5C%22fallbackToOlderReleases%5C%22%3Atrue%2C%5C%22filterReleaseTitlesByRegEx%5C%22%3A%5C%22%5C%22%2C%5C%22filterReleaseNotesByRegEx%5C%22%3A%5C%22%5C%22%2C%5C%22verifyLatestTag%5C%22%3Afalse%2C%5C%22sortMethodChoice%5C%22%3A%5C%22date%5C%22%2C%5C%22useLatestAssetDateAsReleaseDate%5C%22%3Afalse%2C%5C%22releaseTitleAsVersion%5C%22%3Afalse%2C%5C%22trackOnly%5C%22%3Afalse%2C%5C%22versionExtractionRegEx%5C%22%3A%5C%22%5C%22%2C%5C%22matchGroupToUse%5C%22%3A%5C%22%5C%22%2C%5C%22versionDetection%5C%22%3Atrue%2C%5C%22releaseDateAsVersion%5C%22%3Afalse%2C%5C%22useVersionCodeAsOSVersion%5C%22%3Afalse%2C%5C%22apkFilterRegEx%5C%22%3A%5C%22%5C%22%2C%5C%22invertAPKFilter%5C%22%3Afalse%2C%5C%22autoApkFilterByArch%5C%22%3Atrue%2C%5C%22appName%5C%22%3A%5C%22%5C%22%2C%5C%22appAuthor%5C%22%3A%5C%22inssekt%5C%22%2C%5C%22about%5C%22%3A%5C%22%5C%22%2C%5C%22refreshBeforeDownload%5C%22%3Afalse%2C%5C%22includeZips%5C%22%3Afalse%2C%5C%22zippedApkFilterRegEx%5C%22%3A%5C%22%5C%22%7D%22%2C%22overrideSource%22%3Anull%7D)

### Manual Installation

1. Download the latest APK from [Releases](https://github.com/inssekt/CocoonFE/releases/latest).
2. Enable **Install from Unknown Sources** in Android settings.
3. Install the APK.

## Setup

The setup wizard walks you through everything you need to get up and running.

See the [Cocoon Wiki](https://cocoon-shell.com/wiki/) for setup guides. The complete platform list is available in [platforms/index.json](platforms/index.json).

## Resources

- [Cocoon website](https://cocoon-shell.com/)
- [Latest release](https://github.com/inssekt/CocoonFE/releases/latest)
- [Documentation and setup guides](https://cocoon-shell.com/wiki/)
- [Themes and asset packs](https://cocoon-shell.com/themes/)
- [Release news](https://cocoon-shell.com/news/)

## Support

For bug reports and feature requests, please use [GitHub Discussions](https://github.com/inssekt/CocoonFE/discussions). For general help and community chat, [join our Discord](https://discord.gg/cocoon).

## Acknowledgments

- **ScreenScraper.fr:** Game metadata and ROM information
- **SteamGridDB:** High-quality game artwork
- **Daijisho:** A great curated collection of platforms and players that we use as a base
