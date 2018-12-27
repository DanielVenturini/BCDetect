# -*- coding:ISO8859-1 -*-

import re
import sys
import subprocess
from Worker import Worker
from Reader import Reader
import threading
import NodeManager

# check if any required program are installed
def verifyRequired(prog, call, flag, regexString):
    print(prog + ': ', end='')

    resp = subprocess.getoutput(call + ' ' + flag)  # execute e.g. 'node -v' and get response
    matchs = re.search(regexString, resp)           # get the strings matchs

    version = matchs.group(0)                       # get the first result, or raise AttributeError
    print(version)

def verifyPrograms():
    try:
        print("Checking if Node, NPM, GIT and NVM are installed.")
        verifyRequired('NodeJs', 'node', '-v', '^v[\d]+\.[\d]+\.[\d]+')         # check node
        verifyRequired('NPM', 'npm', '-v', '[\d]+\.[\d]+\.[\d]+')               # check npm
        verifyRequired('Git', 'git', '--version', '[\d]\.[\d]+(\.[\d]+)*')      # check git
        verifyRequired('NVM', 'bash nvm.sh', '--version', '[\d]\.[\d]+\.[\d]+') # check nvm
    except AttributeError:  # no has some required program
        print("ERR!", end='\n')
        print("Some required program aren't installed")
        raise

    print()

def verifyFile(file):
    try:
        reader = Reader(["client_name", "client_version", "client_timestamp", "client_previous_timestamp", "dependency_name",
         "dependency_type", "dependency_resolved_version", "dependency_resolved_version_change"], csvFileName=file)
    except FileNotFoundError:   # file not exists
        print("File CSV/" + file + " not found!")
        raise
    except Exception:           # file dont contains the correct fields -> client_version_num_2, dependency_name
        print("File CSV/" + file + " dont have correct fields")
        raise
    else:
        print("File CSV/" + file + " is OK")
        return reader


'''
    First, verify all required programs.
    After, verify csv file
'''

# each thread get one pos in argv
# to get file1.csv, file2.csv, file3.csv ...
class Iterator:

    def __init__(self, max):
        self.lock = threading.Lock()
        self.current = 0
        self.max = max

    def getNextPos(self, argv):

        self.lock.acquire(blocking=True)
        current = -1

        while self.current < self.max-1:            # enquanto nao chegar no maximo
            self.current += 1                       # avança

            if argv[self.current].__eq__('--only'): # if has '--only', jump this flag
                self.current += 1                   # jump the version too
                continue                            # go at begin

            if argv[self.current].__eq__('--node-i'):# dont verify node
                continue

            if argv[self.current].__eq__('--no-del'):   # dont delete pathClient when finish
                continue

            if argv[self.current].__eq__('--no-clone'): # dont clone pathClient, because path is there
                continue

            if self.current >= self.max:            # if is end
                current = -1
            else:
                current = self.current              # then, get the position

            break

        self.lock.release()

        return current


class Execute(threading.Thread):
    def __init__(self, iterator):
        threading.Thread.__init__(self)

        self.iterator = iterator

    # return True, if flag is given, or False if dont
    def getFlag(self, flag):
        try:
            sys.argv.index(flag)

            # flag with specify value
            if flag.__eq__('--only'):
                return sys.argv[sys.argv.index(flag)+1]
            else:
                return True

        except ValueError:
            # flag with specify value
            if flag.__eq__('--only'):
                return '-1'
            else:
                return False

    def run(self):
        while True:

            pos = self.iterator.getNextPos(sys.argv)
            if pos == -1:
                return

            fileName = sys.argv[pos]+'.csv'

            # execute the install and test in specify version
            version = self.getFlag('--only')

            # dont clone. The path is there
            clone = not self.getFlag('--no-clone')

            # dont delete the pathClient when finish
            delete = not self.getFlag('--no-del')

            try:
                reader = verifyFile(fileName)
                Worker(reader, version, clone, delete).start()
            except Exception as ex:
                print("Exception: " + str(ex))
                continue

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def printHelp():
    print('|-----------------------------------------------------------------------|')
    print('|        BCDetect     -     BREAK CHANGE DETECT    -    B R A S I L     |')
    print('|-----------------------------------------------------------------------|')
    print('|USE: python3 BCDetect.py [file1.csv, file2.csv, ...] [flags]           |')
    print('|-----------------------------------------------------------------------|')
    print('|Flags:                                                                 |')
    print('|    --node-i     : install all major versions of NodeJS.               |')
    print('|    --no-clone   : if the repo was cloned in CSV/repo, don\'t clone.    |')
    print('|    --no-del     : don\'t delete CSV/repo when finish.                  |')
    print('|    --only x.y.z : execute "npm [install | test]" only in this version.|')
    print('|-----------------------------------------------------------------------|')

if sys.argv.__contains__('--help') or sys.argv.__contains__('-h'):
    printHelp()
    exit(1)

if len(sys.argv) > 1:
    # vefiry all required programs
    try:

        if sys.argv.__contains__('--node-i'):   # dont verify node
            NodeManager.installAllVersions()

        verifyPrograms()

        # one iterator and four threads
        iterator = Iterator(len(sys.argv))
        Execute(iterator).start()
        Execute(iterator).start()
        Execute(iterator).start()
        Execute(iterator).start()
    except AttributeError:
        pass

else:
    print("USE: python3 BCDetect.py [file1.csv, file2.csv, ...] [flags]")
