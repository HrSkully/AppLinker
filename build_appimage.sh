#!/bin/bash

echo "Bündle Python-Code mit PyInstaller..."
pip install pyinstaller --quiet

python3 -m PyInstaller --noconfirm --onefile --windowed \
            --paths core \
            --add-data "icons:icons" \
            --name "yail" \
            core/main.py

if [ ! -f linuxdeploy-x86_64.AppImage ]; then
    echo "Lade linuxdeploy herunter..."
    wget -c https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
    chmod +x linuxdeploy-x86_64.AppImage
fi

export OUTPUT="YAIL-x86_64.AppImage"
export APPIMAGE_EXTRACT_AND_RUN=1

if ./linuxdeploy-x86_64.AppImage --executable dist/yail \
    --icon-file icons/yail_icon.png \
    --icon-filename yail \
    --appdir AppDir \
    --create-desktop-file \
    --output appimage; then
    echo "------------------------------------------------"
    echo "ERFOLG: AppImage wurde erstellt: $OUTPUT"
    echo "------------------------------------------------"
else
    echo "------------------------------------------------"
    echo "FEHLER: AppImage konnte nicht erstellt werden."
    echo "Wahrscheinlich liegt es am Icon (max. 512x512 erlaubt)."
    echo "------------------------------------------------"
    exit 1
fi