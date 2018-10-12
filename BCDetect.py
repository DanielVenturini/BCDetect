# -*- coding:ISO8859-1 -*-

import re
import sys
import subprocess
from Worker import Worker
from Reader import Reader
import threading

# check if any required program are installed
def verifyRequired(prog, flag, regexString):
    print(prog + ': ', end='')

    resp = subprocess.getoutput(prog + ' ' + flag)  # execute e.g. 'node -v' and get response
    matchs = re.search(regexString, resp)           # get the strings matchs

    version = matchs.group(0)                       # get the first result, or raise AttributeError
    print(version)

def verifyPrograms():
    try:
        print("Checking if Node, NPM and GIT are installed.")
        verifyRequired('node', '-v', '^v[\d]+\.[\d]+\.[\d]+')      # check node
        verifyRequired('npm', '-v', '[\d]+\.[\d]+\.[\d]+')         # check npm
        verifyRequired('git', '--version', '[\d]\.[\d]+(\.[\d]+)*')# check git

    except IndexError:      # no has filename.csv
        print("Wrong inicialization: BCDetect filename.csv")
    except AttributeError:  # no has some required program
        print("ERR!", end='\n')
        print("Some required program aren't installed")


def verifyFile(file):
    try:
        reader = Reader(["client_name", "client_version", "client_timestamp", "client_previous_timestamp", "dependency_name",
         "dependency_type", "dependency_resolved_version"], csvFileName=file)
    except FileNotFoundError:   # file not exists
        print("File CSV/" + file + " not found!")
    except Exception:           # file dont contains the correct fields -> client_version_num_2, dependency_name
        print("File CSV/" + file + " dont have correct fields")
    else:
        print("File CSV/" + file + " is OK")
        return reader


'''
    First, verify all required programs.
    After, verify csv file
'''

class Iterator:

    def __init__(self, max):
        self.lock = threading.Lock()
        self.current = 0
        self.max = max

    def getNextPos(self):

        self.lock.acquire(blocking=True)

        self.current += 1
        if self.current >= self.max:
            current = -1
        else:
            current = self.current

        self.lock.release()

        return current

class Execute(threading.Thread):
    def __init__(self, iterator):
        threading.Thread.__init__(self)

        self.iterator = iterator

    def run(self):
        while True:

            pos = self.iterator.getNextPos()
            if pos == -1:
                return

            fileName = sys.argv[pos]+'.csv'
            try:
                reader = verifyFile(fileName)
                Worker(reader).start()
            except Exception:
                continue

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


if len(sys.argv) > 1:

    # vefiry all required programs
    verifyPrograms()

    # one iterator and four threads
    iterator = Iterator(30)
    Execute(iterator).start()
    Execute(iterator).start()
    Execute(iterator).start()
    Execute(iterator).start()

else:
    print("ERR: python3 BCDetect.py file1.csv file2.csv ...")