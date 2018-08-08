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

    lines = fileReader.readlines()
    for i in range(0, len(lines)):
        try:
            # get the package name
            package = re.search('[A-z]+((\.?-?\d*)?[A-z]+)*', lines[i]).group(0)
            print(str(i) + ' - ' + str(len(lines)) + ' ' + package + ': ', end='', flush=True)

            # get the info
            if(subprocess.getstatusoutput('npm view {0} dependencies'.format(package))[1] == ''):
                print('ERR!')
                continue    # dosent have dependents

            # baixa e verifica se tem tests files
            print('OK!')

        except AttributeError:
            pass

    fileReader.close()
    fileWriter.close()

getPackage()