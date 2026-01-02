import os
import subprocess

def create_desktop_file(name, exec_path, icon_path, categories="Utility;"):
    file_id = name.lower().replace(' ', '_')
    dest_path = f"/usr/share/applications/{file_id}.desktop"
    temp_desktop = f"/tmp/{file_id}.desktop"

    icon_ext = os.path.splitext(icon_path)[1]
    system_icon_path = f"/usr/share/pixmaps/{file_id}{icon_ext}"

    content = f"""[Desktop Entry]
    Name={name}
    Exec="{exec_path}"
    Icon={system_icon_path}
    Type=Application
    Terminal=false
    Categories={categories}
    Comment=Created with YAIL
    """

    with open(temp_desktop, "w") as f:
        f.write(content)

    cmd = [
        "pkexec", "bash", "-c",
        f"cp '{icon_path}' {system_icon_path} && "
        f"mv {temp_desktop} {dest_path} && "
        f"chmod 644 {dest_path} {system_icon_path} && "
        f"update-desktop-database /usr/share/applications"
    ]

    try:
        subprocess.run(cmd, check=True)
        return True, dest_path
    except Exception as e:
        return False, str(e)