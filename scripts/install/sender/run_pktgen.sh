#!/bin/bash

source constants.sh

DPDK_DIR="../dpdk-$DPDK_VERSION"
LUA_SCRIPT="~/run_dataplane/sender.lua"

cd pktgen-$PKTGEN_VERSION
sudo -E ./usr/local/bin/pktgen -l 0-3 --proc-type auto --log-level 7 --file-prefix pg -a $PCI -n 4 -- -v -T -P -j -m [1-4].0 -f themes/black-yellow.theme -f $LUA_SCRIPT
#sudo -E ./usr/local/bin/pktgen -l 0-3 --proc-type auto --log-level 7 --file-prefix pg -a $PCI -n 4 -d $DPDK_DIR/build/drivers/librte_net_mlx5.so -d $DPDK_DIR/build/drivers/librte_common_mlx5.so -d $DPDK_DIR/build/drivers/librte_mempool_ring.so -- -v -T -P -j -m [1-4].0 -f themes/black-yellow.theme
