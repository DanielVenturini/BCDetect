# -*- coding:ISO8859-1 -*-
import sys
import subprocess
from Package import Package

class Worker:

    def __init__(self, reader):
        self.reader = reader

    # start work
    def start(self):
        version_package = ''

        self.fullCSV = self.reader.getFull()                # get all versions of csv file
        qtdSucess = 0
        qtdFail = 0

        client_name = self.reader.client_name
        pathName = 'workspace/' + client_name

        subprocess.getstatusoutput('mkdir workspace/')                          # if this path dont exists, create
        subprocess.getstatusoutput('mkdir workspace/{0}'.format(client_name))   # if this path dont exists, create

        print('PACKAGE: ' + self.reader.csvFileName)
        # clone repository
        self.clone(self.reader.urlRepo, client_name)

        # file to write
        writer = open('workspace/' + client_name+'_results.csv', 'w')
        writer.write("version, version_package, result\n")

        # for each version: ['3.5.0', '3.1.0', '1.0.0', '2.1.0' ...]
        keys = list(self.fullCSV.keys())
        keys.sort()                             # sort the keys
        for version in keys:
            finalCode = 'ERR'                   # if get any err
            release = self.fullCSV[version]     # get the release

            try:
                print('\n=================={0}=================={1}-{2}=========================\n'.format(release, release.client_timestamp, release.client_previous_timestamp))

                commitAll(client_name)
                # change the repository to specify date
                self.checkout(pathName, release)

                # get the package without changes
                subprocess.getstatusoutput('cp workspace/{0}/package.json workspace/'.format(client_name))

                #input('')
                print('    update package.json')
                # open package.json
                package = Package(pathName+'/package.json')

                # for each dependencie in release
                for dependencie in release.dependencies:
                    # write all dependencies # json.end()
                    print('        {0}@{1}-{2}'.format(dependencie.name, dependencie.version, dependencie.type))
                    package.update(dependencie.name, dependencie.version, dependencie.type)

                version_package = package.get('version')
                # close package.json
                package.save()

                #input('')
                # install all dependencies
                self.npmInstall(pathName)

                #input('')
                # npm test
                self.npmTest(pathName)

            except FileNotFoundError as ex:
                qtdFail += 1
                print('ERR FNF: ' + str(ex))

                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1

            except subprocess.TimeoutExpired as ex:
                qtdFail += 1
                print("ERR: " + str(ex))

                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1

            except Exception as ex:
                qtdFail += 1
                print("ERR: " + str(ex))

                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1

            else:
                qtdSucess += 1
                finalCode = 'OK'

            #input('')
            # delete folder node_modules and file package.json
            self.deleteCurrentFolder('{0}/node_modules'.format(client_name))
            self.deleteCurrentFolder('{0}/package.json'.format(client_name))

            #input('')
            # save result
            writer.write('{0}, {1}, {2}\n'.format(release.version, version_package, finalCode))
            # get the package without changes
            subprocess.getstatusoutput('rm workspace/{0}/package.json'.format(client_name))
            subprocess.getstatusoutput('cp workspace/package.json workspace/{0}/'.format(client_name))

        writer.close()
        self.deleteCurrentFolder('{0}'.format(client_name))
        self.deleteCurrentFolder('package.json')

        print("Sucess:", qtdSucess)
        print("Fail:", qtdFail)

    # change the git tree to specify data
    def checkout(self, pathName, release):
        print('    checkout: ', end='', flush=True)
        client_timestamp = release.client_timestamp
        client_previous_timestamp = release.client_previous_timestamp

        if client_previous_timestamp.__eq__(''):
            if subprocess.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" master`'.format(pathName, client_timestamp))[0] != 0:
                raise Exception('Wrong checkout')
        else:
            if subprocess.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" --after="{2}" master`'.format(pathName, client_timestamp, client_previous_timestamp))[0] != 0:
                raise Exception('Wrong checkout')

        print('OK')


    def commitAll(self, client_name):
        subprocess.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ add {0}/workspace/{1}/*'.format('/home/venturini/git/BCDetect', client_name))
        subprocess.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ commit -m "." {0}/workspace/{1}/'.format('/home/venturini/git/BCDetect', client_name))

    # npm install
    def npmInstall(self, pathName):
        print('    npm install: ', end='', flush=True)
        if subprocess.run(['npm', 'install', '--prefix', './{0}'.format(pathName)], timeout=(10*60)).returncode != 0:
            raise Exception('Wrong NPM install')

        print('OK')


    # npm test /workspace/path
    def npmTest(self, pathName):
        print('    npm test: ', end='', flush=True)
        if subprocess.run(['npm', 'test', '--prefix', './{0}'.format(pathName)], timeout=(5*60)).returncode != 0:
            raise Exception('Wrong NPM test')

        print('OK')


    # download repository
    def clone(self, urlRepo, client_name):
        print('Clone: ', end='', flush=True)
        # download source code
        if(subprocess.getstatusoutput('git clone ' + urlRepo + ' workspace/{0}'.format(client_name))[0] != 0):
            print('ERR')
            raise Exception

        print('OK')


    # only delete the current package folder
    def deleteCurrentFolder(self, client_name):
        subprocess.getstatusoutput('rm -rf workspace/{0}'.format(client_name))