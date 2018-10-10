# -*- coding:ISO8859-1 -*-

import re
import sys
import subprocess
from Worker import Worker
from Reader import Reader

class BCDetect:

    def __init__(self, file):
        self.allok = False

        try:
            print("Checking if Node, NPM and GIT are installed.")
            self.verifyRequired('node', '-v', '^v[\d]+\.[\d]+\.[\d]+')      # check node
            self.verifyRequired('npm', '-v', '[\d]+\.[\d]+\.[\d]+')         # check npm
            self.verifyRequired('git', '--version', '[\d]\.[\d]+(\.[\d]+)*')# check git

            # some lines in csv dont have the value for "dependency_version_max_satisf_2". So, install the "dependency_version_max_satisf_1"
            self.reader = Reader(["client_name", "client_version", "client_timestamp", "client_previous_timestamp", "dependency_name", "dependency_type", "dependency_version_range"], csvFileName=file)
        except IndexError:      # no has filename.csv
            print("Wrong inicialization: BCDetect filename.csv")
        except AttributeError:  # no has some required program
            print("ERR!", end='\n')
            print("Some required program aren't installed")
        except FileNotFoundError:   # file not exists
            print("File CSV/" + file + " not found!")
        except Exception:           # file dont contains the correct fields -> client_version_num_2, dependency_name
            print("File CSV/" + file + " dont have correct fields")
        else:
            print("File CSV/" + file + " is OK")
            self.allok = True

    # check if any required program are installed
    def verifyRequired(self, prog, flag, regexString):
        print(prog + ': ', end='')

        resp = subprocess.getoutput(prog + ' ' + flag)  # execute e.g. 'node -v' and get response
        matchs = re.search(regexString, resp)           # get the strings matchs

        version = matchs.group(0)                       # get the first result, or raise AttributeError
        print(version)

    # call the worker
    def work(self):
        if not self.allok:
            return

        print()
        Worker(self.reader).start()

if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        BCDetect(sys.argv[i]).work()
else:
    print("ERR: python3 BCDetect.py file1.csv file2.csv ...")