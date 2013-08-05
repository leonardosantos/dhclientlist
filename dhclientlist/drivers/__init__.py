# coding: utf-8
"""
This package is intended to contain the drivers for each dhcp server.
In order to acheive it, every module must contain one visible *get* function.

Every get function must receive its 3 fisrt parameters as described in DRIVER_ARGSPEC bellow
"""
DRIVER_ARGSPEC = ['address',  # dhcp server's address, normally the host and port
                  'username',  # username used to authenticate within the dhcp server
                  'password']  # password used to authenticate within the dhcp server

"""
And every get function must return a list of dicts, each dict containing the following key-value pairs:
- "name", str  # name of the guest connected to the dhcp server
- "mac", str  # MAC address of the guest connected to the dhcp server
- "ip", str  # IP address of the guest connected to the dhcp server
- "lease", str  # time in the format hh:mm:ss until this registry is updated in the dhcp server

Each module should be within a sub package of this drivers package, for organization reasons.
Each sub package should group drivers by its target router company.
"""
