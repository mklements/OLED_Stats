import os
import subprocess
from copy import copy


class Adaptor:
    """Handles adaptor settings"""

    def __init__(self):
        self.pre_commands = ["sudo", "nmcli", "con"]

    def _run_process(self, commands):
        # return subprocess.run(
        #     commands,
        #     check=False,
        # )

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

    def set_adaptor_static(self, ip_address, gateway):
        """Sets the adaptor for static
        Args:
            ip_address(str)
            gateway(str)
        """
        self._set_adaptor_address(ip_address, gateway)
        self._set_adaptor_priority("up", "ipstatic")
        self._set_adaptor_priority("down", "dhcp")
        self._set_adaptor_status("up", "ipstatic")
        self._set_adaptor_status("down", "dhcp")
