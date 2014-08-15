# coding: utf-8
import os.path
import glob
import inspect
import drivers
import texttable


texttable_deco = texttable.Texttable.HEADER + texttable.Texttable.BORDER

IMPORT_BASE = os.path.basename(os.path.dirname(__file__))
try:
    __import__(IMPORT_BASE)
except ImportError:
    IMPORT_BASE = ''


def get_subpackages(package):
    dir_name = os.path.dirname(package.__file__)

    def is_package(d):
        d = os.path.join(dir_name, d)
        return os.path.isdir(d) and glob.glob(os.path.join(d, '__init__.py*'))
    return filter(is_package, os.listdir(dir_name))


def get_modules(package):
    return [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(package.__file__)+"/*.py")]


def find_driver(address, username, password):
    drivers_list = list_all_drivers()
    if len(drivers_list) == 1:
        return drivername_to_module(drivers_list[0])


def list_all_drivers(package=drivers):
    result = []
    package_path = os.path.join(IMPORT_BASE, os.path.relpath(os.path.dirname(package.__file__), os.path.dirname(__file__)))
    fs_to_py = lambda s: s.replace('\\', '.')

    for modname in get_modules(package):
        mod_path = fs_to_py(os.path.join(package_path, modname))
        mod = __import__(mod_path, fromlist=[fs_to_py(package_path)])
        if hasattr(mod, 'get') and hasattr(mod.get, '__call__') and inspect.getargspec(mod.get).args[0:3] == drivers.DRIVER_ARGSPEC:
            result.append(mod_path)

    for subp in get_subpackages(package):
        subp_path = fs_to_py(os.path.join(package_path, subp))
        result += list_all_drivers(__import__(subp_path, fromlist=[fs_to_py(package_path)]))

    return result


class UnknownDriver(Exception):
    pass


def drivername_to_module(drivername):
    if drivername is None:
        return None

    prefix = 'drivers.'
    if len(IMPORT_BASE):
        prefix = '%s.%s' % (IMPORT_BASE, prefix)
    if not drivername.startswith(prefix):
        drivername = prefix + drivername

    try:
        return __import__(drivername,  fromlist=['.'.join(drivername.split('.')[:-1])])
    except ImportError:
        raise UnknownDriver("Unable to find driver.")


def to_texttable(result):
    table = texttable.Texttable()
    table.set_deco(texttable_deco)
    cols = result[0].keys()
    cols.sort()
    cols.reverse()
    table.add_rows([[col.upper() for col in cols]] + [[row[cel] for cel in cols] for row in result])
    return table.draw()
