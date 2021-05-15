#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018
# Andrei + Z.TANG + Bowen, 2019



"""
Student Name: Tan Shin Jie

Student ID: 1003715

Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/
"""


from pwn import remote

# pass two bytestrings to this function
def XOR(a, b):
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r

char_map = {}
word_map = {}
final_char_map = {}

def extract_frequency(challenge):
    challenge_local = challenge
    with open("frequency_dist.csv",'w') as file: 
        for byte in challenge:
            if byte not in char_map.keys() and byte != 32:
                char_map[byte] = challenge.count(byte) 
        for i in range(65,91):
            final_char_map[chr(i)] = 0

        str_challenge = challenge_local.decode('utf-8').split(' ')
        for word in str_challenge:
            word = word.strip(',').strip('.')
            if len(word) > 1:
                final_char_map[str(word[-1:])] += 1
            if word not in word_map.keys():
                word_map[word] = str_challenge.count(word)
                
        sorted_char_keys = sorted(char_map.keys())
        for char in sorted_char_keys:
            toWrite = chr(char) + ',' + str(char_map[char]) + '\n'
            file.write(toWrite)

        sorted_word_keys = sorted(word_map.keys())
        for word in sorted_word_keys:
            toWrite = word + ',' + str(word_map[word]) + '\n'
            file.write(toWrite)
        
        for final_char in final_char_map.keys():
            toWrite = final_char + ',' + str(final_char_map[final_char]) + '\n'
            file.write(toWrite)
       
mapping = {
    'A':'A',
    'B':'Z',
    'C':'E',
    'D':'R',
    'E':'T',
    'F':'Y',
    'G':'U',
    'H':'I',
    'I':'O',
    'J':'P',
    'K':'Q',
    'L':'S',
    'M':'D', 
    'N':'F',
    'O':'G',
    'P':'H',
    'Q':'J',
    'R':'K', 
    'S':'L',
    'T':'M',
    'U':'W',
    'V':'X',
    'W':'C',
    'X':'V',
    'Y':'B',
    'Z':'N',
    ',':',',
    '.':'.'
}
    

def sol1():
    conn.send("1")  # select challenge 1
    challenge = conn.recv()
    print("Question 1:\n")
    print(challenge)
    # decrypt the challenge here
    print('')
    # extract_frequency(challenge)
    challenge_word_list = challenge.decode('utf-8').split(' ')
    plaintext = []
    for word in challenge_word_list:
        plain_word = ''
        for char in word:
            plain_word += mapping[char]
        plaintext.append(plain_word)
    solution = ' '.join(plaintext)
    conn.send(solution.encode())
    message = conn.recv()
    if b'Congratulations' in message:
        print(message)

def sol2():
    conn.send("2")  # select challenge 2
    challenge = conn.recv()
    print("\nQuestion 2:\n")
    challenge = challenge.decode("UTF-8")
    print(challenge)
    challenge = bytearray.fromhex(challenge)

    # some all zero mask.
    # TODO: find the magic mask!
    mask = bytearray(len(challenge))
    mask[14] = 3
    mask[15] = 7
    mask[16] = 1
    mask[17] = 5
    mask[24] = 4
    message = XOR(challenge, mask)
    conn.send(message)
    message = conn.recv()
    if b' points' in message:
        print(message)


if __name__ == "__main__":

    # NOTE: UPPERCASE names for constants is a (nice) Python convention
    URL = "35.198.199.82"
    PORT = 4455

    conn = remote(URL, PORT)
    receive1 = conn.recv()
    print(receive1.decode("UTF-8"))

    sol1()
    sol2()
    conn.close()
