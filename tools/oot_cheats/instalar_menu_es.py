#!/usr/bin/env python3
"""Instala sloperinaGZ y traduccion al espanol en OoT Switch 2 / Eritchii.

No modifica lichii.exe, ni la partida, ni otros mods desconocidos. Conserva una
copia recuperable del cheatVM anterior. Usa solo una version verificada del mod.
"""
from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import shutil
import sys
import urllib.request
import zipfile

TITLE = '0400486024DEC000'
BUILDS = (
    '33FA6C2C23848282A77E8B88A0A93F4887C55920',
    'E0F3CCFAF50065AE4EA01EB5AEB13B1A45DA3348',
)
RELEASE = 'v0.0.4.1'
URL = f'https://github.com/PracticeROM/sloperina/releases/download/{RELEASE}/sloperinaGZ-0.0.4.1.zip'
EXPECTED_SHA = '7c119938897e4ecd84c974148caf46855eccce3b93f4ac5df94d483fa3cc3e75'
MAX_ZIP = 4 * 1024 * 1024
MOD_NAME = 'sloperinaGZ'


def verify_root(root: Path) -> Path:
    if not root.is_dir() or not any((root / x).is_dir() for x in ('load', 'sdmc', 'nand', 'config')):
        raise ValueError('Debes indicar Root Data Folder (carpeta que contiene load, sdmc o nand).')
    return root.resolve()


def archive_bytes(local: Path | None) -> bytes:
    if local:
        if not local.is_file() or local.stat().st_size > MAX_ZIP:
            raise ValueError('Archivo ZIP local inexistente o demasiado grande.')
        data = local.read_bytes()
    else:
        req = urllib.request.Request(URL, headers={'User-Agent': 'Eritchii-Menu-ES/1.0'})
        with urllib.request.urlopen(req, timeout=50) as resp:
            data = resp.read(MAX_ZIP + 1)
    if len(data) > MAX_ZIP or hashlib.sha256(data).hexdigest() != EXPECTED_SHA:
        raise ValueError('La descarga no coincide con el SHA-256 de sloperinaGZ 0.0.4.1.')
    return data


def read_mod_files(data: bytes) -> dict[str, bytes]:
    wanted = ('subsdk9', *(f'{x}.ips' for x in BUILDS))
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        found = {}
        for name in wanted:
            matches = [info for info in z.infolist() if not info.is_dir() and
                       (info.filename == f'files/{name}' or info.filename.endswith(f'/files/{name}'))]
            if len(matches) != 1 or matches[0].file_size > MAX_ZIP:
                raise ValueError(f'El ZIP no contiene un archivo valido: files/{name}')
            found[name] = z.read(matches[0])
        return found


def check_no_conflicts(root: Path, mod_files: dict[str, bytes]) -> tuple[Path, Path, Path]:
    mods_root = root / 'load' / TITLE
    mod = mods_root / MOD_NAME
    prev = mods_root / 'cheatvm'
    backup = root / 'eritchii_oot_copias' / 'cheatvm_anterior'
    if prev.exists() and backup.exists():
        raise FileExistsError('Hay un cheatVM y una copia previa. Revisa las carpetas antes de seguir.')
    if prev.exists() and not prev.is_dir():
        raise FileExistsError(f'Ruta inesperada: {prev}')
    for folder in mods_root.iterdir() if mods_root.is_dir() else ():
        if folder.name in (MOD_NAME, 'cheatvm') or not folder.is_dir():
            continue
        if (folder / 'exefs' / 'subsdk9').exists():
            raise FileExistsError(f'Otro mod usa subsdk9: {folder.name}. Desactivalo primero.')
    for name, contents in mod_files.items():
        existing = mod / 'exefs' / name
        if existing.exists() and (not existing.is_file() or existing.read_bytes() != contents):
            raise FileExistsError(f'No se sobrescribira un archivo diferente: {existing}')
    return mod, prev, backup


def set_spanish(settings: Path) -> None:
    if settings.exists():
        txt = settings.read_text(encoding='utf-8-sig')
        lines = txt.splitlines()
        lines = [line for line in lines if not line.strip().startswith('language=')]
        lines.append('language=es')
        if '\r\n' in txt:
            settings.write_bytes(('\r\n'.join(lines) + '\r\n').encode('utf-8'))
        else:
            settings.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    else:
        settings.parent.mkdir(parents=True, exist_ok=True)
        settings.write_text('language=es\n', encoding='utf-8')


