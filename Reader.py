# -*- coding: ISO8859-1 -*-

import csv

class Reader(Exception):

    # file name, fields which be returneds
    def __init__(self, csvFileName, fields):

        try:
            self.fileExists = False
            self.fieldsExists = False

            csvfile = open('CSV/' + csvFileName)    # open file which is csv reader
            self.csvReader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            self.fileExists = True

            self.posFields = []                     # store the position of each field
            self.chechFields(fields)                # check fields -> client_version_num_2, dependency_name,
            self.fieldsExists = True
        except FileNotFoundError:
            self.fileexists = False
            raise
        except Exception:
            self.fieldsExists = False
            raise

    # check if fields exists in the first row of the csv
    def chechFields(self, fields):

        self.formalize(fields)
        mainRow = self.csvReader.__next__()         # get first line which contains all fields

        for field in fields:                        # each required field
            for pos, fieldRow in enumerate(mainRow):# each field in the first line
                if(field.__eq__(fieldRow)):
                    self.posFields.append(pos)
                    break
                elif(pos == len(mainRow)-1):        # last position
                    raise Exception('NoFieldsFound')# if not found the field, raise exception

        #print(self.posFields)

    # get the nexts values for each field
    # raise StopIteration when dont has more lines
    def next(self):
        if(not self.fieldsExists or not self.fileExists):
            raise StopIteration

        line = self.csvReader.__next__()            # get next line
        values = []                                 # store the values

        for i in self.posFields:
            values.append(line[i].replace('"', '')) # get each value

        #print(values)
        return values


    # insert "" in all fields
    def formalize(self, fields):
        for i in range(0, len(fields)):
            fields[i] = '\"' + fields[i] + '\"'


    # get the hash {'package@version': ['dep1@version', 'dep2@version']}
    def getFull(self):
        if(not self.fieldsExists or not self.fileExists):
            raise StopIteration

        hash = {}

        try:
            while True:
                client, client_version, dependency, dependency_version = self.next()

                fullClient = "{0}@{1}".format(client, client_version)
                fullDependency = '{0}@{1}'.format(dependency, dependency_version)

                try:
                    hash[fullClient].append(fullDependency)
                except KeyError:
                    hash[fullClient] = []
                    hash[fullClient].append(fullDependency)

        except StopIteration:
            return hash
