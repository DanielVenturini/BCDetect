# -*- coding:ISO8859-1 -*-
import Operations as op
import subprocess as sp
from Package import Package
import NodeManager
from Except import (ScriptTestErr, InstallErr, TestErr)

class Worker():

    def __init__(self, reader, version, oneTest, clone, delete):
        self.onlyVersion = version
        self.oneTest = oneTest
        self.delete = delete
        self.reader = reader
        self.toClone = clone

        if version.__eq__('-1'):
            self.oneVersion = False
        else:
            self.oneVersion = True


    # start work
    def start(self):
        currentDirectory = sp.getstatusoutput('pwd')[1]     # pwd -> /home/user/path/to/BCDetect

        self.fullCSV = self.reader.getFull()                # get all versions of csv file
        qtdSucess = 0
        qtdFail = 0

        client_name = self.reader.client_name
        pathName = 'workspace/' + client_name

        sp.getstatusoutput('mkdir workspace/')                          # if this path doesnt exists, create

        # if --no-clone was specified
        if self.toClone:
            # clone repository
            op.clone(self.reader.urlRepo, client_name)

        # file to write
        writer = open('workspace/' + client_name+'_results.csv', 'w')
        writer.write("version, version_package, script_test, install, test, node_on_date, node_sucess\n")

        # for each version: ['3.5.0', '3.1.0', '1.0.0', '2.1.0' ...]
        keys = list(self.fullCSV.keys())
        keys.sort()                             # sort the keys
        executed = False                        # if executed only one version
        for version in keys:

            # if oneVersion was specified, skip anothers versions
            if self.oneVersion and self.onlyVersion.__eq__(version):
                executed = True
            elif self.oneVersion:
                continue                        # search to specify version

            release = self.fullCSV[version]     # get the release

            # initializing all info variables
            operation = 'INSTALL'   # current operation
            script_test = '-'       # has scripts->test
            codeInstall = '-'       # if get any err in install
            codeTest = '-'          # if get any err in test
            version_package = '-'   # the version of package in package.json
            node_on_date = '-'      # latest node version in date of release
            node_sucess = '-'       # node version that test had sucess

            # get the list of node versions and sort decrescent
            versions = list(NodeManager.nodeVersions.values())
            versions.sort()
            versions.reverse()

            posCurrentVersion = versions.index()
            try:
                op.printTableInfo('   {0}@{1}   {2}--{3}   '.format(client_name, release, release.client_timestamp, release.client_previous_timestamp))

                op.commitAll(client_name, currentDirectory)
                # change the repository to specify date
                op.checkout(pathName, release)

                input()
                # open package.json
                package = Package(pathName+'/package.json')

                # verify if package.json has test
                op.verifyTest(package)
                script_test = 'OK'

                print('    update package.json')
                op.updatePackage(release, package)

                version_package = package.get('version')

                # get the latest node version of this release
                versionPackage = NodeManager.getVersion(package, release.client_timestamp)

                try:
                    print("Test with Node {0}".format(versionPackage))

                    # install all dependencies and test in specify version package
                    operation = 'INSTALL'
                    op.npmInstall(pathName, versionPackage)
                    codeInstall = 'OK'

                    operation = 'TEST'
                    op.npmTest(pathName, versionPackage)
                    codeTest = 'OK'

                except Exception:   # try with latest version of node: 10.9.0
                    input()
                    if self.oneTest:    # if dosent want make install and test twice
                        raise

                    print('------------\n{0}: ERR\n------------\n'.format(operation))
                    print("Tentando com Node {0}".format('10.9.0'))
                    codeInstall = 'ERR'  # if get any err
                    codeTest = 'ERR'
                    op.deleteCurrentFolder('{0}/node_modules'.format(client_name))

                    operation = 'INSTALL'
                    op.npmInstall(pathName, '10.9.0')
                    codeInstall = 'OK'

                    operation = 'TEST'
                    op.npmTest(pathName, '10.9.0')
                    codeTest = 'OK'

            except FileNotFoundError as ex: # se não foi possível abrir o package.json
                qtdFail += 1
                '''
                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1
                '''
            except sp.TimeoutExpired as ex: # se a o teste ou o install demorar mais que 10 minutos
                qtdFail += 1
                '''
                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1
                '''
            except ScriptTestErr as ex:     # it's exception, but doesn't err, because package.json doesn't have scripts->test or doesn't be specified
                print('ERR: ' + str(ex).upper())

            except TestErr as ex:     # it's exception, but doesn't err, because package.json doesn't have scripts->test or doesn't be specified
                print('ERR: ' + str(ex).upper())

            except InstallErr as ex:     # it's exception, but doesn't err, because package.json doesn't have scripts->test or doesn't be specified
                print('ERR: ' + str(ex).upper())

            except Exception as ex:
                qtdFail += 1
                print('------------\n{0}: ERR: {1}\n------------\n'.format(operation, str(ex)))
                '''
                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1
                '''
            else:
                qtdSucess += 1

            #input()
            # delete folder node_modules
            if self.delete:
                op.deleteCurrentFolder('{0}/node_modules'.format(client_name))

            # version, version_package, script_test, install, test, node_on_date, node_sucess
            # save result
            writer.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}\n'.format(release.version, version_package, script_test, codeInstall, codeTest, node_on_date, node_sucess))

            if executed:        # if the specify version are executed
                break

        writer.close()
        if self.delete:
            op.deleteCurrentFolder('{0}'.format(client_name))

        print("Sucess:", qtdSucess)
        print("Fail:", qtdFail)