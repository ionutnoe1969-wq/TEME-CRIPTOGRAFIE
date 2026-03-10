import random
from math import gcd

def jacobi(a, n):
    if n <= 0 or n % 2 == 0:
        return 0

    a = a % n
    result = 1

    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result

        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result

        a = a % n

    return result if n == 1 else 0


def solovay_strassen(n, k=10):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randrange(2, n - 1)
        g = gcd(a, n)
        if g > 1:
            return False

        j = jacobi(a, n) % n
        x = pow(a, (n - 1) // 2, n)

        if x != j:
            return False

    return True


def afisare_test(n, k=10):
    print(f"Test Solovay–Strassen pentru n = {n}, runde = {k}")
    rezultat = solovay_strassen(n, k)

    if rezultat:
        print(f"{n} este probabil prim (cu probabilitate ≥ 1 - 2^(-{k}))")
    else:
        print(f"{n} este compus")

afisare_test(97)
afisare_test(221)


import math

def fermat_factor(n):
    if n % 2 == 0:
        return 2, n // 2

    a = math.isqrt(n)
    if a * a < n:
        a += 1

    while True:
        b2 = a * a - n
        b = int(math.isqrt(b2))

        if b * b == b2:
            return a - b, a + b

        a += 1


def afisare_fermat(n):
    print(f"Factorizare Fermat pentru n = {n}")
    f1, f2 = fermat_factor(n)
    print(f"Factorii sunt: {f1} și {f2}")

afisare_fermat(5959)
afisare_fermat(221)
