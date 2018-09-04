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
Verify in package.json the test script and search in files the files to tests.

if function='num_tests', read to csvfile and use 'npm view 'file_name' repository' go get repository URL
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
    resp = subprocess.getstatusoutput('npm view {0} repository.url'.format(packageName))    # get the repository url
    if resp[1].find('npm ERR!') == -1:                                                      # if dosent have err
        return resp[1]
    else:
        return ''

def verifyTests(fileName='../CSV/npmreleases.csv', function='worker'):
    try:
        qtdThreads = int(sys.argv[1])
    except IndexError:
        print("Use: python3 lists.py <num_thread>")
        return

    if function.__eq__('worker'):
        function = worker
    else:
        function = num_tests

    qtdLines = 3065381
    #qtdLines = 640

    #qtdLines = 80
    qtdRepo = 461640
    factor = int((qtdLines/qtdThreads)+1)   # divide for threads
    threads = list(range(0, qtdThreads))

    for i in range(0, qtdThreads):
        csvReader = csv.reader(open(fileName, 'r'), delimiter=',', quotechar='\n')
        threads[i] = threading.Thread(target=function, args=(i*factor, ((i+1)*factor)-1, csvReader,))
        threads[i].start()

    for i in range(0, qtdThreads):          # wait for each threads
        threads[i].join()

    print("TODAS AS THREADS ACABARAM")

def worker(begin, end, csvReader):
    print("Thread " + str(threading.get_ident() % 99) + " lendo de " + str(begin) + " ate " + str(end))

    for i in range(0, begin):
        csvReader.__next__()            # ignoring lines that are not mine

    client_name = ''                    # name of client
    last_client = ''                    # dont make clone twice
    client_path = ''                    # some packages haven't same name of package and repo
    client_timestamp = ''               # before this timestamp
    client_previous_timestamp = ''      # after this timestamp

    while begin < end:
        try:
            line = csvReader.__next__()             # read line
            client_name = line[0]                   # client name
            client_timestamp = line[4]              # before
            client_previous_timestamp = line[10]    # after
        except IndexError:
            # this ocorrus when first line of package, where previous_timestamp dosent exists
            print("Erro no primeiro")
            client_previous_timestamp = ''
            pass
        except StopIteration:
            # this ocorrus when get the EOF
            break

        try:
            if(not last_client.__eq__(client_name)):                # not the same repository
                print(client_name)
                client_path = clone(client_path, client_name, csvReader.line_num) # delete the last_client repository and clone client_name
                last_client = client_name                           # update the last client
        except Exception:
            continue

        checkout(client_name, client_timestamp, client_previous_timestamp)  # change the files to specify date
        findTests(client_name)                  # find files to test
        begin += 1

    subprocess.getstatusoutput('rm -rf {0}/'.format(client_name))   # delete the last repo cloned

def clone(client_path, client_name, client_name_path):
    if not client_path.__eq__(''):                                  # dont 'rm -rf /'
        print('    rm -rf {0}/'.format(client_path))
        subprocess.getstatusoutput('rm -rf {0}/'.format(client_path))       # delete the last repo

    repURL = getRepositoryURL(client_name)
    if repURL.__eq__(''):
        print('------------------------------------------------')
        raise Exception

    print('    git clone {0}'.format(repURL))          # clone the current
    subprocess.getstatusoutput('git clone {0}'.format(repURL))          # clone the current
    return getPath(repURL)

    #print("Thread " + str(threading.get_ident() % 99) + " clone: " + repURL + " - " + str(line))
    pass

def checkout(client_name, client_timestamp, client_previous_timestamp):
    # git checkout `git rev-list -1 --before="2016-12-04T13:44:16.882Z" --after="client_version_timestamp_1" master`
    comandCd = 'cd {0}/'.format(client_name)
    comandCheckout = 'git checkout `git rev-list -1 --before="' + client_timestamp + '"'

    if not client_previous_timestamp.__eq__(''):
        comandCheckout += ' --after="' + client_previous_timestamp + '" master`'
    else :
        comandCheckout += ' master`'

    # cd client_name/ && git checkout ...
    subprocess.getstatusoutput(comandCd + ' && ' + comandCheckout)
    print('    ' + comandCd + ' && ' + comandCheckout)
    #print("  checkout: " + client_timestamp + " - " + client_previous_timestamp)
    #print("  checkout: " + comandCheckout)

def findTests(client_name):
    print('    npm test fail')

def getPath(repURL):
    begin = repURL.find('/', 19)+1

    # remove '.git' if contains
    if repURL.find('.git') == -1:
        end = repURL.__len__()
    else:
        end = repURL.__len__()-4

    return repURL[begin:end]

def num_tests(begin, end, csvReader):
    print("Thread " + str(threading.get_ident()) + " comecando em " + str(begin) + " e indo ate " + str(end))

    for i in range(0, begin):
        csvReader.__next__()            # ignoring lines that are not mine

    client_name = ''  # name of client
    last_client = ''

    while begin < end:
        begin += 1

        try:
            line = csvReader.__next__()             # read line
            client_name = line[0]                   # client name

            if last_client.__eq__(client_name):     # if is the same repo
                continue

            # arent the same repo
            last_client = client_name

            '''if getRepositoryURL(client_name).__eq__(''):
                print('ERR: ' + str(failNum))
            else:
                print('OK!')'''
            print(client_name + ' : ' + getRepositoryURL(client_name))

        except StopIteration:
            return

def csvAdapter(fileName):
    fieldnames = ['client_name', 'client_timestamp', 'client_previous_timestamp', 'client_git_head', 'repository_link']    # fields in the new csv

    csvReader = csv.reader(open(fileName), delimiter=',', quotechar='\n')
    fileToWrite = open('npmreleases_reduzide.csv', 'w')
    csvWriter = csv.DictWriter(fileToWrite, fieldnames=fieldnames)
    csvWriter.writeheader()

    last_client = ''
    csvReader.__next__()            # ignore first line with fields
    i = 0
    try:
        while True:

            line = csvReader.__next__()
            if last_client.__eq__(line[0]):
                csvWriter.writerow({'client_name': line[0], 'client_timestamp': line[4], 'client_previous_timestamp': line[10], 'client_git_head': line[6], 'repository_link': ''})
            else:
                #csvWriter.writerow({'client_name': line[0], 'client_timestamp': line[4], 'client_previous_timestamp': line[10], 'client_git_head': line[6], 'repository_link': getRepositoryURL(line[0])})
                i += 1
                url = getRepositoryURL(line[0])
                csvWriter.writerow({'client_name': line[0], 'client_timestamp': line[4], 'client_previous_timestamp': line[10], 'client_git_head': line[6], 'repository_link': url})
                #print(i, ' - ', 461640, ' ' + line[0] + ' : ' + url)
                print(i)
                last_client = line[0]

    except (StopIteration, KeyboardInterrupt):
        print("Chegou no fim do arquivo")
        fileToWrite.close()

#getPackage()
#getNumDepsAndVersion()
failNum = 0                     # num of fail repo
#verifyTests(function='num_tests')
