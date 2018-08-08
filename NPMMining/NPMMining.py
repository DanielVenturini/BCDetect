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
    lines = fileReader.readlines()
    for i in range(0, len(lines)):
        try:
            # get the package name
            package = re.search('[A-z]+((\.?-?\d*)?[A-z]+)*', lines[i]).group(0)

            printNum(i)
            printTotal(len(lines))
            printName(package)

            getDependencies(package)
            printResp(' OK!')

            hasTests(package)
            printResp(' OK!', last=True)

            fileWriter.write(package + '\n')        # write the sucessful package

        except AttributeError:
            printResp(' ERR!', last=True)
        except Exception:
            printResp(' ERR!', last=True)

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
        re.search('test', resp).group(0)                                # search the test files
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

def printNum(num):
    max = 5                 # max of algarism
    qtdNum = len(str(num))  # qtd algarism of num

    print('| ' + str(num), end='')
    printSpace(max-qtdNum-1)

def printTotal(num):
    max = 7                 # max of algarism
    qtdNum = len(str(num))  # qtd algarism of num

    print(str(num), end='')
    printSpace(max-qtdNum)

def printName(name):
    max = 50            # max of characters
    qtdName = len(name) # max of characters of name

    print(name, end='')
    printSpace(max-qtdName)

def printResp(resp, last=False):
    max = 6
    qtdResp = len(resp) # max of characters of name

    print(resp, end='')
    printSpace(max-qtdResp, last)


def printSpace(qtd, last=False):
    print((' '*qtd) + '|', end='', flush=True)

    if last:
        print()

getPackage()