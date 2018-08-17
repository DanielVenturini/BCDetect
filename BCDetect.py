# -*- coding:ISO8859-1 -*-

import re
import sys
import subprocess
from Worker import Worker
from Reader import Reader

class BCDetect:

    def __init__(self):
        self.allok = False

        try:
            print("Checking if Node, NPM, TAR and Mocha are installed.")
            self.verifyRequired('node', '-v', '^v[\d]+\.[\d]+\.[\d]+')      # check node
            self.verifyRequired('npm', '-v', '[\d]+\.[\d]+\.[\d]+')         # check npm
            self.verifyRequired('tar', '--version', '[\d]\.[\d]+(\.[\d]+)*')# check tar
            self.verifyRequired('nyc', '--version', '[\d]+\.[\d]+\.[\d]+')# check nyc

            self.reader = Reader(["client_name", "dependency_name", "client_version_timestamp_1", "client_version_timestamp_2", "dependency_version_max_satisf_2"], csvFileName=sys.argv[1])
        except IndexError:      # no has filename.csv
            print("Wrong inicialization: BCDetect filename.csv")
        except AttributeError:  # no has some required program
            print("ERR!", end='\n')
            print("Some required program aren't installed")
        except FileNotFoundError:   # file not exists
            print("File CSV/" + sys.argv[1] + " not found!")
        except Exception:           # file dont contains the correct fields -> client_version_num_2, dependency_name
            print("File CSV/" + sys.argv[1] + " dont has correct fields")
        else:
            print("File CSV/" + sys.argv[1] + " is OK")
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

BCDetect().work()