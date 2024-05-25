"""Base class for other network types to inherit."""

import logging
from peernet.utils import ch


class BaseNetwork:
    """An abstract class that specific network types will inherit from."""

    def __init__(self, devices, verbose=0, *args, **kwargs):
        """Constructor."""
        # logger setup
        self.logger = logging.getLogger("BaseNetwork")
        if verbose == 0:
            self.logger.setLevel(logging.DEBUG)
        elif verbose == 1:
            self.logger.setLevel(logging.WARN)
        else:
            self.logger.setLevel(logging.CRITICAL)
        self.logger.addHandler(ch)

        # Maintain a forward and reverse mapping of device names and ip addresses
        self.NUM_DEVICES = len(devices)
        self.device_number = {name: i for i, name in enumerate(devices.keys())}
        self.name_to_ip = devices
        self.ip_to_name = {ip: name for name, ip in devices.items()}

    def get_ip(self, hostname: str) -> str:
        """Given a hostname, returns the dns/ip.
        
        Args:
            hostname: str = Hostname as a string.
        
        Returns:
            str - IP address.
        """
        if hostname not in self.name_to_ip:
            self.logger.error(f"Couldn't find device name {hostname} in device mapping")
            return -1

        return self.name_to_ip[hostname]

    def get_hostname(self, ip) -> str:
        """Given an ip, returns the hostname.
        
        Args:
            ip : str = Ip address
            
        Returns:
            str = hostname
        """
        if ip not in self.ip_to_name:
            self.logger.error(f"Coulnd't find ip address {ip} in device mapping")
            return -1

        return self.ip_to_name[ip]
