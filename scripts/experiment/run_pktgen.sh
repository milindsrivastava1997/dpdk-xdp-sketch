#!/bin/bash

ROOT_DIR=$1
PCI=$2
LUA_SCRIPT=$3
LOG_FILE=$4
PCAP_FILE=$5

(cd $ROOT_DIR; sudo -E ./usr/local/bin/pktgen -l 0-3 --proc-type auto --log-level 7 --file-prefix pg -a $PCI -n 4 -- -v -T -P -j -m [1-4].0 -f themes/black-yellow.theme -f $LUA_SCRIPT -l $LOG_FILE -s 0:$PCAP_FILE)
