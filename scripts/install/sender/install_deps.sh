#!/bin/bash

source constants.sh

sudo apt-get update
sudo apt-get install -y build-essential libnuma-dev python3-pip python3-pyelftools tcpreplay
sudo apt-get install -y lua5.4 liblua5.4-*
sudo pip3 install meson==$MESON_VERSION ninja psutil
