# -*- coding:ISO-8859-1 -*-

import subprocess
import re

'''
This file contains the implementations of the functions that are
responsable to change the node version.
'''

# 0.11.16 -> 2015-01-14
# 1.8.2   -> 2015-05-04
# 2.5.0   -> 2015-08-04
# 3.3.1   -> 2015-09-08
# 4.2.2   -> 2015-10-29
# 5.11.1  -> 2016-04-26
# 6.9.2   -> 2016-10-25
# 7.10.1  -> 2017-05-30
# 8.9.0   -> 2017-10-31
# 9.11.2  -> 2018-04-24
# 10.12.0 -> 2018-10-10
# 12.18.3 -> 2020-04-21

nodeDates = ['2015-01-14', '2015-05-04', '2015-08-04', '2015-09-08', '2015-10-29',
             '2016-04-26', '2016-10-25', '2017-05-30', '2017-10-31', '2018-04-24', '2018-10-10', '2020-04-21']

nodeVersions = {'2015-01-14':'0.11.16', '2015-05-04':'1.8.2', '2015-08-04':'2.5.0', '2015-09-08':'3.3.1', '2015-10-29':'4.2.2',
                '2016-04-26':'5.11.1', '2016-10-25':'6.9.2', '2017-05-30':'7.10.1', '2017-10-31':'8.9.0', '2018-04-24':'9.11.2', '2018-10-10': '10.12.0', '2020-04-21': '12.18.3'}

# get the latest version based in current version
def getVersionOnVersion(version):

    versions = list(nodeVersions.values())  # get all versions
    versions.sort()                         # sort the version

    for i, lVersion in enumerate(versions): # in each version
        if lVersion > version:              # if latest version is minor than version
            return versions[i]              # return the previous version

    return versions[-1]                     # return the last version


# check if version is installed
def isInstalled(version):
    if subprocess.getstatusoutput('bash nvm.sh version {0}'.format(version))[1].__eq__('N/A'):
        return False
    else:
        return True


# install in local machine the specify version of node
def installVersion(version):
    subprocess.getstatusoutput('bash nvm.sh install {0}'.format(version))


# format the output
def printLine(num, version):

    if num < 10:
        line = str(num) + '  - '
    else:
        line = str(num) + ' - '

    line += version
    i = 8 - len(version)
    line += (' ' * i)

    line += ': '
    print(line, end='', flush=True)


# install all required versions of node js
def installAllVersions():

    print('\nInstall all - 11 - required versions of NodeJs')
    for i, date in enumerate(nodeDates):

        version = nodeVersions[date]
        printLine(i+1, version)

        if not isInstalled(version):
            installVersion(version)

        print("OK")

    print('')

# based in date, get the latest version
# of Node before this date
def getVersionOnDate(date):

    for dateNode in nodeDates:
        if date < dateNode:                 # if date release is menor than date node
            return nodeVersions[dateNode]   # get the node version in this date

    return nodeVersions[nodeDates[-1]]      # latest version


# return the version if there is in package
# if the developer put the version in 'engines'->'node', get this
def getVersionOnPackage(package):
    engines = package.get('engines')        # get the map engines, if exists, or raise KeyError
    version = engines['node']               # get the version of node

    version = re.search('[\d]+', version).group(0)
    version = getVersionOnVersion(version)  # get last version of this version

    return version


# return the version of NodeJs if there is in package.json based in date
# and install the current version of node if version isnt installed
def getVersion(package, date):
    # first, try to get the version on the package.json
    # after, get based in the date of release
    version = ' '
    try:
        version = getVersionOnPackage(package)

        if not isInstalled(version):
            installVersion(version)             # try install

    except (KeyError, IndexError, AttributeError, TypeError):
        version = getVersionOnDate(date)

    return version