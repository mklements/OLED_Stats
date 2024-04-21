import json
import os
import re
import subprocess
from copy import copy

dir_path = os.path.dirname(os.path.realpath(__file__))


class Address:
    """Handles adaptor settings"""

    def __init__(self):
        self.pre_commands = ["sudo", "nmcli", "con"]
        self.config = self._get_config()

    def _get_config(self):
        with open(f"{dir_path}/config.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_config(self):
        with open(f"{dir_path}/config.json", "w", encoding="utf-8") as f:
            f.write(
                json.dumps(self.config, indent=4, sort_keys=True, ensure_ascii=False)
            )

    def _run_process(self, commands):
        return subprocess.run(
            commands,
            check=False,
        )

    def _set_adaptor_status(self, status, adaptor):
        commands = copy(self.pre_commands)
        commands.extend([status, adaptor])
        self._run_process(commands)

    def _set_adaptor_priority(self, status, adaptor):
        if status == "up":
            autoconnect = "yes"
            priority = "10"
        else:
            autoconnect = "no"
            priority = "-1"
        commands = copy(self.pre_commands)
        commands.extend(
            [
                "mod",
                adaptor,
                "connection.autoconnect",
                autoconnect,
                "connection.autoconnect-priority",
                priority,
            ]
        )
        self._run_process(commands)

    def _set_adaptor_address(self, ip_address, gateway):
        commands = copy(self.pre_commands)
        commands.extend(
            [
                "mod",
                "ipstatic",
                "ipv4.addresses",
                ip_address,
                "ipv4.gateway",
                gateway,
            ]
        )
        self._run_process(commands)

    def set_adaptor_dhcp(self):
        """Sets the adaptor for dhcp"""
        self._set_adaptor_priority("down", "ipstatic")
        self._set_adaptor_priority("up", "dhcp")
        self._set_adaptor_status("down", "ipstatic")
        self._set_adaptor_status("up", "dhcp")
        self.config["mode"] = "D"
        self._write_config()
        return self.config

    def set_adaptor_static(self, ip_address=None, gateway=None):
        """Sets the adaptor for static
        Args:
            ip_address(str)
            gateway(str)
        """
        if not ip_address:
            ip_address = self.config.get("static_ip", "192.168.1.241/24")

        if not gateway:
            gateway = self.config.get("gateway", "192.168.1.1")
        if self.check_ip(ip_address, gateway):
            self._set_adaptor_address(ip_address, gateway)
            self._set_adaptor_priority("up", "ipstatic")
            self._set_adaptor_priority("down", "dhcp")
            self._set_adaptor_status("up", "ipstatic")
            self._set_adaptor_status("down", "dhcp")

            self.config["static_ip"] = ip_address
            self.config["gateway"] = gateway
            self.config["mode"] = "S"

            self._write_config()
            return self.config
        else:
            raise ValueError("Ip or Gateway not Valid")

    def factory_reset(self):
        self.set_adaptor_dhcp()
        self.config["static_ip"] = "192.168.1.241/24"
        self.config["gateway"] = "192.168.1.1"
        self._write_config()

    def check_ip(self, ip_address, gateway):
        pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(/(3[0-2]|[12]?[0-9]))?$"
        gateway_pattern = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        check = bool(re.match(pattern, ip_address))
        if check:
            check = bool(re.match(gateway_pattern, gateway))
        return check
