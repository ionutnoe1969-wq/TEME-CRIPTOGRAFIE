import random
from math import gcd

def modexp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def modinv(a, mod):
    t, new_t = 0, 1
    r, new_r = mod, a

    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r

    if r > 1:
        raise ValueError("Nu există invers modular")
    if t < 0:
        t += mod

    return t

def generate_keypair(p):
    while True:
        e = random.randint(2, p - 2)
        if gcd(e, p - 1) == 1:
            break
    d = modinv(e, p - 1)
    return e, d

def massey_omura_encrypt(m, e, p):
    return modexp(m, e, p)

def massey_omura_decrypt(c, d, p):
    return modexp(c, d, p)

if __name__ == "__main__":
    p = 30803
    m = 12345

    eA, dA = generate_keypair(p)
    eB, dB = generate_keypair(p)

    print("Chei Alice:", eA, dA)
    print("Chei Bob:", eB, dB)

    X = massey_omura_encrypt(m, eA, p)

    Y = massey_omura_encrypt(X, eB, p)

    Z = massey_omura_decrypt(Y, dA, p)

    decrypted = massey_omura_decrypt(Z, dB, p)

    print("Mesaj original:", m)
    print("Mesaj decriptat:", decrypted)
