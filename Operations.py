import subprocess as sp
from Except import (ScriptTestErr, InstallErr, TestErr)
import re

# to print the table formated
table = {
    '1': '┌',
    '2': '┐',
    '3': '─',
    '4': '│',
    '5': '└',
    '6': '┘',
}

# change the git tree to specify data
def checkout(pathName, release):
    print('    checkout: ', end='', flush=True)
    client_timestamp = release.client_timestamp
    client_previous_timestamp = release.client_previous_timestamp

    if client_previous_timestamp.__eq__(''):
        if sp.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" master`'.format(pathName, client_timestamp))[0] != 0:
            raise Exception('Wrong checkout')
    else:
        if sp.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" --after="{2}" master`'.format(pathName, client_timestamp, client_previous_timestamp))[0] != 0:
            raise Exception('Wrong checkout')

    print('OK')


def commitAll(client_name, currentDirectory):
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ add {0}/workspace/{1}/.'.format(currentDirectory, client_name))
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ commit -n -m "." {0}/workspace/{1}/'.format(currentDirectory, client_name))


# npm install
def npmInstall(pathName, version):
    print('    npm install: ', end='', flush=True)
    if sp.run(['bash', 'nvm.sh', 'npm', 'install', './{0}'.format(pathName), '{0}'.format(version)], timeout=(10*60)).returncode != 0:       # if has error
        printTableInfo('TEST ERR')
        raise Exception('Wrong NPM install')

    printTableInfo('INSTALL OK')


# npm test /workspace/path
def npmTest(pathName, version):
    print('    npm test: ', end='', flush=True)
    if sp.run(['bash', 'nvm.sh', 'npm', 'test', './{0}'.format(pathName), '{0}'.format(version)], timeout=(10*60)).returncode != 0:  # if has error, try with lattest node version
        printTableInfo('TEST ERR')
        raise Exception('Wrong NPM test')

    printTableInfo('TEST OK')


# download repository
def clone(urlRepo, client_name):
    print('Clone {0} : '.format(urlRepo), end='', flush=True)
    # download source code
    if(sp.getstatusoutput('git clone ' + urlRepo + ' workspace/{0}'.format(client_name))[0] != 0):
        print('ERR')
        raise Exception

    print('OK')


# only delete the current package folder
def deleteCurrentFolder(client_name):
    sp.getstatusoutput('rm -rf workspace/{0}'.format(client_name))


# print the table
def printTableInfo(line):
    lenLine = len(line)

    print()
    print(table['1'] + table['3']*lenLine + table['2'])
    print(table['4'] + line + table['4'])
    print(table['5'] + table['3']*lenLine + table['6'])

# code 1 if package.json hasn't scripts->test
# code 0 if package.json doesn't specified test: 'echo \"Error: no test specified\" && exit 1'
def verifyTest(package):
    try:
        stringTest = package.get('scripts')['test']

        if stringTest.lower().__contains__('no test specified'):
            raise ScriptTestErr(0)
    except KeyError:
        raise ScriptTestErr(1)