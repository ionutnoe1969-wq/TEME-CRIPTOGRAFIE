import random
from math import gcd

def is_probable_prime(n, k=10):
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_blum_prime(bits=16):
    while True:
        p = random.getrandbits(bits) | 1
        if p % 4 != 3:
            continue
        if is_probable_prime(p):
            return p

def blum_goldwasser_keygen(bits=16):
    p = generate_blum_prime(bits)
    q = generate_blum_prime(bits)
    n = p * q
    public_key = {"n": n}
    private_key = {"p": p, "q": q}
    return public_key, private_key

def bbs_stream(n, x0, length):
    x = x0
    bits = []
    for _ in range(length):
        x = pow(x, 2, n)
        bits.append(x & 1)  # LSB
    return bits, x

def blum_goldwasser_encrypt(public_key, m_bits):
    n = public_key["n"]
    while True:
        x0 = random.randrange(2, n)
        if gcd(x0, n) == 1:
            break
    keystream, xL = bbs_stream(n, x0, len(m_bits))
    c_bits = [(mb ^ kb) for mb, kb in zip(m_bits, keystream)]
    return {"c_bits": c_bits, "x0": x0, "xL": xL}

def blum_goldwasser_decrypt(private_key, public_key, ciphertext):
    n = public_key["n"]
    x0 = ciphertext["x0"]
    c_bits = ciphertext["c_bits"]
    keystream, _ = bbs_stream(n, x0, len(c_bits))
    m_bits = [(cb ^ kb) for cb, kb in zip(c_bits, keystream)]
    return m_bits

if __name__ == "__main__":
    pk, sk = blum_goldwasser_keygen(16)
    m_bits = [1, 0, 1, 1, 0, 0, 1]
    ct = blum_goldwasser_encrypt(pk, m_bits)
    m_rec = blum_goldwasser_decrypt(sk, pk, ct)
    print("m original:", m_bits)
    print("m decriptat:", m_rec)
