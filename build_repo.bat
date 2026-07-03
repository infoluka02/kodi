@echo off
setlocal enabledelayedexpansion

echo Dang quet cac thu muc trong addons...
set "ADDON_LIST="
for /D %%i in (addons\*) do (
    set "ADDON_LIST=!ADDON_LIST! "%%i""
)

echo Dang build lai repository...
python create_repository.py --datadir="./" !ADDON_LIST!

echo Build xong! Dang cho sep Push len GitHub...
pause