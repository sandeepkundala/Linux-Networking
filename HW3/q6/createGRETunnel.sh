#!/bin/bashsudo
sudo ip tunnel add $1 mode gre local $2 remote $3
sudo ip link set dev $1 up
sudo ip route add $4 dev $1

