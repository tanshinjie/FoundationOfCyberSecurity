# 50.042 FCS Lab 6 template
# Year 2019

"""
Tan Shin Jie
1003715
"""

import primes_template
import random
import ecb


def dhke_setup(nb):
    P = primes_template.gen_prime_nbits(nb)
    alpha = random.randint(2, P - 2)
    return P, alpha


def gen_priv_key(p):
    return random.randint(2, p - 2)


def get_pub_key(alpha, a, p):
    return primes_template.square_multiply(alpha, a, p)


def get_shared_key(keypub, keypriv, p):
    return primes_template.square_multiply(keypub, keypriv, p)


if __name__ == "__main__":
    """ DEMO: To generate 80 bit shared key """
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())
    print()

    # Encryption & Decryption with shared key
    print("Encrypting with Present in ECB mode using shared key")
    ecb.ecb("cyber_risks.png", "encrypted_cyber_risks.png", sharedKeyA, "e")

    print()
    print("Decrypting with Present in ECB mode using shared key")
    ecb.ecb("encrypted_cyber_risks.png", "decrypted_cyber_risks.png", sharedKeyB, "d")

