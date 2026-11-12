# Ocarina of Time (Switch 2): optional in-game cheats

The game's built-in mod support can load a third-party cheat VM without modifications to the emulator's executable. This is **not** the full Hookshot Debug menu: it currently offers **No damage**, **Refill hearts**, **Max hearts 20**, and **ZL slow descend / ZL+X moon jump**. Its in-game menu lets you toggle these during play.

The code and menus in [NotRexed/Hookshot](https://github.com/NotRexed/Hookshot) are for a native PC recompilation, not for the emulated game. Copying its `vk_menu.cpp` or `hos_main.c` into Eritchii would not make those game hooks work. The remaining tools (noclip flight, teleport, changing Link's age, inventory and world time, free camera) require separate game-specific runtime patches.

## Supported game build

- Game: *The Legend of Zelda: Ocarina of Time* (Switch 2 remake)
- Title ID: `0400486024DEC000`
- **Main Build ID: `E0F3CCFAF50065AE`** (full: `E0F3CCFAF50065AE4EA01EB5AEB13B1A45DA3348`)

Do **not** install this pack for another build. Confirm the Build ID in the emulator's log before proceeding. Back up your game save. This third-party pack was reported tested on Lichii `nx2` for Windows, but has not been independently tested on Eritchii.

## Installation

1. In Eritchii, open **File > Open Lichii Folders > Root Data Folder** (the wording might differ by build). This folder contains `load`, `sdmc`, `nand`, or `config`. For a portable installation it is typically `user` next to the executable; otherwise use the menu to find the actual directory.
2. With Python 3.9+ installed, run from the source checkout:

   ```powershell
   python tools/oot_cheats/install.py --root "C:\path\to\your\emulator\data"
   ```

   On Linux, use `python3` and the relevant data directory. `--dry-run` checks the destinations, and `--archive path/to/OoT_cheatvm_E0F3CCFAF50065AE.zip` uses a previously downloaded ZIP.
3. Restart the game. Under **Configure Game > Add-ons**, make sure `cheatvm` is enabled.
4. While playing, hold **L + R** and press **D-pad Down**. Use A to toggle a cheat and B to go back. All cheats start off; your selections are remembered.

The installer downloads only the [specific release](https://github.com/tomvita/MyNXCheats/releases/tag/0400486024DEC000) of the optional third-party menu, verifies its SHA-256 checksum, and copies exactly two files to the emulator's data folder:

```
load/0400486024DEC000/cheatvm/exefs/subsdk9
sdmc/atmosphere/contents/0400486024DEC000/cheats/E0F3CCFAF50065AE.txt
```

It never overwrites existing files. If you have a different `subsdk9` module or existing cheats, inspect those first; do not overwrite them automatically. Do **not** also install the cheat TXT inside `load/.../cheats/`, because it could run twice (through the module and through the emulator's built-in cheat engine).

For extracted games launched through their `main` file, see the release's `README.txt`: the emulator may not apply `load` mods to that format.

To remove the menu, first close the game, then remove only `load/0400486024DEC000/cheatvm/` and, if desired, the `E0F3CCFAF50065AE.txt` file above. Keep your save backups.

## Source and licence

- Hookshot Debug tools: [NotRexed/Hookshot](https://github.com/NotRexed/Hookshot), GPL-3.0.
- Cheat pack and module: [tomvita/MyNXCheats release](https://github.com/tomvita/MyNXCheats/releases/tag/0400486024DEC000). The module is GPLv2 and the release includes its source code. The pack is downloaded only at the user's request, not bundled into Eritchii.

The installer has game-free tests: `python tools/oot_cheats/test_install.py`.