def install(root: Path, archive: bytes, translation: Path, dry_run: bool = False) -> list[Path]:
    root = verify_root(root)
    mod_files = read_mod_files(archive)
    if not translation.is_file() or translation.stat().st_size > 150000:
        raise ValueError('No aparece es.json junto al instalador (o es demasiado grande).')
    import json
    lang = json.loads(translation.read_text(encoding='utf-8-sig'))
    if lang.get('language') != 'Español' or not isinstance(lang.get('strings'), dict):
        raise ValueError('La traduccion es.json no es valida.')
    mod, prev, backup = check_no_conflicts(root, mod_files)
    lang_file = root / 'sdmc' / MOD_NAME / 'lang' / 'es.json'
    settings = root / 'sdmc' / MOD_NAME / 'settings.ini'
    if lang_file.exists() and lang_file.read_bytes() != translation.read_bytes():
        raise FileExistsError(f'No se sobrescribira una traduccion distinta: {lang_file}')
    targets = [mod / 'exefs' / name for name in mod_files] + [lang_file, settings]
    if dry_run:
        return targets
    moved = False
    created = []
    try:
        if prev.is_dir():
            backup.parent.mkdir(parents=True, exist_ok=True)
            prev.rename(backup)
            moved = True
        for name, contents in mod_files.items():
            target = mod / 'exefs' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                with target.open('xb') as f:
                    created.append(target)
                    f.write(contents)
        lang_file.parent.mkdir(parents=True, exist_ok=True)
        if not lang_file.exists():
            with lang_file.open('xb') as f:
                created.append(lang_file)
                f.write(translation.read_bytes())
        if not settings.exists():
            created.append(settings)
        else:
            # Conserva una copia de la configuracion original la primera vez.
            original = root / 'eritchii_oot_copias' / 'settings_anterior.ini'
            if not original.exists() and 'language=es' not in settings.read_text(encoding='utf-8-sig'):
                original.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(settings, original)
        set_spanish(settings)
    except Exception:
        for p in reversed(created):
            p.unlink(missing_ok=True)
        if moved:
            backup.rename(prev)
        raise
    return targets


def restore(root: Path) -> None:
    root = verify_root(root)
    mod = root / 'load' / TITLE / MOD_NAME
    prev = root / 'load' / TITLE / 'cheatvm'
    backup = root / 'eritchii_oot_copias' / 'cheatvm_anterior'
    if prev.exists():
        raise FileExistsError('Ya hay un cheatVM activo: no se sobrescribira.')
    if mod.is_dir():
        allowed = {f'exefs/{name}' for name in ('subsdk9', *(f'{bid}.ips' for bid in BUILDS))}
        actual = {f.relative_to(mod).as_posix() for f in mod.rglob('*') if f.is_file()}
        if not actual.issubset(allowed):
            raise FileExistsError('Hay otros archivos en sloperinaGZ; no se borrara un mod modificado.')
        shutil.rmtree(mod)
    if backup.is_dir():
        prev.parent.mkdir(parents=True, exist_ok=True)
        backup.rename(prev)
    print('Menu sloperinaGZ desactivado; cheatVM anterior restaurado si habia copia.')
    print('Los archivos es.json y la configuracion se conservan.')


def main() -> int:
    p = argparse.ArgumentParser(description='Menu completo de OoT + traduccion al espanol para Eritchii')
    p.add_argument('--root', required=True, type=Path, help='Root Data Folder del emulador')
    p.add_argument('--archive', type=Path, help='ZIP de sloperinaGZ 0.0.4.1 descargado previamente')
    p.add_argument('--dry-run', action='store_true', help='Solo comprobar, no modificar nada')
    p.add_argument('--restore', action='store_true', help='Restaurar cheatVM anterior desde la copia')
    args = p.parse_args()
    try:
        if args.restore:
            restore(args.root)
            return 0
        print('Verificando el modulo original sloperinaGZ 0.0.4.1...')
        targets = install(args.root, archive_bytes(args.archive), Path(__file__).with_name('es.json'), args.dry_run)
        print(('Comprobacion correcta' if args.dry_run else 'Instalacion completa') + ':')
        for f in targets:
            print('  ' + str(f))
        if not args.dry_run:
            print('\nCierra y reinicia Zelda. Activa sloperinaGZ en los mods del juego si hace falta.')
            print('Abre el menu con R + clic del stick derecho hacia ABAJO.')
            print('Selecciona con L; navega con la cruceta. Idioma: Espanol.')
            print('La antigua carpeta cheatvm se guardo como copia si estaba instalada.')
        return 0
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())