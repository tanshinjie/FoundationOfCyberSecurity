# 50.042 FCS Lab 6 template
# Year 2019

"""
Tan Shin Jie
1003715
"""

import math
import primes_template
from dhke_template import *
import time


def baby_step(alpha, beta, p):
    baby_step_dict = {}
    m = math.ceil(math.sqrt(p))
    res = 0
    for xb in range(0, m):
        res = (alpha ** xb) * beta % p
        baby_step_dict[res] = xb
    return baby_step_dict


def giant_step(alpha, p):
    giant_step_dict = {}
    m = math.ceil(math.sqrt(p))
    res = 0
    for xg in range(0, m):
        res = pow(alpha, (xg * m), p)
        giant_step_dict[res] = xg
    return giant_step_dict


def baby_giant(alpha, beta, p):
    baby_step_dict = baby_step(alpha, beta, p)
    giant_step_dict = giant_step(alpha, p)
    for key in baby_step_dict.keys():
        try:
            xg = giant_step_dict[key]
            xb = baby_step_dict[key]
            m = math.ceil(math.sqrt(p))
            x = xg * m - xb
            return x
        except:
            pass
    return 0


if __name__ == "__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    
    """
    # p = 17851
    # alpha = 17511
    # A = 2945
    # B = 11844
    # sharedkey = 1671
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # print("a", a)
    # print("b", b)
    # guesskey1 = primes_template.square_multiply(A, b, p)
    # guesskey2 = primes_template.square_multiply(B, a, p)
    # print("Guess key 1:", guesskey1)
    # print("Guess key 2:", guesskey2)
    # print("Actual shared key :", sharedkey)

    # ''' Breaking shared_key of length 16 '''
    # p, alpha = dhke_setup(16)
    # print("Generate P and alpha:")
    # print("P:", p)
    # print("alpha:", alpha)
    # print()
    # a = gen_priv_key(p)
    # b = gen_priv_key(p)
    # A = get_pub_key(alpha, a, p)
    # B = get_pub_key(alpha, b, p)
    # print("My public key is: ", A)
    # print("Test other public key is: ", B)
    # print()
    # sharedKeyA = get_shared_key(B, a, p)
    # sharedKeyB = get_shared_key(A, b, p)
    # print("My shared key is: ", sharedKeyA)
    # print("Test other shared key is: ", sharedKeyB)
    # print("Length of key is %d bits." % sharedKeyA.bit_length())
    # print()
    # a_ = baby_giant(alpha, A, p)
    # b_ = baby_giant(alpha, B, p)
    # print("a_", a_)
    # print("b_", b_)
    # guesskey1 = primes_template.square_multiply(A, b_, p)
    # guesskey2 = primes_template.square_multiply(B, a_, p)
    # print("Guess key 1:", guesskey1)
    # print("Guess key 2:", guesskey2)
    # print("Actual shared key :", sharedKeyA)

    # """
    # Unable to break when n = 34
    # """
    # with open("time_to_break.csv", "w+") as f:
    #     f.write("n,time_to_break\n")
    #     for i in range(3, 128):
    #         total_time = 0
    #         p, alpha = dhke_setup(i)
    #         # print("Attempt to break {} bits key".format(i))
    #         start_time = time.time()
    #         a = gen_priv_key(p)
    #         b = gen_priv_key(p)
    #         A = get_pub_key(alpha, a, p)
    #         B = get_pub_key(alpha, b, p)
    #         sharedKey = get_shared_key(A, b, p)  # same as get_shared_key(B, a, p)
    #         a_ = baby_giant(alpha, A, p)
    #         b_ = baby_giant(alpha, B, p)
    #         guesskey1 = primes_template.square_multiply(A, b_, p)
    #         guesskey2 = primes_template.square_multiply(B, a_, p)
    #         print("Test:", guesskey1 == sharedKey or guesskey2 == sharedKey)
    #         time_taken = time.time() - start_time
    #         f.write("{},{}\n".format(i, time_taken))
    #         print("Time for {} bits key is {}\n".format(i, time_taken))

