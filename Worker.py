# -*- coding:ISO8859-1 -*-

import re
import subprocess
from Package import Package

class Worker:

    def __init__(self, reader):
        self.reader = reader
        self.currentPackage = ''    # usage to doesnt download same package

    # start work
    def start(self):
        print("Starting worker")
        subprocess.getstatusoutput('mkdir workspace/')      # if this path dont exists, create
        subprocess.getstatusoutput('mkdir workspace/cache/')

        self.fullCSV = self.reader.getFull()
        self.package = Package()

        try:

            for fullClient in list(self.fullCSV.keys()):                # for each version: alex@1.6.0, alex@1.2.0, alex@4.0.0, ...

                client = fullClient.split('@')                          # ['alex', '1.6.0']
                client, client_version = client[0], client[1]

                print('Client {0}'.format(fullClient))
                print('    UPDATE package.json')

                for fullDependency in list(self.fullCSV[fullClient]):   # for each dependency: unified@6.1.3, retext-profanities@4.1.0, remark-message-control@4.0.0, ...

                    dependency = fullDependency.split('@')
                    dependency, dependency_version = dependency[0], dependency[1]
                    print('    {0}'.format(fullDependency))
                    self.package.update(dependency, dependency_version) # change the version of dependency in the package.json

                self.package.save()                                     # save the changes in package.json
            '''
                try:
                    if(not fullClient.__eq__(self.currentPackage)):     # dont download twice
                        self.deleteCurrentFolder()                      # delete the current package/
                        self.get(fullClient)
                        self.currentPackage = fullClient

                    self.npmInstall()                       # install alll dependents
                    self.mochaTest()                        # first, check if current version work
                    self.changeDependencyVersion(dependency, dependency_version, change='change')   # change the version of dependenc to test to latest
                    self.mochaTest(test='breaking change')  # test again
                    self.changeDependencyVersion(dependency, dependency_version, change='back')    # back to current dependency
                except Exception:
                    print('ERR')
            '''
        except subprocess.CalledProcessError:
            print('ERR')
            print('Cannot continue. Please, check the permissions of the path CSV/')
        except StopIteration:
            print("Complete...Finish")


    # npm install --no-save --only=dev
    def npmInstall(self):
        print('    npm install: ', end='', flush=True)
        if(subprocess.getstatusoutput('npm install --no-save --prefix ./workspace/package/')[0] != 0):
            raise Exception

        print('OK')


    def mochaTest(self, test='current'):
        print('    mocha {0} test: '.format(test), end='', flush=True)
        if(subprocess.getstatusoutput('mocha workspace/package/index.js')[0] != 0):
            raise Exception

        print('OK')


    # uninstall the current dependency and install the specify version
    def changeDependencyVersion(self, dependency, version, change='change'):
        print('        {0} version to '.format(change), end='', flush=True)
        # uninstall the current
        if(subprocess.getstatusoutput('npm uninstall {0} --no-save --prefix ./workspace/package/'.format(dependency))[0] != 0):
            raise Exception

        # install the specify version
        if(subprocess.getstatusoutput('npm install {0}@{1} --no-save --prefix ./workspace/package/'.format(dependency, version))[0] != 0):
            raise Exception

        print('OK')


    # download and extract source code of client
    def get(self, client):
        print('    Download: ', end='', flush=True)
        # download source code
        if(subprocess.getstatusoutput('npm pack ' + client)[0] != 0):
            print('failed download of pack ' + client)
            raise Exception

        print('OK')
        print('    Move: ', end='', flush=True)
        # move file to workspace
        if(subprocess.getstatusoutput('mv '+client.replace('@', '-')+'.tgz workspace/cache/')[0] != 0):
            print('Failed move {0}.tgz to workspace/cache/'.format(client.replace('@', '-')))
            raise subprocess.CalledProcessError

        print('OK')
        print('    Extract: ', end='', flush=True)
        # extract file to workspace
        if(subprocess.getstatusoutput('tar -xzf workspace/cache/' + client.replace('@', '-')+'.tgz -C workspace')[0] != 0):
            print('Failed extract {0} to workspace/'.format(client.replace('@', '-')))
            raise subprocess.CalledProcessError

        print('OK')


    # only delete the current package folder
    def deleteCurrentFolder(self):
        subprocess.getstatusoutput('rm -rf workspace/package/')