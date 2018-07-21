# -*- coding: ISO8859-1 -*-

import csv

class Reader:

    # file name, fields which be returneds
    def __init__(self, csvFileName, fields):
        try:
            csvfile = open(csvFileName)
            self.fileexists = True
        except FileNotFoundError:
            self.fileexists = False
            raise FileNotFoundError