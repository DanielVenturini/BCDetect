# -*- coding:ISO8859-1 -*-
import Operations as op
import subprocess as sp
from Package import Package
import NodeManager

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
        version_package = ''
        currentDirectory = sp.getstatusoutput('pwd')[1]     # pwd -> /home/user/path/to/BCDetect

        self.fullCSV = self.reader.getFull()                # get all versions of csv file
        qtdSucess = 0
        qtdFail = 0

        client_name = self.reader.client_name
        pathName = 'workspace/' + client_name

        sp.getstatusoutput('mkdir workspace/')                          # if this path dont exists, create

        if self.toClone:
            sp.getstatusoutput('rm -rf workspace/{0}'.format(client_name))  # delete this path - if contain - to dont conflit with git
            sp.getstatusoutput('mkdir workspace/{0}'.format(client_name))   # if this path dont exists, create

            # clone repository
            op.clone(self.reader.urlRepo, client_name)

        # file to write
        writer = open('workspace/' + client_name+'_results.csv', 'w')
        writer.write("version, version_package, install, test\n")

        # for each version: ['3.5.0', '3.1.0', '1.0.0', '2.1.0' ...]
        keys = list(self.fullCSV.keys())
        keys.sort()                             # sort the keys
        executed = False                        # if executed only one version
        for version in keys:

            if self.oneVersion and self.onlyVersion.__eq__(version):
                executed = True
            elif self.oneVersion:
                continue                        # search to specify version

            release = self.fullCSV[version]     # get the release

            operation = 'INSTALL'
            codeInstall = 'ERR'  # if get any err
            codeTest = 'ERR'

            try:
                print('\n==={0}==={1}-{2}==={3}===NodeJs===\n'.format(release, release.client_timestamp, release.client_previous_timestamp, client_name))

                op.commitAll(client_name, currentDirectory)
                # change the repository to specify date
                op.checkout(pathName, release)

                print('    update package.json')
                # open package.json
                package = Package(pathName+'/package.json')
                
                # if want only print the test script. Comment writer.write too
                #print(package.get('script')['test'])
                #'''

                # for each dependencie in release
                release.sort()
                for dependencie in release.dependencies:
                    # write all dependencies # json.end()
                    print('        {0}@{1}-{2}'.format(dependencie.name, dependencie.version, dependencie.type))
                    package.update(dependencie.name, dependencie.version, dependencie.type)

                version_package = package.get('version')
                # close package.json
                package.save()

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

                # if want only print the test script. Comment writer.write too
                #'''
            except FileNotFoundError as ex:
                qtdFail += 1
                '''
                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1
                '''
            except sp.TimeoutExpired as ex:
                qtdFail += 1
                '''
                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1
                '''
            except Exception as ex:
                qtdFail += 1
                print('------------\n{0}: ERR\n------------\n'.format(operation))
                '''
                if input().__eq__('OK'):
                    finalCode = 'OK'
                    qtdSucess += 1
                '''
            else:
                qtdSucess += 1

            input()
            # delete folder node_modules and file package.json
            op.deleteCurrentFolder('{0}/node_modules'.format(client_name))

            # save result
            writer.write('{0}, {1}, {2}, {3}\n'.format(release.version, version_package, codeInstall, codeTest))

            if executed:        # if the specify version are executed
                break

        writer.close()
        if self.delete:
            op.deleteCurrentFolder('{0}'.format(client_name))

        print("Sucess:", qtdSucess)
        print("Fail:", qtdFail)