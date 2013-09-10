DHClientList
============

DHClientList is a tool to get the current client list of a DHCP server. With it one can check who is connected to the local network. To do this one must provide the DHCP server address (IP in local network and port), username and password.

## Installation ##
	pip install dhclientlist

## Usage ##

### Command-line: ###

    usage: dhclientlist print [-h] [-d DRIVERNAME] [-a ADDRESS] [-u USERNAME]
                              [-p PASSWORD] [-f {json,texttable}]

    optional arguments:
      -h, --help            show this help message and exit
      -d DRIVERNAME, --driver DRIVERNAME
                            specify a driver to be used
      -a ADDRESS, --address ADDRESS
                            local dhcp server's address. (default: 192.168.0.1:80)
      -u USERNAME, --username USERNAME
                            local dhcp server's username. (default: admin)
      -p PASSWORD, --password PASSWORD
                            local dhcp server's password.
      -f {json,texttable}, --format {json,texttable}
                            the format of the output list. (default: texttable)

### Python: ###

	import dhclientlist
	dhclientlist.get(address, username, password)  # optionally the 4th parameter: driver

## Drivers ##
	 
The connection with DHCP server is made by a _driver_, a python module inside the **dhclientlist.drivers** package (or in any of its sub-packages) that has a get(address, username, password) function which return a list of dicts; each dict containing the following key-value pairs:
	
	("name", name_str)    # name of the guest connected to the dhcp server
	("mac", mac_str)      # MAC address of the guest connected to the dhcp server
	("ip", ip_str)        # IP address of the guest connected to the dhcp server
	("lease", lease_str)  # time in the format hh:mm:ss until this registry is updated in the dhcp server

The **dhclientlist.util.find_driver** function will try to find the appropriate driver for the local DHCP server. However, the number of drivers is quite small at the moment, and dhclientlist may not succeed with the local DHCP server. In this case, one is welcome to contribute by forking this project and developing a driver to the local DHCP server.
