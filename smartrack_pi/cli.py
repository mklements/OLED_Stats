import json
import os
import sys
from time import sleep

from display import change_display
from ip.set_adaptor import Adaptor
from settings import software

adaptor = Adaptor()


def _get_config():
    with open(
        "/home/smartrack/smartrack-pi/smartrack_pi/config.json", encoding="utf-8"
    ) as f:
        return json.load(f)


def _set_config(key, value):
    config = _get_config()
    config[key] = value
    with open(
        "/home/smartrack/smartrack-pi/smartrack_pi/config.json", "w", encoding="utf-8"
    ) as f:
        json.dump(config, f)


def set_dhcp():
    print("Setting to DHCP")
    adaptor.set_adaptor_dhcp()
    _set_config("mode", "D")


def set_static(ip_address, gateway):
    print("Setting to Static")

    adaptor.set_adaptor_static(ip_address, gateway)
    _set_config("static_ip", ip_address)
    _set_config("gateway", gateway)
    _set_config("mode", "S")


def set_net():
    try:
        net_type = sys.argv[2].lower()
    except IndexError:
        net_type = None
        print("Please supply type: ('dhcp' or 'static')")
    if net_type:
        match net_type:
            case "dhcp":
                change_display.display_text("Setting Net Mode", "to DHCP...")
                set_dhcp()
            case "static":

                try:
                    change_display.display_text("Setting Net Mode", "to Static...")
                    ip = sys.argv[3]
                    gateway = sys.argv[4]
                    set_static(ip, gateway)
                except IndexError:
                    print(
                        "Please ip and gateway: ('smartrack net static 192.168.1.100 10.1.1.1')"
                    )
            case _:
                print("Net type is either 'dhcp' or 'static'")
        sleep(5)
        change_display.stats_status()


def set_display():
    try:
        display_command = sys.argv[2].lower()
    except IndexError:
        display_command = None
        print("Please supply a display command: ('stats' or 'message')")
    if display_command:
        match display_command:
            case "stats":
                try:
                    status = sys.argv[3].lower()
                except IndexError:
                    status = True
                if status == "false":
                    print("Stopping Stats Display...")
                    change_display.stats_status(False)
                else:
                    print("Starting Stats Display...")
                    change_display.stats_status()
            case "message":
                try:
                    messages = sys.argv[3].split("+")
                except IndexError:
                    messages = []
                print(f"Displaying message: {messages}")
                change_display.display_text(*messages)
            case _:
                print("Not a valid command (commands: stats, message)")

def companion():
    try:
        companion_command = sys.argv[2].lower()
    except IndexError:
        companion_command = None
        print("Please supply type: ('set_default' or 'restore')")
    if companion_command:
        match companion_command:
            case "set_default":
                software.update_companion_default()
            case "restore":
                try:
                    file_name = sys.argv[3].lower()
                    file_path =f"/home/smartrack/smartrack-pi/companion/{file_name}"
                    if os.path.isfile(file_path):
                        return software.restore_companion_file(file_name)
                    return f"No valid file path supplied: {file_path}"      
                except IndexError:
                    return "No file path supplied"
                
            case _:
                print("Not a valid command (commands: set_default, restore)")

if __name__ == "__main__":
    try:
        command = sys.argv[1]
    except IndexError:
        command = None
        print("Please Supply Command: ('net' or 'display')")

    match command:
        case "net":
            set_net()
        case "display":
            set_display()
        case "companion":
            print(companion())
        case "update":
            software.update()
        case "factory":
            prompt = input("This will reset all companion settings, and set to dhcp.  Enter Y to continue... \n")
            if prompt.lower() == "y":
                software.factory_reset()
        case _:
            print("Command Not Found")
