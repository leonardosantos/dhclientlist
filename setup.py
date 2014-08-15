from setuptools import setup
from setuptools.command.install_scripts import install_scripts
from os.path import join as pjoin, splitext, split as psplit
from distutils import log
import os

BAT_TEMPLATE = r"""@echo off
set mypath=%~dp0
set pyscript="%mypath%{FNAME}"
set /p line1=<%pyscript%
if "%line1:~0,2%" == "#!" (goto :goodstart)
echo First line of %pyscript% does not start with "#!"
exit /b 1
:goodstart
set py_exe=%line1:~2%
call %py_exe% %pyscript% %*
"""


class my_install_scripts(install_scripts):
    def run(self):
        install_scripts.run(self)
        if not os.name == "nt":
            return
        for filepath in self.get_outputs():
            # If we can find an executable name in the #! top line of the script
            # file, make .bat wrapper for script.
            with open(filepath, 'rt') as fobj:
                first_line = fobj.readline()
            if not (first_line.startswith('#!') and
                    'python' in first_line.lower()):
                log.info("No #!python executable found, skipping .bat wrapper")
                continue
            pth, fname = psplit(filepath)
            froot, ext = splitext(fname)
            bat_file = pjoin(pth, froot + '.bat')
            bat_contents = BAT_TEMPLATE.replace('{FNAME}', fname)
            log.info("Making %s wrapper for %s" % (bat_file, filepath))
            if self.dry_run:
                continue
            with open(bat_file, 'wt') as fobj:
                fobj.write(bat_contents)
        install_scripts.run(self)


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this. Copied from Django's setup.py (https://github.com/django/django/blob/master/setup.py)
def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
project_dir = 'dhclientlist'

for dirpath, dirnames, filenames in os.walk(project_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.') or dirname == '__pycache__':
            del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(
    name='dhclientlist',
    version='0.0.6',
    author='Leonardo Santos',
    author_email='lsantos@inoa.com.br',
    packages=packages,
    data_files=data_files,
    scripts=["scripts/dhclientlist"],
    cmdclass={'install_scripts': my_install_scripts},
    url='https://github.com/leonardosantos/dhclientlist',
    license='LICENSE.txt',
    description=('DHClientList is a tool to get the current client list of a DHCP server. '
                 'With it one can check who is connected to the local network. '
                 'To do this one must provide the DHCP server address (IP in local network and port), username and password. '
                 'The resulting list items contains the host name, MAC address, IP and lease time.'),
    long_description=open('README.md').read(),
    install_requires=[
        "texttable==0.8.1",
        "requests==1.2.3",
        "Werkzeug==0.9.6"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
