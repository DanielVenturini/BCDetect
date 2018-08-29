# -*- coding:ISO-8859-1 -*-

'''
getPackage() - open the 'list_npm' file and get the packages name using regex.
For each package, its download, and check if exists 'test/...' files.

For each package found, save in the 'list_npm_test'
'''
from ctypes import c_short

'''
getNumDepsAndVersion() - after get the list of packages with tests files, read the file 'list_npm_test.
For each package, get the quantity of dependencies and versions and save in the 'list_npm_qtd'
'''

'''
verifyTests() - read to csv file and download from GitHub the source code. Then, use the checkout to change files.
Verify in package.json the test script and search in files the files to tests
'''

import re
import csv
import sys
import threading
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

def getRepositoryURL(packageName):
    try:
        resp = subprocess.getstatusoutput('npm view {0} repository'.format(packageName))    # get the JSON with type and url
        regex = re.compile('(\.com\/[@a-zA-Z0-9_]+([\/@\.a-zA-Z0-9_-])+)')                  # to find '/user/repository'

        if regex.search(resp[1]).group(0).__eq__('/home/venturini'):
            return ''
        else:
            return 'https://github' + regex.search(resp[1]).group(0)
    except AttributeError:
        return ''     # if hasnt repository

def verifyTests(fileName='../CSV/npmreleases.csv'):
    try:
        qtdThreads = int(sys.argv[1])
    except IndexError:
        print("Use: python3 lists.py <num_thread>")
        return

    #qtdLines = 3065381
    qtdLines = 640
    qtdRepo = 461640
    factor = int((qtdLines/qtdThreads)+1)   # divide for threads

    for i in range(0, qtdThreads):
        csvReader = csv.reader(open(fileName, 'r'), delimiter=',', quotechar='\n')
        t = threading.Thread(target=worker, args=(i*factor, ((i+1)*factor)-1, csvReader,))
        t.start()

def worker(begin, end, csvReader):
    print("Thread " + str(threading.get_ident() % 99) + " lendo de " + str(begin) + " ate " + str(end))

    for i in range(0, begin):
        csvReader.__next__()            # ignoring lines that are not mine

    last_client = ''                    # dont make clone twice
    client_name = ''                    # name of client
    client_timestamp = ''               # after this timestamp
    client_previous_timestamp = ''      # before this timestamp

    while begin < end:
        try:
            line = csvReader.__next__()             # read line
            client_name = line[0]                   # client name
            client_timestamp = line[4]              # after
            client_previous_timestamp = line[10]    # before
        except IndexError:
            # this ocorrus when first line of package, where previous_timestamp dosent exists
            print("Erro no primeiro")
            client_previous_timestamp = ''
            pass
        except StopIteration:
            print("saiu por aqui")
            # this ocorrus when get the EOF
            break

        if(not last_client.__eq__(client_name)):    # not the same repository
            last_client = client_name               # update the last client
            clone(last_client, client_name, csvReader.line_num) # delete the last_client repository and clone client_name

        #checkout(client_name, client_timestamp, client_previous_timestamp)  # change the files to specify date
        #findTests(client_name)                  # find files to test
        begin += 1

    # git checkout `git rev-list -1 --before="2016-12-04T13:44:16.882Z" --after="client_version_timestamp_1" master`

def clone(last_client, client_name, line):
    respURL = getRepositoryURL(client_name)
    if respURL.__eq__(''):
        respURL = client_name

    print("Thread " + str(threading.get_ident() % 99) + " clone: " + respURL + " - " + str(line))
    pass

def checkout(client_name, client_timestamp, client_previous_timestamp):
    print("  checkout: " + client_timestamp + " - " + client_previous_timestamp)

def findTests(client_name):
    print('  npm test')

#getPackage()
#getNumDepsAndVersion()
verifyTests()
