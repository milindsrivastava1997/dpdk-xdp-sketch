#!/bin/bash

VERSION="5.9-0.5.6.0"
FILE="MLNX_OFED_LINUX-"$VERSION"-ubuntu22.04-x86_64"
URL="https://www.mellanox.com/downloads/ofed/MLNX_OFED-"$VERSION"/"$FILE".tgz"

wget $URL
tar xf $FILE".tgz"
cd $FILE
sudo ./mlnxofedinstall --all --dpdk --upstream-libs --force
sudo /etc/init.d/openibd restart
