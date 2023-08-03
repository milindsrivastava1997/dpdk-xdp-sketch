#!/bin/bash
DIR="/scratch"
sudo mkdir $DIR
sudo /usr/local/etc/emulab/mkextrafs.pl $DIR
sudo rm -rf $DIR/lo*
sudo chown -R milindsr:cloudmigration-P $DIR
mkdir -p $DIR
