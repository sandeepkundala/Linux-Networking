#!/bin/bashsudo
sudo ip link set dev $1 down
sudo ip link del dev $1

