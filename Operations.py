import subprocess as sp

# change the git tree to specify data
def checkout(pathName, release):
    print('    checkout: ', end='', flush=True)
    client_timestamp = release.client_timestamp
    client_previous_timestamp = release.client_previous_timestamp

    if client_previous_timestamp.__eq__(''):
        if sp.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" master`'.format(pathName, client_timestamp))[0] != 0:
            raise Exception('Wrong checkout')
    else:
        if sp.getstatusoutput('cd {0}/ && git checkout `git rev-list -1 --before="{1}" --after="{2}" master`'.format(pathName, client_timestamp, client_previous_timestamp))[0] != 0:
            raise Exception('Wrong checkout')

    print('OK')


def commitAll(client_name, currentDirectory, error=0):
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ add {0}/workspace/{1}/.'.format(currentDirectory, client_name))
    sp.getstatusoutput('git --git-dir={0}/workspace/{1}/.git/ --work-tree={0}/workspace/{1}/ commit -n -m "." {0}/workspace/{1}/'.format(currentDirectory, client_name))


# npm install
def npmInstall(pathName, version):
    print('    npm install: ', end='', flush=True)
    if sp.run(['bash', 'nvm.sh', 'npm', 'install', './{0}'.format(pathName), '{0}'.format(version)], timeout=(10*60)).returncode != 0:       # if has error
        raise Exception('Wrong NPM install')

    print('------------\nINSTALL OK\n------------\n')


# npm test /workspace/path
def npmTest(pathName, version):
    print('    npm test: ', end='', flush=True)
    if sp.run(['bash', 'nvm.sh', 'npm', 'test', './{0}'.format(pathName), '{0}'.format(version)], timeout=(10*60)).returncode != 0:  # if has error, try with lattest node version
        raise Exception('Wrong NPM test')

    print('\n------------\nTEST OK\n------------\n')


# download repository
def clone(urlRepo, client_name):
    print('Clone {0} : '.format(urlRepo), end='', flush=True)
    # download source code
    if(sp.getstatusoutput('git clone ' + urlRepo + ' workspace/{0}'.format(client_name))[0] != 0):
        print('ERR')
        raise Exception

    print('OK')


# only delete the current package folder
def deleteCurrentFolder(client_name):
    sp.getstatusoutput('rm -rf workspace/{0}'.format(client_name))