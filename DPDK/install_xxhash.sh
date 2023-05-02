#!/bin/bash

git submodule init
git submodule update

cd common/xxHash
make
sudo make install
