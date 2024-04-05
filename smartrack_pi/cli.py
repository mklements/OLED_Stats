import os
import sys

from dotenv import find_dotenv, load_dotenv, set_key
from ip.set_adaptor import Adaptor

adaptor = Adaptor()
DOTENV_FILE = find_dotenv()
load_dotenv(override=True)


def _set_env(key, value):
    os.environ[key] = value
    set_key(DOTENV_FILE, key, value)


def set_dhcp():
    print("Setting to DHCP")
    adaptor.set_adaptor_dhcp()
    _set_env("MODE", "D")


def set_static(ip_address, gateway):
    print("Setting to Static")

    adaptor.set_adaptor_static(ip_address, gateway)
    _set_env("STATIC_IP", ip_address)
    _set_env("GATEWAY", gateway)
    _set_env("MODE", "S")


if __name__ == "__main__":
    command = sys.argv[1]

    match command:
        case "dhcp":
            set_dhcp()
        case "static":
            ip = sys.argv[2]
            gateway = sys.argv[3]
            set_static(ip, gateway)
