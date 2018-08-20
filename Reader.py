# -*- coding: ISO8859-1 -*-

import csv

class Reader(Exception):

    # file name, fields which be returneds
    def __init__(self, fields, csvFileName='alex.csv'):

        try:
            self.fileExists = False
            self.fieldsExists = False
            self.hash = None

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
            print(field)
            for pos, fieldRow in enumerate(mainRow):# each field in the first line
                print('    ' + fieldRow)
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

        if(self.hash):
            return self.hash

        self.hash = {}

        try:
            while True:
                # client_name, dependency_name, client_version_timestamp_1, client_version_timestamp_2, dependency_version_max_satisf_1, dependency_version_max_satisf_2
                client, dependency, client_version_1, client_version_2, dependency_version_1, dependency_version_2 = self.next()

                '''
                print("Client: " + client)
                print("Dependency: " + dependency)
                print("client_version_1: " + client_version_1)
                print("client_version_2: " + client_version_2)
                print("dependency_version_1: " + dependency_version_1)
                print("dependency_version_2: " + dependency_version_2)
                '''

                fullClient = "{0}@{1}".format(client, client_version)
                fullDependency = '{0}@{1}'.format(dependency, dependency_version)

                try:
                    self.hash[fullClient].append(fullDependency)
                except KeyError:
                    self.hash[fullClient] = []
                    self.hash[fullClient].append(fullDependency)

        except StopIteration:
            return self.hash