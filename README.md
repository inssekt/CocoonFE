# Cocoon

<div align="center">

![Banner](banner.png)

**A Modern Emulation Frontend for Android**

[![Platform](https://img.shields.io/badge/platform-Android-green.svg)](https://www.android.com/)
![Discord](https://img.shields.io/discord/1445504354563002429)


*An emulation frontend inspired by the 3DS UI built for single and dual screen Android devices*

[Features](#features) • [Installation](#installation) • [Setup](#setup)

</div>

---

## Features

### Multi-Platform Game Library
- **Universal Emulator Support**: Works with any Android emulator (RetroArch, Dolphin, PPSSPP, and more)
- **100+ Platform Support**: Nintendo (NES, SNES, N64, GameCube, Wii, Switch), PlayStation (1-4), Sega (Genesis, Saturn, Dreamcast), Xbox, Arcade, and more
- **Smart Organization**: Automatically categorizes games by platform with intelligent folder detection

### Beautiful UI & Visuals
- **Rich Artwork**: Automatically fetches icons, logos, and hero images from SteamGridDB
- **Smooth Animations**: Fluid transitions and responsive interactions
- **Adaptive game grid with zoom feature**: just like the 3DS!

### Automatic Metadata Scraping
- **Hash-Based ROM Identification**: Uses CRC32, MD5, and SHA1 for accurate game matching
- **ScreenScraper.fr Integration**: 
  - Comprehensive game metadata (title, description, release date, genres)
  - Developer and publisher information
  - User ratings and classifications
  - Multiple regions support
  - Works with guest API (no account required) or authenticated for faster access
- **SteamGridDB Artwork**: High-quality game artwork in multiple styles
- **Batch Processing**: Scrape entire libraries with progress tracking

### Advanced Display Features

![Banner](screen_swap.gif)

- **External Display Support**: Display game information and launch games to an external display
- **Display Management**: 
  - Automatic external display detection
  - Seamless game launching to secondary displays
  - External display overlay with game info
- **Live screen-swapping**: Seamlessly switch between screen roles with a button

### Powerful Configuration
- **Per-Platform Settings**: 
  - Custom emulator app/player selection
  - Multiple ROM folder paths per platform
- **Appearance Customization**:
  - Customize library layout
  - Icon image size adjustment

---

## Installation
[<img src="https://raw.githubusercontent.com/ImranR98/Obtainium/refs/heads/main/assets/graphics/badge_obtainium.png"
     alt="Get it on Obtainium"
     height="55"
     style="border: 13px solid transparent;">](https://apps.obtainium.imranr.dev/redirect?r=obtainium://app/{%22id%22%3A%22rip.moth.cocoon%22%2C%22url%22%3A%22https%3A%2F%2Fgithub.com%2Finssekt%2FCocoonFE%22%2C%22author%22%3A%22inssekt%22%2C%22name%22%3A%22CocoonFE%22%2C%22preferredApkIndex%22%3A0%2C%22additionalSettings%22%3A%22{\%22includePrereleases\%22%3Atrue%2C\%22fallbackToOlderReleases\%22%3Atrue%2C\%22filterReleaseTitlesByRegEx\%22%3A\%22\%22%2C\%22filterReleaseNotesByRegEx\%22%3A\%22\%22%2C\%22verifyLatestTag\%22%3Afalse%2C\%22sortMethodChoice\%22%3A\%22date\%22%2C\%22useLatestAssetDateAsReleaseDate\%22%3Afalse%2C\%22releaseTitleAsVersion\%22%3Afalse%2C\%22trackOnly\%22%3Afalse%2C\%22versionExtractionRegEx\%22%3A\%22\%22%2C\%22matchGroupToUse\%22%3A\%22\%22%2C\%22versionDetection\%22%3Atrue%2C\%22releaseDateAsVersion\%22%3Afalse%2C\%22useVersionCodeAsOSVersion\%22%3Afalse%2C\%22apkFilterRegEx\%22%3A\%22\%22%2C\%22invertAPKFilter\%22%3Afalse%2C\%22autoApkFilterByArch\%22%3Atrue%2C\%22appName\%22%3A\%22\%22%2C\%22appAuthor\%22%3A\%22\%22%2C\%22shizukuPretendToBeGooglePlay\%22%3Afalse%2C\%22allowInsecure\%22%3Afalse%2C\%22exemptFromBackgroundUpdates\%22%3Afalse%2C\%22skipUpdateNotifications\%22%3Afalse%2C\%22about\%22%3A\%22\%22%2C\%22refreshBeforeDownload\%22%3Afalse%2C\%22includeZips\%22%3Afalse%2C\%22zippedApkFilterRegEx\%22%3A\%22\%22}%22%2C%22overrideSource%22%3Anull}%0A%0A)

### Download
1. Download the latest APK from [Releases](https://github.com/inssekt/CocoonFE/releases)
2. Enable "Install from Unknown Sources" in Android settings
3. Install the APK

---

## 🎯 Setup

### First-Time Setup Wizard

---

## Setups (Optional but recommended):
   - **SteamGridDB**: Get artwork for your games
     - Visit [steamgriddb.com/profile/preferences/api](https://www.steamgriddb.com/profile/preferences/api)
     - Create an API key
   - **ScreenScraper.fr**: Get game metadata
     - Register at [screenscraper.fr](https://www.screenscraper.fr/)
     - Optional - works with guest API without login

2. **Organization Mode**:
   - **Smart Folders** (Recommended): Cocoon auto-detects platforms and creates smart folders from which you can create homescreen shortcuts
   - **Manual Mode**: Cocoon puts all detected ROMs onto your homescreen to be organised yourself (Smart Folders can still be manually created)

3. **ROM Folders**:
   - Browse to your ROM root folder
   - Cocoon will scan for games automatically with optional subfolder scanning

---


The complete platform list is available in [platforms.json](platforms.json).

---


## Support

For bug reports and feature requests, please use [GitHub Issues](https://github.com/inssekt/CocoonFE/issues) or [Join our Discord](https://discord.gg/ytWHjRuKdS).

---

## Acknowledgments

- **ScreenScraper.fr**: Game metadata and ROM information
- **SteamGridDB**: High-quality game artwork
- **Daijisho**: A great curated collection of platforms & players that we use as a base
