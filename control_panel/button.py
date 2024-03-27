import os
import subprocess
from signal import pause
from time import sleep

from gpiozero import Button

WAS_HELD = False
DHCP = True


def set_static(ip_address):
    pcess = subprocess.run(
        [
            "sudo",
            "nmcli",
            "con",
            "mod",
            "Wired connection 1",
            "ipv4.addresses",
            f"{ip_address}/24",
        ],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        [
            "sudo",
            "nmcli",
            "con",
            "mod",
            "Wired connection 1",
            "ipv4.method",
            "manual",
        ],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        ["sudo", "nmcli", "con", "up", "Wired connection 1"],
        check=False,
    )
    print(pcess)


def set_dhcp():
    pcess = subprocess.run(
        [
            "sudo",
            "nmcli",
            "con",
            "mod",
            "Wired connection 1",
            "ipv4.method",
            "auto",
        ],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        ["sudo", "nmcli", "con", "up", "Wired connection 1"],
        check=False,
    )
    print(pcess)


def released():
    global WAS_HELD
    global DHCP
    print(WAS_HELD)
    print("take action")
    WAS_HELD = False
    if DHCP:
        print("Setting to DHCP")
        set_dhcp()
    else:
        print("Setting to Static")
        config = set_static("192.168.1.241")
    DHCP = not DHCP


def held():
    global WAS_HELD
    WAS_HELD = True


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
