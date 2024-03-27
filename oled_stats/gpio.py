import os
import subprocess
from signal import pause
from time import sleep

from gpiozero import Button

WAS_HELD = False
DHCP = True


def write_config(config):
    with open("/tmp/interfaces", "w") as f:
        f.write(config)
    pcess = subprocess.run(["sudo", "mv", "/tmp/interfaces", "/etc/network/interfaces"])
    print(pcess)
    print("Flushing Networking")
    pcess = subprocess.run(["sudo", "ip", "addr", "flush", "eth0"])
    print("Restarting Networking")
    print(pcess)
    pcess = subprocess.run(["sudo", "systemctl", "restart", "networking"])
    print(pcess)


def set_network_config(interface, ip_address, netmask, gateway):
    """Sets the network configuration for a given interface.

    Args:
      interface: The name of the network interface.
      ip_address: The IP address to assign to the interface.
      netmask: The netmask for the IP address.
      gateway: The gateway for the network.
    """

    return f"""# auto {interface}
  iface {interface} inet static
    address {ip_address}
    netmask {netmask}
    gateway {gateway}
"""


def set_auto():
    return """auto eth0
allow-hotplug eth0
iface eth0 inet dhcp
"""


def released():
    global WAS_HELD
    global DHCP
    print(WAS_HELD)
    print("take action")
    WAS_HELD = False
    if DHCP:
        print("Setting to DHCP")
        config = set_auto()
    else:
        print("Setting to Static")
        config = set_network_config(
            "eth0", "192.168.1.241", "255.255.255.0", "192.168.1.1"
        )
    write_config(config)
    DHCP = not DHCP


def held():
    global WAS_HELD
    WAS_HELD = True


button = Button(21, hold_time=5, bounce_time=0.1)
button.when_released = released
button.when_held = held

pause()
