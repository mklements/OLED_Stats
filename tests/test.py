import os
import json
import subprocess

COMPANION_DB = "/home/companion/.config/companion-nodejs/v3.2/db"

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

def restore_file(filename):
    config_file = (get_companion_config(filename))    
    streamdeck_1,streamdeck_2,streamdeck_3 = _get_streamdeck_names()

    new_config = _replace_default_names(config_file)
    tmp_location = "/tmp/config"
    with open (tmp_location, "w") as f:
        f.write(json.dumps(new_config))
        
    print("Updating Companion...")
    # file_path = f"/home/smartrack/smartrack-pi/companion/{file_name}"
    # show.text(f"Restoring Companion File: {file_name} & Rebooting")
    _run_process(["sudo", "cp", "/tmp/config", COMPANION_DB])
    _run_process(["sudo", "reboot"])
    # return f"Restoring {file_name}"
    print(streamdeck_1, streamdeck_2, streamdeck_3)