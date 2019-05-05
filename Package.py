# -*- coding:ISO-8859-1 -*-

'''
    This file contains the class that is responsability to open package.json
    remove all contents in the key dependencies and devDependencies and add
    all dependencies from csv to dependencies key
'''

import json

class Package:

    # the file to change is the package json
    def __init__(self, fileName='workspace/package/package.json'):
        self.fileExists = False
        self.fileName = fileName

        try:
            self.fileJson = json.load(open(self.fileName))
            self.fileExists = True
        except FileNotFoundError:
            raise

        # delete all dependencies to install only dependencies in csv file
        self.fileJson['dependencies'] = {}
        self.fileJson['devDependencies'] = {}


    # update the value of the specify key
    def update(self, dependency, version):
        if not self.fileExists:
            return

        # dependencies and devDependencies are installed in the dependencies key
        self.fileJson['dependencies'][dependency] = version


    # get the value of the key
    def get(self, key):
        if not self.fileExists:
            return None

        try:
            return self.fileJson[key]
        except KeyError:
            print('Key {0} isn\'t in the JSON object.'.format(key))
            raise


    def print(self):
        print(self.fileJson)


    # save the current state of json to a file
    def save(self):
        json.dump(self.fileJson, open(self.fileName, 'w'), indent=2)