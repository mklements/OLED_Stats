import subprocess
from smartrack_pi.display import show
import shutil
import pathlib
from datetime import datetime
import os


COMPANION_DB = "/home/companion/.config/companion-nodejs/v3.2/db"
SYSTEM_CONFIGS = ["default"]

def get_companion_configs():
    folder = "/home/smartrack/smartrack-pi/companion"
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

def _run_process(commands):
    return subprocess.run(
        commands,
        check=False,
        cwd="/home/smartrack/smartrack-pi"
    )

def check_file(file_name):
    file_path =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    if os.path.isfile(file_path):
        return True
    return False

def update():
    print("Updating...")
    show.text("Updating...")
    _run_process(["sudo", "systemctl", "stop", "button.service"])
    _run_process(["git", "fetch", "--all"])
    _run_process(["git", "reset", "--hard", "origin/master"])
    _run_process(["chmod", "+x", "/home/smartrack/smartrack-pi/install/update.sh"])
    _run_process(["/home/smartrack/smartrack-pi/install/update.sh"])
    print("Update complete.")
    return

def factory_reset():    
    print("Resetting...")
    show.text("Factory Resetting Companion...")
    for config in get_companion_configs():
        if not config.startswith("system-"):
            _run_process(["sudo", "rm", f"/home/smartrack/smartrack-pi/companion/{config}"])
    _run_process(["sudo", "cp", "/home/smartrack/smartrack-pi/companion/system-default", "/home/companion/.config/companion-nodejs/v3.2/db"])
    _run_process(["sudo", "reboot"])

    print("Update complete.")
    return

def backup_companion_file(file_name):
    file_name= file_name.replace(" ", "")
    print("Backing up Companion...")
    if file_name.find("system-") != -1:
        return f"File Name not allowed to start with 'system-'"
    elif not file_name.startswith("user-"):
        file_name = f"user-{file_name}"    
    repo_db =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    _run_process(["sudo", "cp", COMPANION_DB, repo_db])
    return("Back up Complete")

def restore_companion_file(file_name):
    print("Updating Companion...")
    file_path =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    show.text(f"Restoring Companion File: {file_name} & Rebooting")
    _run_process(["sudo", "cp", file_path, COMPANION_DB])
    _run_process(["sudo", "reboot"])
    return(f"Restoring {file_name}")

def delete_companion_file(file_name):
    print("Deleting Companion File...")
    file_path =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    _run_process(["sudo", "rm", file_path])
    return(f"Deleted {file_name}")

def push_companion_config(file_name):
    print("Saving System File...")
    if not file_name.startswith("user-"):
        file_name = f"user-{file_name}" 
    user_db =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    file_name = file_name.lower().replace("user-", "system-")
    system_db = f"/home/smartrack/smartrack-pi/companion/{file_name}"

    _run_process(["sudo", "cp", user_db, system_db])
    _run_process(["git", "add", system_db])
    _run_process(["git", "commit", "-m", "companion update", system_db])
    _run_process(["git", "push", "origin", "master"])
    return("Update complete.")

