#!/bin/bash

source constants.sh

URL="http://static.dpdk.org/rel/dpdk-"$DPDK_VERSION".tar.xz"

echo 100 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
#echo 1024 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs -o pagesize=1G nodev /mnt/huge

mkdir -p $DPDK_DIR
wget $URL -O $DPDK_DIR.tar.xz
tar -C $DPDK_DIR -xf $DPDK_DIR.tar.xz --strip-components=1
cd $DPDK_DIR

meson build
cd build
ninja
sudo ninja install
sudo ldconfig
