# 50.042 FCS Lab 6 template
# Year 2019

"""
Tan Shin Jie
1003715
"""

import random

MR_ROUND = 40


def square_multiply(a, x, n):
    res = 1
    for i in bin(x)[2:]:
        res = res * res % n
        if i == "1":
            res = res * a % n
    return res


def miller_rabin(n, a):
    # Check is n is 2 or 3
    if n == 2 or n == 3:
        return True
    # Check if n is not even.
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r >>= 1
    for _ in range(a):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def gen_prime_nbits(n):
    p = 0
    while not miller_rabin(p, MR_ROUND):
        p = generate_prime_candidate(n)
    return p


def generate_prime_candidate(n):
    p = random.getrandbits(n)
    p |= (1 << n - 1) | 1
    return p


if __name__ == "__main__":
    print("Is 561 a prime?")
    print(miller_rabin(561, MR_ROUND))
    print("Is 27 a prime?")
    print(miller_rabin(27, MR_ROUND))
    print("Is 61 a prime?")
    print(miller_rabin(61, MR_ROUND))

    print("Random number (100 bits):")
    print(gen_prime_nbits(100))
    print("Random number (80 bits):")
    print(gen_prime_nbits(80))

