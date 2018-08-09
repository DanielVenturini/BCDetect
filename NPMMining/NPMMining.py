# -*- coding:ISO-8859-1 -*-

'''
This file open the 'list_npm' file and get the packages name using regex.
For each package, its download, and check if exists 'test/...' files.

For each package found, save in the 'list_npm_test'
'''

import re
import subprocess

def getPackage(fileName='list_npm'):
    fileReader = open(fileName, 'r')
    fileWriter = open('list_npm_test', 'w')

    print('| NUM | TOTAL | PACKAGE NAME                                     | DEPD | TEST |')
    fileWriter.write('| NUM | TOTAL | PACKAGE NAME                                     | QDEP | QVER |\n')

    lines = fileReader.readlines()
    for i in range(0, len(lines)):
        try:
            # get the package name
            package = re.search('[A-z]+((\.?-?\d*)?[A-z]+)*', lines[i]).group(0)

            printNum(i, fileWriter)
            printTotal(len(lines), fileWriter)
            printName(package, fileWriter)

            getDependencies(package)
            printResp(' OK!', fileWriter)

            hasTests(package)
            printResp(' OK!', fileWriter, last=True)

            fileWriter.write(package + '\n')        # write the sucessful package

        except AttributeError:
            printResp(' ERR!', fileWriter, last=True)
        except Exception:
            printResp(' ERR!', fileWriter, last=True)

    fileReader.close()
    fileWriter.close()

def getDependencies(package):
    # get the info
    if (subprocess.getstatusoutput('npm view {0} dependencies'.format(package))[1] == ''):
        raise Exception

# npm view package files dosent work
def hasTests(package):
    resp = ''

    try:
        resp = subprocess.getstatusoutput('npm pack ' + package)[1]     # download package
        re.search('test[/]', resp).group(0)                            # search the test files
    except AttributeError:
        subprocess.getstatusoutput('rm -rf ' + getPackName(resp))       # delete the package
        raise

# from resp, get the package name
def getPackName(resp):
    name = ''
    for i in range(1, len(resp)):
        if resp[-i] == '\n':
            return name[::-1]
        else:
            name += resp[-i]

def printNum(num, fileWriter):
    max = 5                 # max of algarism
    qtdNum = len(str(num))  # qtd algarism of num

    fileWriter.write('| ' + str(num))
    print('| ' + str(num), end='')
    printSpace(max-qtdNum-1, fileWriter)

def printTotal(num, fileWriter):
    max = 7                 # max of algarism
    qtdNum = len(str(num))  # qtd algarism of num

    fileWriter.write(str(num))
    print(str(num), end='')
    printSpace(max-qtdNum, fileWriter)

def printName(name, fileWriter):
    max = 50            # max of characters
    qtdName = len(name) # max of characters of name

    fileWriter.write(name)
    print(name, end='')
    printSpace(max-qtdName, fileWriter)

def printResp(resp, fileWriter, last=False):
    max = 6
    qtdResp = len(resp) # max of characters of name

    fileWriter.write(resp)
    print(resp, end='')
    printSpace(max-qtdResp, fileWriter, last)


def printSpace(qtd, fileWriter, last=False):
    fileWriter.write((' '*qtd) + '|')
    print((' '*qtd) + '|', end='', flush=True)

    if last:
        fileWriter.write('\n')
        print()

# read 'list_npm_test' and get the number of dependencies and version for each package
def getNumDepsAndVersion(fileName='list_npm_test'):

    fileReader = open(fileName, 'r')
    fileWriter = open('list_npm_qtd', 'w')

    print('| NUM | TOTAL | PACKAGE NAME                                     | QDEP | QVER |')
    fileWriter.write('| NUM | TOTAL | PACKAGE NAME                                     | QDEP | QVER |\n')

    lines = fileReader.readlines()
    for i in range(0, len(lines)):
        package = lines[i].strip()

        printNum(i, fileWriter)
        printTotal(len(lines), fileWriter)
        printName(package, fileWriter)

        getNumDeps(package, fileWriter)
        getNumVersion(package, fileWriter)

    fileReader.close()
    fileWriter.close()


def getNumDeps(package, fileWriter):
    resp = subprocess.getstatusoutput('npm view {0} dependencies'.format(package))[1]
    qtd = resp.count(':')

    printResp(' ' + str(qtd), fileWriter)

def getNumVersion(package, fileWriter):
    resp = subprocess.getstatusoutput('npm view {0} versions'.format(package))[1]
    qtd = resp.count(',')

    printResp(' ' + str(qtd+1), fileWriter, last=True)

#getPackage()
getNumDepsAndVersion()