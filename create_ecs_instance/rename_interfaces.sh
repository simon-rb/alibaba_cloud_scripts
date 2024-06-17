#!/bin/bash

# Bring down both interfaces
ip link set eth0 down
ip link set eth1 down

# Rename the interfaces using a temporary name
ip link set eth0 name output
ip link set eth1 name input1

# Bring up the renamed interfaces
ip link set output up
ip link set input1 up