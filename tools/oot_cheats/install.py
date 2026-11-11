#!/usr/bin/env python3
"""Install the optional OoT cheat VM menu into an Eritchii data directory.

The game-specific executable is downloaded only when this script is run. It is
not part of the emulator and must match the supported game build ID.
"""

import argparse
import hashlib
import io
from pathlib import Path
import sys
import urllib.request
import zipfile


TITLE_ID = "0400486024DEC000"
BUILD_ID = "E0F3CCFAF50065AE"
RELEASE_URL = (
    "https://github.com/tomvita/MyNXCheats/releases/download/0400486024DEC000/"
    "OoT_cheatvm_E0F3CCFAF50065AE.zip"
)
RELEASE_SHA256 = "0cc0c0c60d401c4c9ef3b2190f3f4cd8626514c68f971eb393abba675df39164"
MAX_DOWNLOAD_SIZE = 5 * 1024 * 1024
FILES = (
    f"load/{TITLE_ID}/cheatvm/exefs/subsdk9",
    f"sdmc/atmosphere/contents/{TITLE_ID}/cheats/{BUILD_ID}.txt",
)


def get_archive(archive_path: Path | None) -> bytes:
    if archive_path is not None:
        if archive_path.stat().st_size > MAX_DOWNLOAD_SIZE:
            raise ValueError("The archive exceeds the expected download size")
        archive = archive_path.read_bytes()
    else:
        request = urllib.request.Request(RELEASE_URL, headers={"User-Agent": "Eritchii-OoT-cheats"})
        with urllib.request.urlopen(request, timeout=45) as response:
            archive = response.read(MAX_DOWNLOAD_SIZE + 1)

    if len(archive) > MAX_DOWNLOAD_SIZE:
        raise ValueError("The archive exceeds the expected download size")
    if hashlib.sha256(archive).hexdigest() != RELEASE_SHA256:
        raise ValueError("Unexpected archive checksum; release content may have changed")
    return archive


def selected_files(archive: bytes) -> dict[str, bytes]:
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        result = {}
        for name in FILES:
            entry = bundle.getinfo(name)
            if entry.is_dir() or entry.file_size > MAX_DOWNLOAD_SIZE:
                raise ValueError(f"Invalid file in release archive: {name}")
            data = bundle.read(entry)
            if len(data) != entry.file_size:
                raise ValueError(f"Incomplete file in release archive: {name}")
            result[name] = data
    return result


def verify_root(root: Path) -> Path:
    if not root.is_dir():
        raise ValueError(f"The emulator data folder does not exist: {root}")
    if not any((root / part).is_dir() for part in ("config", "nand", "load", "sdmc")):
        raise ValueError("Choose the emulator's Root Data Folder (containing config, nand, load or sdmc)")
    return root.resolve()


def install(root: Path, content: dict[str, bytes], dry_run: bool = False) -> list[Path]:
    """Never replace an existing mod or user's cheat file."""
    root = verify_root(root)
    targets = [(root / name, content[name]) for name in FILES]

    for target, data in targets:
        if not target.resolve().is_relative_to(root):
            raise ValueError(f"A destination points outside the data folder: {target}")
        if target.exists() and (not target.is_file() or target.read_bytes() != data):
            raise FileExistsError(f"A different file already exists; nothing was replaced: {target}")

    if dry_run:
        return [target for target, _ in targets]

    created = []
    try:
        for target, data in targets:
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.resolve().is_relative_to(root):
                raise ValueError(f"A destination points outside the data folder: {target}")
            with target.open("xb") as file:
                created.append(target)
                file.write(data)
    except Exception:
        for target in created:
            target.unlink(missing_ok=True)
        raise
    return [target for target, _ in targets]


def main() -> int:
    parser = argparse.ArgumentParser(description="Install a third-party OoT in-game cheat menu")
    parser.add_argument("--root", required=True, type=Path, help="Eritchii Root Data Folder")
    parser.add_argument("--archive", type=Path, help="Previously downloaded release ZIP (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Check destinations without writing")
    args = parser.parse_args()

    try:
        content = selected_files(get_archive(args.archive))
        targets = install(args.root, content, args.dry_run)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        print(f"OoT cheats: {error}", file=sys.stderr)
        return 1

    action = "Would install" if args.dry_run else "Installed or already present"
    print(f"{action}:")
    for target in targets:
        print(f"  {target}")
    if not args.dry_run:
        print("Restart the game, then hold L+R and press D-pad Down for the cheat menu.")
        print("All cheats start off. Use only on OoT TID 0400486024DEC000, BID E0F3CCFAF50065AE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
