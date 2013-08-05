# coding: utf-8
import requests
import re
import json


def get(address, username, password):
    GROUP_LENGTH = 4
    page = requests.get("http://%s/userRpm/AssignedIpAddrListRpm.htm" % address, auth=(username, password))
    list_str = re.search("(var DHCPDynList = new Array\(([^\)]*)\))", page.content.replace("\n", "")).groups()[1]
    list_arr = json.loads('[%s]' % list_str)
    list_arr = list_arr[0:(len(list_arr) // GROUP_LENGTH) * GROUP_LENGTH]
    groups = [{'name': list_arr[i],
               'mac': list_arr[i+1],
               'ip': list_arr[i+2],
               'lease': list_arr[i+3]}
              for i in range(len(list_arr))[0::GROUP_LENGTH]]
    return groups
