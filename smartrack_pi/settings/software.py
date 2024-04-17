import subprocess
from display import change_display
import shutil
import pathlib
from datetime import datetime
def _run_process(commands):
    return subprocess.run(
        commands,
        check=False,
        cwd="/home/smartrack/smartrack-pi"
    )


def update():
    print("Updating...")
    change_display.display_text("Updating")
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
    change_display.display_text(["Factory Resetting", "Companion..."])
    _run_process(["sudo", "cp", "/home/smartrack/smartrack-pi/companion/db", "/home/companion/.config/companion-nodejs/v3.2/db"])
    _run_process(["sudo", "reboot"])

    print("Update complete.")
    return

def update_companion_repo():
    print("Updating Companion...")
    _run_process(["git", "config", "--global", "user.name", "Smartrack"])
    _run_process(["git", "config", "--global", "user.email", "Automation"])
    companion_db = "/home/companion/.config/companion-nodejs/v3.2/db"
    repo_db = "/home/smartrack/smartrack-pi/companion/db"
    repo_archive_dir = f"/home/smartrack/smartrack-pi/companion/archive/{datetime.strftime(datetime.now(), '%Y%m%d %H:%M')}"
    pathlib.Path(repo_archive_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy(repo_db, f"{repo_archive_dir}/db")
    _run_process(["sudo", "cp", companion_db, repo_db])
    _run_process(["git", "commit", "-m", "companion update", "companion/db"])
    _run_process(["git", "push", "origin", "master"])
    print("Update complete.")
    return
