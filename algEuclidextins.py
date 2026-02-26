def euclid_extins(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = euclid_extins(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return d, x, y

def phi(n):
    rezultat = n
    d = 2
    while d * d <= n:
        if n % d == 0:
            while n % d == 0:
                n //= d
            rezultat -= rezultat // d
        d += 1
    if n > 1:
        rezultat -= rezultat // n
    return rezultat

print(euclid_extins(23, 12))
print(euclid_extins(1, 2))
print(phi(1325))

