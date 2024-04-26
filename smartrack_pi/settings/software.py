import os
import subprocess
import json
from smartrack_pi.display import show
from smartrack_pi.net import adaptor

COMPANION_DB = "/home/companion/.config/companion-nodejs/v3.2/db"

def get_companion_config_file_list():
    folder = "/home/smartrack/smartrack-pi/companion"
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

def get_companion_config(file):
    filename = f"/home/smartrack/smartrack-pi/companion/{file}"
    with open (filename) as f:
        default_json = json.load(f)
    return default_json

def _run_process(commands):
    return subprocess.run(commands, check=False, cwd="/home/smartrack/smartrack-pi")

def _get_streamdeck_names(config_file):
    streamdeck_1,streamdeck_2,streamdeck_3 =None,None,None
    streamdecks =  (config_file.get("deviceconfig"))
    for streamdeck, values in streamdecks.items():
        match values["config"].get("xOffset"):
            case 0:
                streamdeck_1 = streamdeck
            case 5:
                streamdeck_2 = streamdeck
            case 11:
                streamdeck_3 = streamdeck
    return streamdeck_1,streamdeck_2,streamdeck_3

def _replace_default_names(streamdeck_1,streamdeck_2,streamdeck_3):
    default_file = get_companion_config("system-default")
    default_streamdecks =  (default_file.get("deviceconfig"))
    for streamdeck, values in default_streamdecks.items():
        match values["config"].get("xOffset"):
            case 0:
                default_file["deviceconfig"][streamdeck_1] = default_file["deviceconfig"].pop(streamdeck)
            case 5:
                default_file["deviceconfig"][streamdeck_2] = default_file["deviceconfig"].pop(streamdeck)
            case 11:
                default_file["deviceconfig"][streamdeck_3] = default_file["deviceconfig"].pop(streamdeck)
    return default_file

def check_file(file_name):
    file_path = f"/home/smartrack/smartrack-pi/companion/{file_name}"
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
    # for config in get_companion_config_file_list():
    #     if not config.startswith("system-"):
    #         _run_process(
    #             ["sudo", "rm", f"/home/smartrack/smartrack-pi/companion/{config}"]
    #         )
    # _run_process(
    #     [
    #         "sudo",
    #         "cp",
    #         "/home/smartrack/smartrack-pi/companion/system-default",
    #         "/home/companion/.config/companion-nodejs/v3.2/db",
    #     ]
    # )
    # address = adaptor.Address()
    # address.factory_reset()
    # _run_process(["sudo", "reboot"])

    # print("Update complete.")
    return


def backup_companion_file(file_name):
    file_name = file_name.replace(" ", "").lower()
    print("Backing up Companion...")
    if file_name.find("system-") != -1:
        return "File Name not allowed to start with 'system-'"
    if not file_name.startswith("user-"):
        file_name = f"user-{file_name}"
    repo_db = f"/home/smartrack/smartrack-pi/companion/{file_name}"
    _run_process(["sudo", "cp", COMPANION_DB, repo_db])
    _run_process(["sudo", "chown", "smartrack:smartrack", repo_db])
    return "Back up Complete"


def restore_companion_file(file_name):
    print("Updating Companion...")
    show.text(f"Restoring Companion File: {file_name} & Rebooting")
    config_file = (get_companion_config(file_name))

    streamdeck_1,streamdeck_2,streamdeck_3 = _get_streamdeck_names()
    new_config = _replace_default_names(streamdeck_1,streamdeck_2,streamdeck_3)
    tmp_location = "/tmp/config"
    with open (tmp_location, "w") as f:
        f.write(json.dumps(new_config))

    _run_process(["sudo", "cp", tmp_location, COMPANION_DB])
    _run_process(["sudo", "reboot"])
    return f"Restoring {file_name}"


def delete_companion_file(file_name):
    print("Deleting Companion File...")
    file_path = f"/home/smartrack/smartrack-pi/companion/{file_name}"
    _run_process(["sudo", "rm", file_path])
    return f"Deleted {file_name}"


def push_companion_config(file_name):
    print("Saving System File...")
    if not file_name.startswith("user-"):
        file_name = f"user-{file_name}"
    user_db = f"/home/smartrack/smartrack-pi/companion/{file_name}"
    file_name = file_name.lower().replace("user-", "system-")
    system_db = f"/home/smartrack/smartrack-pi/companion/{file_name}"

    _run_process(["sudo", "cp", user_db, system_db])
    _run_process(["git", "add", system_db])
    _run_process(["git", "commit", "-m", "companion update", system_db])
    _run_process(["git", "push", "origin", "master"])
    return "Update complete."
