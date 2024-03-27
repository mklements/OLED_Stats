import os
import subprocess
from signal import pause
from time import sleep

from dotenv import load_dotenv
from gpiozero import Button

WAS_HELD = False
DHCP = True


def set_static(ip_address, gateway):

    pcess = subprocess.run(
        [
            "sudo",
            "nmcli",
            "con",
            "mod",
            "ipstatic",
            "ipv4.addresses",
            f"{ip_address}",
            "ipv4.gateway",
            gateway,
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
            "dhcp",
            "connection.autoconnect",
            "no",
            "connection.autoconnect-priority",
            "-1",
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
            "ipstatic",
            "connection.autoconnect",
            "yes",
            "connection.autoconnect-priority",
            "10",
        ],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        ["sudo", "nmcli", "con", "down", "dhcp"],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        ["sudo", "nmcli", "con", "up", "ipstatic"],
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
            "ipstatic",
            "connection.autoconnect",
            "no",
            "connection.autoconnect-priority",
            "-1",
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
            "dhcp",
            "connection.autoconnect",
            "yes",
            "connection.autoconnect-priority",
            "10",
        ],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        ["sudo", "nmcli", "con", "down", "ipstatic"],
        check=False,
    )
    print(pcess)

    pcess = subprocess.run(
        ["sudo", "nmcli", "con", "up", "dhcp"],
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
        load_dotenv(override=True)
        set_static(os.getenv("STATIC_IP"), os.getenv("STATIC_IP"))
    DHCP = not DHCP


def held():
    global WAS_HELD
    WAS_HELD = True


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
