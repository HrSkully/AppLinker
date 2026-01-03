import os
import subprocess
import json

# Global path for the configuration file in the user's home directory
CONFIG_PATH = os.path.expanduser("~/.config/applinker/config.json")

def load_config():
    """
    Loads the user configuration from the JSON file.
    Returns a dictionary with language settings or default values if file is missing/invalid.
    """
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
                # Ensure the expected key exists
                if "language" in config:
                    return config
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or unreadable, fall back to defaults
            pass
    return {"language": None}

def save_config(config_data):
    """
    Saves the provided configuration dictionary to the local config path.
    Creates necessary directories if they do not exist.
    """
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    try:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Error saving configuration: {e}")

def create_desktop_file(name, exec_path, icon_path, description, wm_class, categories="Utility;"):
    """
    Creates a Linux .desktop entry and installs it system-wide.
    This includes copying the icon to /usr/share/pixmaps/ and the entry to /usr/share/applications/.
    Uses pkexec for administrative privileges.
    """
    # Generate a unique ID based on the application name
    file_id = name.lower().replace(' ', '_')
    dest_path = f"/usr/share/applications/{file_id}.desktop"
    temp_desktop = f"/tmp/{file_id}.desktop"

    # Determine icon extension and set system-wide icon path
    icon_ext = os.path.splitext(icon_path)[1]
    system_icon_path = f"/usr/share/pixmaps/{file_id}{icon_ext}"

    # Construct the content for the .desktop entry
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

    # Write temporary file before moving it to a restricted system folder
    with open(temp_desktop, "w") as f:
        f.write(content)

    # Shell command execution via pkexec for elevated permissions
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
    """
    Scans the system applications folder for files created by AppLinker.
    Checks for the 'X-Created-By=AppLinker' tag inside .desktop files.
    Returns a sorted list of application metadata dictionaries.
    """
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
            # Open file with error ignoring to handle non-utf-8 system files
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if "X-Created-By=AppLinker" in content:
                    display_name = filename.replace(".desktop", "")

                    # Extract the actual Name field for a better UI display
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

    # Alphabetical sorting by application name
    installed_apps.sort(key=lambda x: x['name'].lower())
    return installed_apps

def delete_desktop_file(file_path):
    """
    Removes a .desktop file and its associated icon from the system folders.
    Triggers a database update for the desktop environment to reflect changes.
    """
    try:
        # Extract the file ID to locate the corresponding icon
        file_id = os.path.basename(file_path).replace(".desktop", "")
        icon_pattern = f"/usr/share/pixmaps/{file_id}.*"

        # Combined command to remove both entry and icon, then refresh system database
        cmd = [
            "pkexec", "bash", "-c",
            f"rm '{file_path}' && rm -f {icon_pattern} && update-desktop-database /usr/share/applications"
        ]

        subprocess.run(cmd, check=True)
        return True, "Successfully deleted"
    except Exception as e:
        return False, str(e)