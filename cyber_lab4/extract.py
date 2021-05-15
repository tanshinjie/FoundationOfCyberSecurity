#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

# Tan Shin Jie
# 1003715

"""
I first ignore the first 16 bytes from letter.e, 
knowing that it contains information about the header which we were already given 

Then I identify the most repeated block in letter.e
Replace that with b'00000000'

and replace the rest with b'11111111'

The file decrypted_letter.e is the result
by combining the given header file 
and the replaced content
"""

import argparse


def getInfo(headerfile):
    h_info = b""
    with open(headerfile, "rb") as f:
        h_info = f.read()
    return h_info


def extract(infile, outfile, headerfile):
    h_info = getInfo(headerfile)
    blocks = []
    with open(infile, "rb") as f:
        content = f.read()
        content_no_header = content[16:]
        repeated = content[16:24]
        for i in range(0, len(content_no_header), 8):
            if content_no_header[i : i + 8] == repeated:
                blocks.append(b"00000000")
            else:
                blocks.append(b"11111111")
    with open(outfile, "wb") as f:
        f.write(h_info)
        f.write(b"\n")
        for i in range(len(blocks)):
            f.write(blocks[i])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract PBM pattern.")
    parser.add_argument("-i", dest="infile", help="input file, PBM encrypted format")
    parser.add_argument("-o", dest="outfile", help="output PBM file")
    parser.add_argument("-hh", dest="headerfile", help="known header file")

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print("Reading from: %s" % infile)
    print("Reading header file from: %s" % headerfile)
    print("Writing to: %s" % outfile)

    success = extract(infile, outfile, headerfile)
