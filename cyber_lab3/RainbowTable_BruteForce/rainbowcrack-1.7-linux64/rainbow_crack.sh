#!/bin/bash

cd "rainbowcrack-1.7-linux64"

# Generating
./rtgen md5 ascii-32-95 1 6 0 3800 19357581879 0
./rtgen md5 ascii-32-95 1 6 1 3800 19357581879 0
./rtgen md5 ascii-32-95 1 6 2 3800 19357581879 0
./rtgen md5 ascii-32-95 1 6 3 3800 19357581879 0

# ./rtsort .

# Cracking
# ./rcrack /home/shinjie/Desktop/cyber_lab3/rainbowcrack-1.7-linux64/. -l ../hash5_salted.txt