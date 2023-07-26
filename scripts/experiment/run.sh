#!/bin/bash

if [[ ($# -lt 1) || ($# -gt 2) ]]; then
    echo "Illegal number of parameters"
    exit
fi

EXP_NAME=$1
if [ -z $2 ]; then
    PORT=4000
else
    PORT=$2
fi

PCAP_DIR="/scratch/"
EXP_NAME=$HOME"/"$EXP_NAME
mkdir -p $EXP_NAME


DATAPLANES=("xdp" "dpdk")
SKETCHES=("CM" "Count")
PCAPS=("equinix-nyc.dirA.20180517-130900.UTC.anon.tcp_or_udp.rewrite.pcap" "equinix-nyc.dirA.20180517-131000.UTC.anon.tcp_or_udp.rewrite.pcap" "equinix-nyc.dirA.20180517-131100.UTC.anon.tcp_or_udp.rewrite.pcap")

for dataplane in ${DATAPLANES[@]}; do
    for sketch in ${SKETCHES[@]}; do
        for pcap in ${PCAPS[@]}; do
            out_dir=$EXP_NAME"/"$dataplane"/"$sketch"/"$pcap
            mkdir -p $out_dir
            sudo python3 execute_receiver.py --output_dir $out_dir --dataplane $dataplane --sketch $sketch --pcap "$PCAP_DIR$pcap" --comm_port $PORT
            PORT=$((PORT+1))
        done
    done
done

