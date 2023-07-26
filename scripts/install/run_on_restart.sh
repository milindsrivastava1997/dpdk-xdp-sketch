#!/bin/bash

echo 100 | sudo tee /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
sudo mkdir -p /mnt/huge
sudo mount -t hugetlbfs -o pagesize=1G nodev /mnt/huge
