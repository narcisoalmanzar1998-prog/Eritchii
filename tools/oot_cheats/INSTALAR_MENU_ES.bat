@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "ROOT=%APPDATA%\eden"
echo.
echo === ERITCHII - MENU AVANZADO DE OOT EN ESPANOL ===
echo.
echo Se instalaran los trucos en:
echo %ROOT%
echo.
echo Cierra Zelda antes de continuar.
echo El menu de cheats anterior se guardara como copia de seguridad.
echo.
if not exist "%ROOT%" (
  echo ERROR: no existe esta carpeta. Consulta LEEME_MENU_ES.md.
  pause
  exit /b 1
)
choice /M "Quieres instalar el menu ampliado y traducido"
if errorlevel 2 exit /b 1
python "%~dp0optional-OoT-cheats\instalar_menu_es.py" --root "%ROOT%"
echo.
echo Si aparece un ERROR, copia el mensaje para revisarlo.
pause
