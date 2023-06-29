#!/bin/bash

source constants.sh

curl -R -O http://www.lua.org/ftp/lua-"$LUA_VERSION".tar.gz
tar xvf lua-"$LUA_VERSION".tar.gz
cd lua-$LUA_VERSION
make all test
sudo make install
