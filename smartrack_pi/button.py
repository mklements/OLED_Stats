import json
import os
import subprocess
from signal import pause
from time import sleep

from display import change_display
from gpiozero import Button
from ip.set_adaptor import Adaptor

WAS_HELD = False




def released():
    global WAS_HELD
    WAS_HELD = False
    adaptor = Adaptor()
    if adaptor.config.get("mode") == "D":
        print("Setting to Static")
        change_display.display_text("Setting Net Mode", "to Static...")
        adaptor.set_adaptor_static()
    else:
        print("Setting to DHCP")
        change_display.display_text("Setting Net Mode", "to DHCP...")
        adaptor.set_adaptor_dhcp()
    sleep(5)
    change_display.stats_status()


def held():
    global WAS_HELD
    WAS_HELD = True


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
