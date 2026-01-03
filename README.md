# AppLinker - Yet Another AppImage Linker 🚀

<p align="center">
  <img src="icons/AppLinker_icon.png" width="128" alt="AppLinker Logo">
</p>

![Build Status](https://github.com/HrSkully/AppLinker/actions/workflows/release.yml/badge.svg)

**AppLinker** ist ein schlankes GUI-Tool basierend auf Python und PyQt6, um AppImage-Dateien (oder andere ausführbare Dateien) nahtlos in Linux-Desktop-Umgebungen zu integrieren. Es erstellt automatisch `.desktop`-Dateien, damit deine Apps im App-Menü erscheinen, ein Icon haben und an das Dock angeheftet werden können.

## Features
- ✨ Erstellt saubere `.desktop`-Starter in `/usr/share/applications/`
- 🖼️ Unterstützung für benutzerdefinierte Icons
- 📂 Einfache Dateiauswahl über GUI-Dialoge
- 🛠️ Automatische Rechtevergabe (macht Dateien ausführbar)
- 🐧 Entwickelt für moderne Linux-Desktops (GNOME, KDE, XFCE etc.)

## Nutzung (AppImage)

Der einfachste Weg, AppLinker zu nutzen, ist das fertige AppImage:

1. **Download:** Lade die neueste Version unter [Releases](https://github.com/HrSkully/AppLinker/releases) herunter.
2. **Ausführbar machen:** Klicke rechts auf die Datei -> Eigenschaften -> Berechtigungen -> "Datei als Programm ausführen" (oder via Terminal: `chmod +x AppLinker-x86_64.AppImage`).
3. **Starten:** Doppelklick auf die Datei und loslegen!

> **Hinweis:** Da AppLinker Starter systemweit erstellt, wird beim Speichern nach deinem Passwort gefragt (`pkexec`), um Schreibrechte für `/usr/share/applications/` zu erhalten.

## Für Entwickler (Source Code)

Falls du das Tool aus dem Quellcode starten oder daran arbeiten möchtest:

### 1. Repository klonen
```bash
git clone [https://github.com/HrSkully/AppLinker.git](https://github.com/HrSkully/AppLinker.git)
cd AppLinker
```

### 2. Abhängigkeiten installieren
Stelle sicher, dass du Python installiert hast und führe dann aus:
```bash
pip install PyQt6
```

### 3. Programm starten
Starte das Programm über den python interpreter:
```bash
python core/main.py
```

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die LICENSE Datei für Details.


