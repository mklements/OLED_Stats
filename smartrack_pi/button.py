import json
import os
import subprocess
from signal import pause
from time import sleep

from gpiozero import Button
from ip.set_adaptor import Adaptor

WAS_HELD = False

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


def released():
    global WAS_HELD
    WAS_HELD = False
    config = _get_config()
    if config.get("mode") == "D":
        print("Setting to Static")
        adaptor.set_adaptor_static(config.get("static_ip"), config.get("gateway"))
        _set_config("mode", "S")
    else:
        print("Setting to DHCP")
        adaptor.set_adaptor_dhcp()
        _set_config("mode", "D")


def held():
    global WAS_HELD
    WAS_HELD = True


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
