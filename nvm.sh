#!/bin/bash

# this file is to operate NVM - Node Version Manager
# Python dosent know 'nvm', because nvm need to be load in section Linux
# if used 'subprocess.getstatusoutput('nvm --version'), Python dosent know
# but, in shell is to easy to load and to operate

# this function load the env of NVM

# Use:
# bash nvm.sh --version         -> get the version of nvm
# bash nvm.sh version x.y.z     -> get if specify version of node is installed
# bash nvm.sh install x.y.z
# bash nvm.sh npm install ./path/to/test x.y.z
# bash nvm.sh npm test ./path/to/test x.y.z

loads_nvm() {
	export NVM_DIR="$HOME/.nvm"
	[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  					# This loads nvm
	[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
}

# get the current version of nvm
nvm_version() {
    loads_nvm
	nvm --version   # here, nvm is a program
}

# get info if specify version is installed
node_version() {
    loads_nvm
    nvm version $1
}

# install the specify version $2
nvm_install() {
    loads_nvm
    nvm install $1 --force  # if the package has himself as dependencies
}

# change the version of nvm
nvm_use() {
    loads_nvm
    nvm use $1
}

# execute npm install in ./path/to/install in the node version x.y.z
npm_install() {
    nvm_use $2
    npm install --prefix $1
}

# execute npm test in ./path/to/test in the node version x.y.z
npm_test() {
    nvm_use $2
    npm test --prefix $1
}

correct_usage() {
    echo "bash nvm.sh [version] x.y.z | [install] x.y.z | npm [test|install] ./path/to/operation x.y.x"
}

# bash nvm.sh version
# bash nvm.sh install x.y.z
# bash nvm.sh npm install ./path/to/test x.y.z
# bash nvm.sh npm test ./path/to/test x.y.z

main() {
	if [ $1 = "--version" ]; then
        nvm_version
    elif [ -z $2 ]; then                # the follows need the $2, version
        correct_usage
    elif [ $1 = "version" ]; then
        node_version $2
	elif [ $1 = "install" ]; then
		nvm_install $2
	elif [ -z $3 ] || [ -z $4 ]; then   # the follows need the $3 - ./path/to - and $4 - x.y.z
	    correct_usage
    elif [ $1 = "npm" ]; then
        if [ $2 = "install" ]; then
            npm_install $3 $4
        elif [ $2 = "test" ]; then
            npm_test $3 $4
        else
            correct_usage
        fi
	else
	    correct_usage
	fi
}

main $1 $2 $3 $4