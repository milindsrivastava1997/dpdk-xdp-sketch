#!/bin/bash
NEW_KERNEL="5.15.0-72-generic"

configure_line="FORCE_SUBDIR_LIBBPF=1"
configure_file="./configure"

makefile_line="READELF\ := readelf"
makefile_file="./lib/libxdp/Makefile"

DPDK_VERSION=22.11.1
DPDK_DIR="dpdk-"$DPDK_VERSION

PKTGEN_VERSION=23.03.0
PKTGEN_DIR="pktgen-"$PKTGEN_VERSION

MESON_VERSION=0.53.2
LUA_VERSION=5.4.6
PCI="41:00.0"
