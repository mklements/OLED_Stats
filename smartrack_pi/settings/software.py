import subprocess


def _run_process(commands):
    return subprocess.run(
        commands,
        check=False,
    )


def update():
    print("Updating...")
    _run_process(
        [
            "/home/smartrack/smartrack-pi/smartrack_pi/.venv/bin/python",
            "/home/smartrack/smartrack-pi/smartrack_pi/cli.py",
            "display",
            "message",
            "Updating...",
        ]
    )
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
    _run_process(
        [
            "/home/smartrack/smartrack-pi/smartrack_pi/.venv/bin/python",
            "/home/smartrack/smartrack-pi/smartrack_pi/cli.py",
            "display",
            "message",
            "Resetting Companion...",
        ]
    )
    _run_process(["sudo", "cp", "/home/smartrack/smartrack-pi/companion/db", "/home/companion/.config/companion-nodejs/v3.2/db"])
    _run_process(["sudo", "reboot"])

    print("Update complete.")
    return