#!/bin/bash

# this file is to operate NVM - Node Version Manager
# Python dosent know 'nvm', because nvm need to be load in section Linux
# if 'subprocess.getstatusoutput('nvm --version'), Python dosent know
# but, in shell is to easy to load and to operate

# this function load the env of NVM
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

# change the version of nvm
nvm_change() {
    loads_nvm
	echo "Change version of NodeJs to $1"
}

# install the specify version $2
nvm_install() {
    loads_nvm
	echo "Install NodeJs $1"
}

main() {
    #loads_nvm              # shouldnt load here

	if [ $1 = "version" ]; then
		nvm_version
	elif [ $1 = "change" ]; then
		nvm_change $2
	elif [ $1 = "install" ]; then
		nvm_install $2
	fi
}

# if $1 is equal ['change'|'install], then $2 is the version
main $1 $2