# -*- coding: ISO8859-1 -*-

import csv

class Reader(Exception):

    # file name, fields which be returneds
    def __init__(self, csvFileName, fields):

        try:
            csvfile = open('CSV/' + csvFileName)    # open file which is csv reader
            self.csvReader = csv.reader(csvfile, delimiter=',', quotechar='\n')
            self.fileexists = True

            self.chechFields(fields)                # check fields -> client_version_num_2, dependency_name,
            self.fieldsexists = True
        except FileNotFoundError:
            self.fileexists = False
            raise
        except Exception:
            self.fieldsexists = False
            raise


    # check if fields exists in the first row of the csv
    def chechFields(self, fields):

        self.formalize(fields)
        mainRow = self.csvReader.__next__()         # get first line which contains all fields

        for field in fields:
            if field not in mainRow:
                raise Exception('NoFieldsFound')

    # insert "" in all fields
    def formalize(self, fields):
        for i in range(0, len(fields)):
            fields[i] = '\"' + fields[i] + '\"'