from math import gcd
from random import randrange

from core.aks import is_prime

def miller_rabin_algorithm(n):
    assert n >= 2
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert 2 ** s * d == n - 1
    
    for i in range(100):
        a = randrange(2, n)
        if try_composite(a, d, n, s):
            return False
    return True

def try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True

def is_odd_prime(a):
    return is_prime(a) and a % 2 == 1


def is_coprime(a, b):
    return gcd(a, b) == 1


def to_base_2(a):
    # phân tích a về dạng a = q.2^s, với q lẻ
    q, s = a, 0
    while q % 2 == 0:
        q /= 2
        s += 1
    return q, s


def to_base(n, base):
    digits = []
    while n:
        digits.insert(0, n % base)
        n //= base
    return digits