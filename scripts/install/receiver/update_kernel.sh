#!/bin/bash

source constants.sh

sudo apt-get update
sudo apt-get install -y linux-image-$NEW_KERNEL linux-headers-$NEW_KERNEL
sudo reboot
