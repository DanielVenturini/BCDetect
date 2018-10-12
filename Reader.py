# -*- coding: ISO8859-1 -*-

import csv
from Dependency import Dependency
from Release import Release

'''
This file contains the implementations of the functions that are
responsible to read the target file and return all values.
'''

class Reader():

    # file name, fields which be returneds
    def __init__(self, fields, csvFileName):

        try:
            self.fileExists = False
            self.fieldsExists = False
            self.hash = None
            self.csvFileName = csvFileName

            csvfile = open('CSV/' + csvFileName)    # open file which is csv reader
            self.csvReader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            self.fileExists = True

            self.posFields = []                     # store the position of each field
            self.chechFields(fields)                # check fields -> client_version_num_2, dependency_name,
            self.fieldsExists = True
        except FileNotFoundError:                   # file isent in folder 'CSV/'
            self.fileexists = False
            raise
        except Exception:                           # all fields isent in file
            self.fieldsExists = False
            raise


    # check if fields exists in the first row of the csv
    def chechFields(self, fields):

        #self.formalize(fields)
        mainRow = self.csvReader.__next__()         # get first line which contains all fields
        self.urlRepo = mainRow[-1]                  # url to clone repository

        for field in fields:                        # each required field
            for pos, fieldRow in enumerate(mainRow):# each field in the first line
                if(field.__eq__(fieldRow)):
                    self.posFields.append(pos)
                    break
                elif(pos == len(mainRow)-1):        # last position
                    raise Exception('NoFieldsFound')# if not found the field, raise exception


    # get the nexts values for each field
    # raise StopIteration when dont has more lines
    def next(self):
        if(not self.fieldsExists or not self.fileExists):
            raise StopIteration

        line = self.csvReader.__next__()            # get next line
        values = []                                 # store the values

        for i in self.posFields:
            values.append(line[i].replace('"', '')) # get each value

        return values


    # insert "" in all fields
    def formalize(self, fields):
        for i in range(0, len(fields)):
            fields[i] = '\"' + fields[i] + '\"'


    # get the hash {'version': release}
    def getFull(self):
        if(not self.fieldsExists or not self.fileExists):
            raise StopIteration

        if(self.hash):
            return self.hash

        self.hash = {}
        self.client_name = ''

        try:
            while True:
                client_name, client_version, client_timestamp, client_previous_timestamp, dependency_name, dependency_type, dependency_resolved_version = self.next()

                self.client_name = client_name
                # name, version, type
                dependency = Dependency(dependency_name, dependency_resolved_version, dependency_type)

                try:
                    # release.addDependency
                    release = self.hash[client_version]                 # get the release

                    if release.client_previous_timestamp.__eq__(''):    # if client_previous_timestamp is null
                        release.client_previous_timestamp = client_previous_timestamp

                    release.addDependency(dependency)
                except KeyError:                                        # if is first release in csv file
                    release = Release(client_version, client_timestamp, client_previous_timestamp)  # create new release
                    release.addDependency(dependency)                   # add dependency
                    self.hash[client_version] = release                 # insert in hash

        except StopIteration:
            return self.hash