#!/bin/bashsudo
sudo ip link add name $1 type vxlan id $2 dev $3 remote $4 dstport 4789
sudo ip link set dev $1 up
sudo brctl addif $5 $1

