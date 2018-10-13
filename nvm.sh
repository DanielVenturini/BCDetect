#!/bin/bash

# this file is to operate NVM - Node Version Manager
# Python dosent know 'nvm', because nvm need to be load in section Linux
# if used 'subprocess.getstatusoutput('nvm --version'), Python dosent know
# but, in shell is to easy to load and to operate

# this function load the env of NVM

# Use:
# bash nvm.sh version
# bash nvm.sh install 6.12.0
# bash nvm.sh alias 0.11.16

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

# install the specify version $2
nvm_install() {
    loads_nvm
    nvm install $1
}

# change the version of nvm
nvm_alias() {
    loads_nvm
    nvm alias default $1
	exec bash
}

correct_usage() {
    echo "bash nvm.sh [version] | [[install|alias] x.y.x]"
}

main() {
    if [[ -e $1 || -e $2 ]]; then
        correct_usage
	elif [ $1 = "version" ]; then
        nvm_version
    elif [ -e $2 ]; then        # the follows need the $2, version
        correct_usage
	elif [ $1 = "alias" ]; then
		nvm_alias $2
	elif [ $1 = "install" ]; then
		nvm_install $2
	else
	    correct_usage
	fi
}

#bash ../../git/BCDetect/nvm.sh alias 0.12.2
main $1 $2