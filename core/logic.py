import os
import subprocess
import json

CONFIG_PATH = os.path.expanduser("~/.config/applinker/config.json")

def load_config():
    """Lädt die Konfiguration oder gibt Standardwerte zurück."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"language": None}

def save_config(config_data):
    """Speichert die Konfiguration im Home-Verzeichnis."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Fehler beim Speichern der Config: {e}")

def create_desktop_file(name, exec_path, icon_path, description, wm_class, categories="Utility;"):
    file_id = name.lower().replace(' ', '_')
    dest_path = f"/usr/share/applications/{file_id}.desktop"
    temp_desktop = f"/tmp/{file_id}.desktop"

    icon_ext = os.path.splitext(icon_path)[1]
    system_icon_path = f"/usr/share/pixmaps/{file_id}{icon_ext}"

    content = f"""[Desktop Entry]
Type=Application
Name={name}
Exec="{exec_path}"
Icon={system_icon_path}
Comment={description}
Terminal=false
StartupWMClass={wm_class}
X-Created-By=AppLinker
Categories={categories}
"""

    with open(temp_desktop, "w") as f:
        f.write(content)

    cmd = [
        "pkexec", "bash", "-c",
        f"cp '{icon_path}' '{system_icon_path}' && "
        f"mv '{temp_desktop}' '{dest_path}' && "
        f"chmod 644 '{dest_path}' '{system_icon_path}' && "
        f"update-desktop-database /usr/share/applications"
    ]

    try:
        subprocess.run(cmd, check=True)
        return True, dest_path
    except Exception as e:
        return False, str(e)


def get_installed_apps():
    """Scannt nach .desktop Dateien, die mit AppLinker erstellt wurden (robuste Version)."""
    app_dir = "/usr/share/applications/"
    installed_apps = []

    if not os.path.exists(app_dir):
        return []

    try:
        filenames = os.listdir(app_dir)
    except OSError:
        return []

    for filename in filenames:
        if not filename.endswith(".desktop"):
            continue

        path = os.path.join(app_dir, filename)

        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if "X-Created-By=AppLinker" in content:
                    display_name = filename.replace(".desktop", "")

                    for line in content.splitlines():
                        if line.startswith("Name="):
                            parts = line.split("=", 1)
                            if len(parts) > 1:
                                display_name = parts[1].strip()
                            break

                    installed_apps.append({
                        "name": display_name,
                        "path": path,
                        "id": filename.replace(".desktop", "")
                    })
        except (OSError, PermissionError):
            continue

    installed_apps.sort(key=lambda x: x['name'].lower())
    return installed_apps

def delete_desktop_file(file_path):
    """Löscht eine .desktop-Datei und das zugehörige Icon systemweit."""
    try:
        file_id = os.path.basename(file_path).replace(".desktop", "")
        icon_pattern = f"/usr/share/pixmaps/{file_id}.*"

        cmd = [
            "pkexec", "bash", "-c",
            f"rm '{file_path}' && rm -f {icon_pattern} && update-desktop-database /usr/share/applications"
        ]

        subprocess.run(cmd, check=True)
        return True, "Erfolgreich gelöscht"
    except Exception as e:
        return False, str(e)