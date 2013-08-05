# coding: utf-8
""" Manage the command line options to get the list, then prints the result in the desired format. """

from __init__ import get
import texttable
import optparse
import json
import util
import sys

texttable_deco = texttable.Texttable.HEADER + texttable.Texttable.BORDER

optparser = optparse.OptionParser()
optparser.add_option("-l", "--list-drivers", dest="list_drivers", action="store_true", help="list all drivers")
optparser.add_option("-d", "--driver", dest="drivername", default=None, help="specify a driver to be used")
optparser.add_option("-a", "--address", dest="address", default="192.168.0.1:80", help="local dhcp server's address. [default: '%default']")
optparser.add_option("-u", "--username", dest="username", default="admin", help="local dhcp server's username. [default: '%default']")
optparser.add_option("-p", "--password", dest="password", default="", help="local dhcp server's password. [default: '%default']")
optparser.add_option("-f", "--format", dest="format", default="texttable", choices=["json", "texttable"],
                     help="the format of the output list. [choices: json, texttable] [default: '%default']")

(options, args) = optparser.parse_args()

if options.list_drivers:
    table = texttable.Texttable()
    table.set_deco(texttable_deco)
    table.add_rows([["All drivers"]] + [[driver_name.replace('drivers.', '')] for driver_name in util.list_all_drivers()])
    print table.draw()
try:
    result = get(options.address, options.username, options.password, util.drivername_to_module(options.drivername))
except Exception as ex:
    print >>sys.stderr, ex
    exit(1)

if len(result):
    if options.format == "json":
        print json.dumps(result)
    elif options.format == "texttable":
        table = texttable.Texttable()
        table.set_deco(texttable_deco)
        cols = result[0].keys()
        cols.sort()
        cols.reverse()
        table.add_rows([[col.upper() for col in cols]] + [[row[cel] for cel in cols] for row in result])
        print table.draw()
else:
    print "No results found."
