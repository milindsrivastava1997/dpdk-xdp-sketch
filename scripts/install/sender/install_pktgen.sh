#!/bin/bash

source constants.sh

URL="https://git.dpdk.org/apps/pktgen-dpdk/snapshot/pktgen-"$PKTGEN_VERSION".tar.xz"

mkdir -p $PKTGEN_DIR
wget $URL -O $PKTGEN_DIR.tar.xz
tar -C $PKTGEN_DIR -xf $PKTGEN_DIR.tar.xz --strip-components=1
cd $PKTGEN_DIR
sudo ./tools/pktgen-build.sh buildlua
