# -*- coding:ISO8859-1 -*-
import Operations as op
import subprocess as sp
from Package import Package
import NodeManager
from Except import (ScriptTestErr, InstallErr, TestErr, NoDependencyChange)

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
        self.currentDirectory = sp.getstatusoutput('pwd')[1]     # pwd -> /home/user/path/to/BCDetect

        self.fullCSV = self.reader.getFull()                # get all versions of csv file
        qtdSucess = 0
        qtdFail = 0

        self.client_name = self.reader.client_name
        self.pathName = 'workspace/' + self.client_name

        sp.getstatusoutput('mkdir workspace/')                          # if this path doesnt exists, create

        # if --no-clone was specified
        if self.toClone:
            # clone repository
            op.clone(self.reader.urlRepo, self.client_name)

        # file to write
        writer = open('workspace/' + self.client_name+'_results.csv', 'w')
        writer.write("version,dependency_changed,script_test,install,test,node_on_date,node_sucess\n")

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

            self.release = self.fullCSV[version]# get the release

            # initializing all info variables
            values = {
                'script_test': '-',       # has scripts->test
                'codeInstall': '-',       # if get any err in install
                'codeTest': '-',          # if get any err in test
                'node_on_date': '-',      # latest node version in date of release
                'node_sucess': '-',       # node version that test had sucess
                'dependency_changed': '-'# if none dependency has changed from the latest release
            }

            # checkout before get package
            op.commitAll(self.client_name, self.currentDirectory)
            # change the repository to specify date
            op.checkout(self.pathName, self.release)

            try:
                # get the list of node versions and sort decrescent
                package = Package(self.pathName+'/package.json')
                versions = self.getListVersions(values, package)

                # for each version of node before the release date
                for version_node in versions:
                    try:

                        self.execute(version_node, package, values)
                        values['node_sucess'] = version_node

                    except NoDependencyChange as ex:    # don't wrong
                        print('EXC: ' + str(ex).upper())
                        values['dependency_changed'] = 'NO'
                        break

                    except ScriptTestErr as ex:         # don't wrong
                        values['script_test'] = 'ERR'
                        print('EXC: ' + str(ex).upper())
                        break

                    except InstallErr as ex:            # npm install wrong
                        values['codeInstall'] = 'ERR'
                        op.deleteCurrentFolder('{0}/node_modules'.format(self.client_name))
                        print('ERR: ' + str(ex).upper())
                        # continue to next node version

                    except TestErr as ex:               # npm test wrong
                        values['node_sucess'] = version_node    # version which install has sucess
                        values['codeTest'] = 'ERR'
                        print('ERR: ' + str(ex).upper())
                        # continue to next node version

                    except Exception as ex:
                        print("Algum erro inesperado::::::::::::::::::::: " + str(ex))

                    else:
                        qtdSucess += 1          # update the count
                        break                   # quit of for statement

            except FileNotFoundError:
                pass    # do something

            #input()
            # delete folder node_modules
            if self.delete:
                op.deleteCurrentFolder('{0}/node_modules'.format(self.client_name))

            # version, dependency_changed, script_test, install, test, node_on_date, node_sucess
            # save result
            writer.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(self.release.version, values['dependency_changed'], values['script_test'], values['codeInstall'], values['codeTest'], values['node_on_date'], values['node_sucess']))

            if executed:        # if the specify version are executed
                break

        writer.close()
        if self.delete:
            op.deleteCurrentFolder('{0}'.format(self.client_name))

        print("Sucess:", qtdSucess)
        print("Fail:", qtdFail)


    # check test, install and test with the specify node version
    def execute(self, version_node, package, values):
        try:
            op.printTableInfo('   {0}@{1}   {2}--{3}   NodeJs-{4}   '.format(self.client_name, self.release, self.release.client_timestamp, self.release.client_previous_timestamp, version_node))

            # verify if any dependency has changed
            operation = 'DEP-CHANGE'
            self.release.verifyDependencyChange(self.oneVersion)
            values['dependency_changed'] = 'YES'

            operation = 'COMMIT'
            op.commitAll(self.client_name, self.currentDirectory)
            # change the repository to specify date
            operation = 'CHECKOUT'
            op.checkout(self.pathName, self.release)

            op.deleteCurrentFolder('{0}/package-lock.json'.format(self.client_name))
            #input()

            # verify if package.json has test
            operation = 'VERIFY-TEST'
            op.verifyTest(package)
            values['script_test'] = 'OK'

            print('    update package.json')
            operation = 'UPDATE-PACKAGE'
            op.updatePackage(self.release, package)

            # close package.json and save changes
            package.save()

            # install all dependencies and test in specify version package
            operation = 'INSTALL'
            if not values['codeInstall'].__eq__('OK'):
                op.npmInstall(self.pathName, version_node)

            values['codeInstall'] = 'OK'

            operation = 'TEST'
            op.npmTest(self.pathName, version_node)
            values['codeTest'] = 'OK'

        except FileNotFoundError as ex: # se não foi possível abrir o package.json
            raise
        except sp.TimeoutExpired as ex: # se a o teste ou o install demorar mais que 10 minutos
            raise
        except Exception as ex:
            print('------------\n{0}: ERR: {1}\n------------\n'.format(operation, str(ex)))
            raise


    # return the list of versions node to execute
    # in future, this will be changed to return the specify version of node
    def getListVersions(self, values, package):

        # get all node versions
        versionsNode = list(NodeManager.nodeVersions.values())
        versionsNode.sort()
        versionsNode.reverse()

        # get the node version based in date
        values['node_on_date'] = NodeManager.getVersionOnDate(self.release.client_timestamp)

        # get only versions to execute
        posCurrentVersion = versionsNode.index(values['node_on_date'])
        versions = versionsNode[posCurrentVersion:]     # get only versions to execute

        # try get the version in package.json engines->node
        # if this versions doesn't exists in versions list, insert
        try:
            versionEngines = NodeManager.getVersionOnPackage(package)

            if not versions.__contains__(versionEngines):
                versions.insert(0, versionEngines)

        except KeyError:
            pass    # do nothing

        # try with the lattest
        if not versions.__contains__('10.12.0'):
            versions.insert(0, '10.12.0')

        op.printTableInfo('NodeJS versions to run in {0}: {1}'.format(self.client_name, str(versions)))
        return versions