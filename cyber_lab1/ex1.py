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
    # open file handles to both files
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode
    c = fin.read()  # read in file into c as a str
    # and write to fileout
    printable = string.printable
    mod = len(string.printable)

    if mode == "e" or mode == "E":
        ciphertext = ""
        for letter in c:
            ciphertext += printable[(printable.find(letter) + key) % mod]
        fout.write(ciphertext)

    if mode == "d" or mode == "D":
        plaintext = ""
        for letter in c:
            plaintext += printable[(printable.find(letter) - key) % mod]
        fout.write(plaintext)

    # close all file streams
    fin.close()
    fout.close()


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
    upperLimit = len(string.printable) - 1
    acceptanceRange = range(1, upperLimit + 1)

    if key.isnumeric() != True or int(key) not in acceptanceRange:
        print(
            "Invalid key: Key should be integer between 1 and {upperLimit}".format(
                upperLimit=upperLimit
            )
        )
    elif mode not in modeArray:
        print("Invalid mode: Mode should be 'e' for encryption or 'd' for decryption")
    else:
        doStuff(filein, fileout, int(key), mode)

    # all done

