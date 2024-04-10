import subprocess


def _run_process(commands):
    return subprocess.run(
        commands,
        check=False,
    )


def update():
    print("Updating...")
    _run_process(["sudo", "systemctl", "stop", "stats.service"])
    _run_process(["sudo", "systemctl", "stop", "button.service"])
    _run_process(["cd", "~"])
    _run_process(["sudo", "rm", "-d", "-r", "smartrack-pi"])
    _run_process(["git", "clone", "https://github.com/ctus-dev/smartrack-pi.git"])
    _run_process(["cd", "smartrack-pi"])
    _run_process(["chmod", "+x", "install/update.sh"])
    _run_process(["install/update.sh"])
    print("Update complete.")
    return
