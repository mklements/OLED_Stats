import json
import os
import sys

from ip.set_adaptor import Adaptor

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


if __name__ == "__main__":
    command = sys.argv[1]

    match command:
        case "dhcp":
            set_dhcp()
        case "static":
            ip = sys.argv[2]
            gateway = sys.argv[3]
            set_static(ip, gateway)
        case _:
            print("Command Not Found")
