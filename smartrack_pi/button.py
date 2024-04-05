import os
import subprocess
from signal import pause
from time import sleep

from dotenv import find_dotenv, load_dotenv, set_key
from gpiozero import Button
from ip.set_adaptor import Adaptor

WAS_HELD = False
DOTENV_FILE = find_dotenv()
adaptor = Adaptor()


def _set_mode_env(mode):
    os.environ["MODE"] = mode
    set_key(DOTENV_FILE, "MODE", os.environ["MODE"])


def released():
    global WAS_HELD
    print("take action")
    WAS_HELD = False
    load_dotenv(override=True)
    if os.environ["MODE"] == "D":
        print("Setting to Static")
        adaptor.set_adaptor_static(os.getenv("STATIC_IP"), os.getenv("GATEWAY"))
        _set_mode_env("S")
    else:
        print("Setting to DHCP")
        adaptor.set_adaptor_dhcp()
        _set_mode_env("D")


def held():
    global WAS_HELD
    WAS_HELD = True


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
