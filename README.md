# YAIL - Yet Another AppImage Linker 🚀

![Build Status](https://github.com/HrSkully/YAIL/actions/workflows/release.yml/badge.svg)

**YAIL** ist ein schlankes GUI-Tool basierend auf Python und PyQt6, um AppImage-Dateien (oder andere ausführbare Dateien) nahtlos in Linux-Desktop-Umgebungen zu integrieren. Es erstellt automatisch `.desktop`-Dateien, damit deine Apps im App-Menü erscheinen, ein Icon haben und an das Dock angeheftet werden können.

## Features
- ✨ Erstellt saubere `.desktop`-Starter in `/usr/share/applications/`
- 🖼️ Unterstützung für benutzerdefinierte Icons
- 📂 Einfache Dateiauswahl über GUI-Dialoge
- 🛠️ Automatische Rechtevergabe (macht Dateien ausführbar)
- 🐧 Entwickelt für moderne Linux-Desktops (GNOME, KDE, XFCE etc.)

## Nutzung (AppImage)

Der einfachste Weg, YAIL zu nutzen, ist das fertige AppImage:

1. **Download:** Lade die neueste Version unter [Releases](https://github.com/HrSkully/YAIL/releases) herunter.
2. **Ausführbar machen:** Klicke rechts auf die Datei -> Eigenschaften -> Berechtigungen -> "Datei als Programm ausführen" (oder via Terminal: `chmod +x YAIL-x86_64.AppImage`).
3. **Starten:** Doppelklick auf die Datei und loslegen!

> **Hinweis:** Da YAIL Starter systemweit unter `/usr/share/applications/` erstellt, wird beim Speichern nach deinem Passwort gefragt (`pkexec`).

## Für Entwickler (Source Code)

Falls du das Tool aus dem Quellcode starten möchtest:

1. Repository klonen:
   ```bash
   git clone [https://github.com/HrSkully/YAIL.git](https://github.com/HrSkully/YAIL.git)
   cd YAIL