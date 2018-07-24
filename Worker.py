# -*- coding:ISO8859-1 -*-

import re
import subprocess

class Worker:

    def __init__(self, reader):
        self.reader = reader
        self.currentPackage = ''    # usage to doesnt download same package

    # start work
    def start(self):
        print("Starting worker")
        try:

            while True:
                client, client_version, dependency, dependency_version = self.reader.next() # get info
                fullClient = "{0}@{1}".format(client, client_version)
                fullDependency = '{0}@{1}'.format(dependency, dependency_version)

                print("Client: " + fullClient)
                print("      Dependency: " + fullDependency)

                if(not fullClient.__eq__(self.currentPackage)):     # dont download twice
                    self.get(fullClient)
                    self.currentPackage = fullClient

        except subprocess.CalledProcessError:
            print('Cannot continue. Please, check the permissions of the path CSV/')
        except StopIteration:
            print("Complete...Finish")

    # download and extract source code of client
    def get(self, client):
        # download source code
        if(subprocess.getstatusoutput('npm pack ' + client)[0] != 0):
            print('failed download of pack ' + client)
            raise Exception

        # move file to workspace
        if(subprocess.getstatusoutput('mv '+client.replace('@', '-')+'.tgz workspace/')[0] != 0):
            print('Failed move {0}.tgz to workspace/'.format(client.replace('@', '-')))
            raise subprocess.CalledProcessError

        # extract file to workspace
        if(subprocess.getstatusoutput('tar -xzf workspace/' + client.replace('@', '-')+'.tgz -C workspace')[0] != 0):
            print('Failed extract {0} to workspace/'.format(client.replace('@', '-')))
            raise subprocess.CalledProcessError