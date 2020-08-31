from colorama import Fore, Style
import subprocess as sp
from Except import (ScriptTestErr, InstallErr, TestErr)
import datetime
import json
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


def checkout_timestamp(pathName, release):
    client_timestamp = release.client_timestamp
    client_previous_timestamp = release.client_previous_timestamp

    if client_previous_timestamp.__eq__(''):
        if sp.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" master`'.format(pathName, client_timestamp))[0] != 0:
            raise Exception('Wrong checkout')
    else:
        if sp.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" --after="{2}" master`'.format(pathName, client_timestamp, client_previous_timestamp))[0] != 0:
            raise Exception('Wrong checkout')

    return getHEAD(pathName, release)


def getTag(version, tags):
    for tag in tags:
        if re.search('^v?' + version + '$', tag):
            return tag

    raise Exception('Tag {} not found'.format(version))


def checkout_tags(pathName, release, tags):
    tag = getTag(release.version, tags)

    if sp.getstatusoutput('cd {0}/ && git checkout {1}'.format(pathName, tag))[0] != 0:
        raise Exception('Wrong checkout')


# change the git tree to specify data
def checkout(pathName, release, tags):
    print('    checkout: '.format(release), end='', flush=True)

    try:
        checkout_tags(pathName, release, tags)
    except:
        # if there is not tag in the repo
        checkout_timestamp(pathName, release)

    print('OK')


def commitAll(client_name, currentDirectory):
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ add {0}/workspace/{1}/.'.format(currentDirectory, client_name))
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ commit -n -m "." {0}/workspace/{1}/'.format(currentDirectory, client_name))


# reset any files unconmmited
def cleanAndReset(client_name, currentDirectory):
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ clean -fd'.format(currentDirectory, client_name))
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ clean -fX'.format(currentDirectory, client_name))
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ clean -fx'.format(currentDirectory, client_name))

    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ reset --hard'.format(currentDirectory, client_name))


# npm install
def npmInstall(pathName, version, client_name):
    deleteCurrentFolder('{0}/node_modules'.format(client_name))
    deleteCurrentFolder('{0}/package-lock.json'.format(client_name))

    print('    npm install: ', end='', flush=True)
    if sp.run(['bash', 'nvm.sh', 'npm', 'install', './{0}'.format(pathName), '{0}'.format(version)], timeout=(10*60)).returncode != 0:       # if has error
        printTableInfo('INSTALL ERR')
        raise InstallErr(0)

    printTableInfo('INSTALL OK')


# npm test /workspace/path
def npmTest(pathName, version):
    print('    npm test: ', end='', flush=True)
    if sp.run(['bash', 'nvm.sh', 'npm', 'test', './{0}'.format(pathName), '{0}'.format(version)], timeout=(10*60)).returncode != 0:  # if has error, try with lattest node version
        printTableInfo('TEST ERR')
        raise TestErr('Wrong NPM test')

    printTableInfo('TEST OK')


def parse_url(urlRepo):
    try:
        fromgit = urlRepo.split('//')[1]
        info = fromgit.split('/')
        if info[2].endswith('.git'):
            info[2] = info[2][:-4]

        return 'https://github.com/{}/{}'.format(info[1], info[2])
    except:
        return urlRepo

# download repository
def clone(urlRepo, client_name):
    urlRepo = parse_url(urlRepo)
    sp.getstatusoutput('rm -rf workspace/{0}'.format(client_name))  # delete this path - if contain - to dont conflit with git
    sp.getstatusoutput('mkdir workspace/{0}'.format(client_name))   # if this path dont exists, create

    print('Clone {0} : '.format(urlRepo), end='', flush=True)
    # download source code
    clone_exec = sp.getstatusoutput('git clone --recurse-submodules ' + urlRepo + ' workspace/{0}'.format(client_name))
    if(clone_exec[0] != 0):
        # print('ERR')
        print(clone_exec[1])
        raise Exception('CLONE ERROR DO VENTU')

    print('OK')


# only delete the current package folder
def deleteCurrentFolder(client_name):
    sp.getstatusoutput('rm -rf workspace/{0}'.format(client_name))


# just add date in package
def addDate(release, filename='./package.json'):
    file = open(filename)
    package = json.load(file)
    package['date'] = release.client_timestamp
    json.dump(package, open(filename, 'w'), indent=2)
    #file.close()

# update all dependencies in package.json
def updatePackage(release, package, pathName):
    # for each dependencie in release
    release.sort()
    for dependencie in release.dependencies:
        # write all dependencies # json.end()
        if dependencie.changed():
            color = Fore.RED
            #print('npm uninstall {0}'.format(dependencie.name))
            #print('npm install {0}@{1}'.format(dependencie.name, dependencie.version))
        else:
            color = Fore.GREEN

        print(color + '        {0}@{1}-{2}'.format(dependencie.name, dependencie.version, dependencie.type) + Style.RESET_ALL)
        package.update(dependencie.name, dependencie.version)

    package.fileJson['date'] = release.client_timestamp
    # close package.json
    package.save()
    getHEAD(pathName, release)


# print the table
def printTableInfo(line):
    lenLine = len(line)

    print()
    print(table['1'] + table['3']*lenLine + table['2'])
    print(table['4'] + line + table['4'])
    print(table['5'] + table['3']*lenLine + table['6'])


# code 1 if package.json hasn't scripts->test
# code 0 if package.json doesn't specified test: 'echo \"Error: no test specified\" && exit 1'
def verifyTest(package, onlyVersion):
    # force install and test
    if onlyVersion:
        return

    try:
        stringTest = package.get('scripts')['test']

        if stringTest.lower().__contains__('no test specified') or stringTest.__eq__(''):
            raise ScriptTestErr(0)
    except KeyError:
        raise ScriptTestErr(1)


def formatDate(release):
    try:
        client_timestamp = release.client_timestamp

        date, time = client_timestamp.split('T')
        year, month, day = date.split('-')
        hour, minutes, seconds = time.split(':')
        seconds, mili = seconds.split('.')

        date = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), int(seconds), int(mili[:-1]))
        return date.strftime('%b %d %Y')
    except:
        return ''


def getHEAD(pathName, release):
    printTableInfo(sp.getstatusoutput('cat {0}/.git/HEAD'.format(pathName))[1] + ' - ' + formatDate(release) + ' - ' + release.client_timestamp)


def getTags(pathName):
    tags = sp.getstatusoutput('cd {0}/ && git tag'.format(pathName))[1]
    return tags.split('\n')