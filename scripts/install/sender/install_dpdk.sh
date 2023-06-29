#!/bin/bash

source constants.sh

URL="http://static.dpdk.org/rel/dpdk-"$DPDK_VERSION".tar.xz"

sudo apt-get update
sudo apt-get install build-essential libnuma-dev python3-pip python3-pyelftools -y
sudo pip3 install meson==$MESON_VERSION ninja

echo 100 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
#echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs -o pagesize=1G nodev /mnt/huge

wget $URL
tar xvf dpdk-$DPDK_VERSION.tar.xz
cd dpdk-$DPDK_VERSION

meson build
cd build
ninja
sudo ninja install
sudo ldconfig
