#!/bin/bash

if [`whoami` != "root"]
then
	echo "This script must be run as root."
	exit 1
fi

apt-get update
apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils python3
apt-get install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev
apt-get install libboost-all-dev
contrib/install_db4.sh pwd
export BDB_PREFIX='/db4'
./autogen.sh 
./configure BDB_LIBS="-L${BDB_PREFIX}/lib -ldb_cxx-4.8" BDB_CFLAGS="-I${BDB_PREFIX}/include"
make
