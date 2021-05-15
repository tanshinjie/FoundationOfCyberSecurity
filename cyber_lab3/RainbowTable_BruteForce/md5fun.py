# Tan Shin Jie
# 1003715
# Time = 198.19631433486938s

import hashlib
import time
import itertools
import string

start_time = time.time()
reverse_hash_table = {}
input_space = string.digits + string.ascii_lowercase
keyspace = []
cracked = {}

for combination in itertools.product(input_space, repeat=5):
    keyspace.append("".join(combination))

# compute all possible hashes
for key in keyspace:
    digest = hashlib.md5(key.encode()).hexdigest()
    reverse_hash_table[digest] = key

# lookup
with open("hash5.txt") as f:
    all_hashes = f.readlines()
    for hash in all_hashes:
        hash = hash.strip("\n")
        cracked[hash] = reverse_hash_table[hash]

with open("hash5_cracked.txt", "w+") as f:
    for key, value in cracked.items():
        f.write("{key},{value}\n".format(key=key, value=value))

print("--- %s seconds ---" % (time.time() - start_time))
