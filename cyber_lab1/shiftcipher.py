#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out

# Tan Shin Jie
# 1003715

# Import libraries
import sys
import argparse
import string


def doStuff(filein, fileout, key, mode):
    # PROTIP: pythonic way
    with open(filein, mode="rb") as fin_b:
        c = fin_b.read()
        fout_b = open(fileout, mode="wb")

        if mode == "e" or mode == "E":
            ciphertext = bytearray()
            for byte in c:
                ciphertext.append(sum([byte, key]) % 256)
            fout_b.write(ciphertext)

        if mode == "d" or mode == "D":
            plaintext = bytearray()
            for byte in c:
                plaintext.append(sum([byte, -key]) % 256)
            fout_b.write(plaintext)

        fout_b.close()


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k", dest="key", help="key")
    parser.add_argument("-m", dest="mode", help="mode")

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    key = args.key
    mode = args.mode
    modeArray = ["e", "d", "E", "D"]
    acceptanceRange = range(0, 256)

    if key.isnumeric() != True or int(key) not in acceptanceRange:
        print("Invalid key: Key should be integer between 0 and 255")
    elif mode not in modeArray:
        print(
            "Invalid mode: Mode should be character 'e' for encryption or 'd' for decryption"
        )
    else:
        doStuff(filein, fileout, int(key), mode)
    # all done

