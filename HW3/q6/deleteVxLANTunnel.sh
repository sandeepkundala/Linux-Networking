#!/bin/bashsudo
sudo ip link set dev $1 down
sudo brctl delif $2 $1
sudo ip link del dev $1

