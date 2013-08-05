# coding: utf-8
import util


class AccessError(Exception):
    pass


def get(address, username, password, driver=None):
    """
    Calls get method from appropriate driver.
    If no driver is passed to this function, it will try to choose the best driver.
    """
    if driver is None:
        driver = util.find_driver(address, username, password)
    try:
        return driver.get(address, username, password)
    except:
        raise AccessError("Error trying to get client list from DHCP server %s with username '%s' and password '%s'" % (address, username, password))
