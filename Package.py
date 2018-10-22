# -*- coding:ISO-8859-1 -*-

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

    # update the value of the specify key
    def update(self, dependency, version, type):
        if not self.fileExists:
            return

        try:
            if type.__eq__('dependency'):
                self.fileJson['dependencies'][dependency] = version
            else:
                self.fileJson['devDependencies'][dependency] = version
        except KeyError:
            print('Key \"dependencies/devDependencies\" or ' + dependency + ' isent in package.json')


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
        json.dump(self.fileJson, open(self.fileName, 'w'), indent=2, sort_keys=True)