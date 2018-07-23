# -*- coding:ISO8859-1 -*-

import re
import subprocess

class Worker:

    def __init__(self, reader):
        self.reader = reader

    # start work
    def start(self):
        print("Starting worker")