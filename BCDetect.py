# -*- coding:ISO8859-1 -*-

import re
import sys
import subprocess

class BCDetect:

    def __init__(self):
        try:
            self.fileName = sys.argv[1]
        except IndexError:
            print("Wrong inicialization: BCDetect filename.csv")

        print("Checking if node, npm and next-update are installed.")
        try:
            self.verifyRequired('node', '^v[\d]+\.[\d]+\.[\d]+')         # check node
            self.verifyRequired('npm', '[\d]+\.[\d]+\.[\d]+')            # check npm
            self.verifyRequired('next-update', '[\d]+\.[\d]+\.[\d]+')    # check next-update
        except AttributeError:
            print("Um dos programas nao esta instalado")
        else:
            print("All required program are installed")

    # check if any required program are installed
    def verifyRequired(self, comand, regexString):
        resp = subprocess.getoutput(comand + ' -v') # execute e.g. 'node -v' and get response
        matchs = re.search(regexString, resp)        # get the string match

        version = matchs.group(0)                   # get the first result, or raise AttributeError
        print(comand + ' OK: ' + version)

BCDetect()