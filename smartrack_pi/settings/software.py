import subprocess
from smartrack_pi.display import show
import shutil
import pathlib
from datetime import datetime
import os
COMPANION_DB = "/home/companion/.config/companion-nodejs/v3.2/db"

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
    show.text("Updating")
    _run_process(["sudo", "systemctl", "stop", "stats.service"])
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
    _run_process(["sudo", "cp", "/home/smartrack/smartrack-pi/companion/db", "/home/companion/.config/companion-nodejs/v3.2/db"])
    _run_process(["sudo", "reboot"])

    print("Update complete.")
    return

def backup_companion_file(file_name):
    print("Backing up Companion...")
    repo_db =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    if check_file(repo_db):
        repo_archive_dir = f"/home/smartrack/smartrack-pi/companion/archive/{datetime.strftime(datetime.now(), '%Y%m%d%H%M')}"
        repo_archive_file = f"{repo_archive_dir}/{file_name}"
        pathlib.Path(repo_archive_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(repo_db, repo_archive_file)
        _run_process(["git", "add", repo_archive_file])
        _run_process(["git", "commit", "-m", "companion update", repo_archive_file])
    _run_process(["sudo", "cp", COMPANION_DB, repo_db])
    _run_process(["git", "add", repo_db])
    _run_process(["git", "commit", "-m", "companion update", repo_db])

    _run_process(["git", "push", "origin", "master"])
    return("Update complete.")

def restore_companion_file(file_name):
    print("Updating Companion...")
    file_path =f"/home/smartrack/smartrack-pi/companion/{file_name}"
    show.text(f"Restoring Companion File: {file_name} & Rebooting")
    _run_process(["sudo", "cp", file_path, COMPANION_DB])
    _run_process(["sudo", "reboot"])
    return(f"Restoring {file_name}")