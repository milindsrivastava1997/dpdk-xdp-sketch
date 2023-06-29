#!/bin/bash

source constants.sh

URL="https://git.dpdk.org/apps/pktgen-dpdk/snapshot/pktgen-"$PKTGEN_VERSION".tar.xz"

wget $URL
tar xvf pktgen-$PKTGEN_VERSION.tar.xz
cd pktgen-$PKTGEN_VERSION
sudo ./tools/pktgen-build.sh build buildlua
