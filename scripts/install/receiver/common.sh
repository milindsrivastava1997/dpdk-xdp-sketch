#!/bin/bash
sudo apt-get update
sudo apt-get install -y linux-tools-`uname -r` linux-tools-common linux-tools-generic check python3-pip python3-pyelftools libnuma-dev libmnl-dev libyaml-dev libibverbs-dev libmlx5-1 iperf cmake iftop libelf-dev gcc-multilib
sudo apt-get install -y irqbalance tcpdump clang llvm gcc iperf3 git numactl gcc binfmt-support qemu-system-common qemu-user-static
sudo pip3 install meson ninja
