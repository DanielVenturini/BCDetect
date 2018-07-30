# -*- coding:ISO-8859-1 -*-

import json

class Package:

    # the file to change is the package json
    def __init__(self, fileName='workspace/package/package.json'):
        self.fileExists = False
        self.fileName = fileName

        try:
            self.fileJson = json.load(open('workspace/test.json'))
            self.fileExists = True
        except FileNotFoundError:
            raise

    # update the value of the specify key
    def update(self, key, value):
        if(not self.fileExists):
            return

        try:
            self.fileJson[key] = value
        except KeyError:
            print('Key {0} isn\'t in the JSON object.'.format(key))

    # get the value of the key
    def get(self, key):
        if(not self.fileExists):
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
        json.dump(self.fileJson, open(self.fileName, 'w'))