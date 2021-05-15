# Tan Shin Jie
# 1003715
# script to generate salted hash, salted_hash = MD5(password||salt)

import hashlib
import string
import random

salted_hash_table = {}

with open("hash5_cracked.txt", "r") as f:
    passwords = f.readlines()
    for password in passwords:
        password = password.split(",")[1].strip("\n")
        salt = string.ascii_lowercase[
            random.randint(0, len(string.ascii_lowercase) - 1)
        ]
        salted_password = password + salt
        salted_digest = hashlib.md5(salted_password.encode()).hexdigest()
        salted_hash_table[salted_password] = salted_digest

with open("pass5_diff_salted.txt", "w+") as f:
    for key in salted_hash_table.keys():
        f.write("{key}\n".format(key=key))

with open("hash5_diff_salted.txt", "w+") as f:
    for value in salted_hash_table.values():
        f.write("{value}\n".format(value=value))

