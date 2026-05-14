import random
from math import gcd

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, n):
    g, x, _ = egcd(a, n)
    if g != 1:
        raise ValueError("Nu există invers modular")
    return x % n

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

def generate_prime(bits=16):
    while True:
        p = random.getrandbits(bits) | 1
        if is_probable_prime(p):
            return p

def lcm(a, b):
    return a // gcd(a, b) * b

def L(u, n):
    return (u - 1) // n

def paillier_keygen(bits=16):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    n2 = n * n
    lam = lcm(p - 1, q - 1)
    g = n + 1
    u = pow(g, lam, n2)
    l_val = L(u, n)
    mu = modinv(l_val, n)
    public_key = {"n": n, "g": g}
    private_key = {"lam": lam, "mu": mu}
    return public_key, private_key

def paillier_encrypt(public_key, m):
    n = public_key["n"]
    g = public_key["g"]
    n2 = n * n
    if not (0 <= m < n):
        raise ValueError("Mesajul trebuie să fie în [0, n)")
    while True:
        r = random.randrange(1, n)
        if gcd(r, n) == 1:
            break
    c = (pow(g, m, n2) * pow(r, n, n2)) % n2
    return c

def paillier_decrypt(public_key, private_key, c):
    n = public_key["n"]
    n2 = n * n
    lam = private_key["lam"]
    mu = private_key["mu"]
    u = pow(c, lam, n2)
    l_val = L(u, n)
    m = (l_val * mu) % n
    return m

# exemplu
if __name__ == "__main__":
    pk, sk = paillier_keygen(16)
    m = 42
    c = paillier_encrypt(pk, m)
    m_rec = paillier_decrypt(pk, sk, c)
    print("m original:", m)
    print("m decriptat:", m_rec)
