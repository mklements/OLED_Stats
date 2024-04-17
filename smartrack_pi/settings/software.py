import subprocess
from display import change_display

def _run_process(commands):
    return subprocess.run(
        commands,
        check=False,
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
    change_display.display_text("Factory Resetting",  "Companion....")
    _run_process(["sudo", "cp", "/home/smartrack/smartrack-pi/companion/db", "/home/companion/.config/companion-nodejs/v3.2/db"])
    _run_process(["sudo", "reboot"])

    print("Update complete.")
    return