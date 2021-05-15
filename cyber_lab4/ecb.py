#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

# Tan Shin Jie
# 1003715
"""
Key should be numeric in this implementation

I implemented a simple padding scheme 
by appending the length of last block to the encrypted file
When decrypting, I first extract the length of the last block 
And then slice the decrypted last block accordingly
The pre-encrypted input file and post-decrypted input file 
should have the same size
"""

from present import *
import argparse

nokeybits = 80  # not used
blocksize = 8  # in bytes


def ecb(infile, outfile, key, mode):
    output_content = b""
    with open(infile, "rb") as f:
        content = f.read()
        blocks = [content[i : i + blocksize] for i in range(0, len(content), blocksize)]
        if mode == "e":
            for b in blocks:
                b = int.from_bytes(b, byteorder="big")
                b_enc = present(b, int(key))
                output_content += int.to_bytes(b_enc, blocksize, byteorder="big")
            output_content = add_padding(output_content, content, key)

        elif mode == "d":
            last_block_size = extract_padding_info(content, key)
            blocks.pop()
            for i in range(len(blocks)):
                b = blocks[i]
                b = int.from_bytes(b, byteorder="big")
                b_dec = present_inv(b, int(key))
                if i == (len(blocks) - 1):
                    start_index = blocksize - last_block_size
                    output_content += int.to_bytes(b_dec, blocksize, byteorder="big")[
                        start_index:
                    ]
                else:
                    output_content += int.to_bytes(b_dec, blocksize, byteorder="big")

    with open(outfile, "wb") as f:
        f.write(output_content)


def extract_padding_info(content, key):
    padding_info = int.from_bytes(
        content[len(content) - blocksize : len(content)], byteorder="big"
    )
    last_block_size = present_inv(padding_info, int(key))
    return last_block_size


def add_padding(output_content, content, key):
    last_block_size = len(content) % blocksize
    last_block_size_enc = present(last_block_size, int(key))
    output_content += int.to_bytes(last_block_size_enc, blocksize, byteorder="big")
    return output_content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Block cipher using ECB mode.")
    parser.add_argument("-i", dest="infile", help="input file")
    parser.add_argument("-o", dest="outfile", help="output file")
    parser.add_argument("-k", dest="key", help="should be a number")
    parser.add_argument("-m", dest="mode", help='"e" or "d"')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    key = args.key
    mode = args.mode

    if (
        infile != None
        and outfile != None
        and key.isnumeric()
        and (mode == "e" or mode == "d")
    ):
        ecb(infile, outfile, key, mode)
    else:
        if not key.isnumeric():
            print("Invalid argument: Please provide a numeric key")
        elif mode != "e" or mode != "d":
            print('Invalid argument: Modes available are "e" and "d"')
        else:
            print("usage: ecb.py [-h] [-i INFILE] [-o OUTFILE] [-k KEYFILE] [-m MODE]")

