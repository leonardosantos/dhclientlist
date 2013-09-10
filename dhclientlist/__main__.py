# coding: utf-8
""" Manage the command line args to get the list, then prints the result in the desired format. """

from __init__ import get
import texttable
import argparse
import json
import util
import sys


class ArgumentDefaultsVoidHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def _get_help_string(self, action):
        if action.default:
            return super(ArgumentDefaultsVoidHelpFormatter, self)._get_help_string(action)
        return action.help

texttable_deco = texttable.Texttable.HEADER + texttable.Texttable.BORDER

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='commands', dest='command')

parser_list_drivers = subparsers.add_parser('list-drivers', help='list all drivers')

parser_print = subparsers.add_parser('print', help='retrieves and prints the dhcp server client list',
                                     formatter_class=ArgumentDefaultsVoidHelpFormatter)
parser_print.add_argument("-d", "--driver", dest="drivername", default=None, help="specify a driver to be used")
parser_print.add_argument("-a", "--address", dest="address", default="192.168.0.1:80", help="local dhcp server's address.")
parser_print.add_argument("-u", "--username", dest="username", default="admin", help="local dhcp server's username.")
parser_print.add_argument("-p", "--password", dest="password", default="", help="local dhcp server's password.")
parser_print.add_argument("-f", "--format", dest="format", default="texttable", choices=["json", "texttable"],
                          help="the format of the output list.")

args = parser.parse_args()

if args.command == 'list-drivers':
    table = texttable.Texttable()
    table.set_deco(texttable_deco)
    table.add_rows([["All drivers"]] + [[driver_name.replace('drivers.', '')] for driver_name in util.list_all_drivers()])
    print table.draw()

elif args.command == 'print':
    try:
        result = get(args.address, args.username, args.password, util.drivername_to_module(args.drivername))
    except Exception as ex:
        print >>sys.stderr, ex
        exit(1)

    if len(result):
        if args.format == "json":
            print json.dumps(result)
        elif args.format == "texttable":
            table = texttable.Texttable()
            table.set_deco(texttable_deco)
            cols = result[0].keys()
            cols.sort()
            cols.reverse()
            table.add_rows([[col.upper() for col in cols]] + [[row[cel] for cel in cols] for row in result])
            print table.draw()
    else:
        print "No results found."
