#!/bin/bash
# Abhängigkeiten installieren (einmalig nötig)
# pip install pyinstaller

# Alles zu einer ausführbaren Datei bündeln
pyinstaller --noconfirm --onefile --windowed \
            --add-data "icons:icons" \
            --name "yail" \
            core/main.py

# Linuxdeploy nutzen, um das AppImage zu bauen
# Download von linuxdeploy herunter, falls nicht vorhanden
if [ ! -f linuxdeploy-x86_64.AppImage ]; then
    wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
    chmod +x linuxdeploy-x86_64.AppImage
fi

# AppImage generieren
export OUTPUT="YAIL-x86_64.AppImage"
./linuxdeploy-x86_64.AppImage --executable dist/yail \
    --description "Yet Another AppImage Linker" \
    --icon-file icons/yail_icon.png \
    --display-name "YAIL" \
    --appdir AppDir --output appimage