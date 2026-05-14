import random

def mat_mul(A, B, n):
    return [
        [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % n,
         (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % n],
        [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % n,
         (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % n]
    ]

def mat_det(A, n):
    return (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % n

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

def mat_inv(A, n):
    det = mat_det(A, n)
    det_inv = modinv(det, n)
    return [
        [( A[1][1] * det_inv) % n, (-A[0][1] * det_inv) % n],
        [(-A[1][0] * det_inv) % n, ( A[0][0] * det_inv) % n]
    ]

def mat_pow(A, e, n):
    R = [[1, 0], [0, 1]]  
    B = [row[:] for row in A]
    while e > 0:
        if e & 1:
            R = mat_mul(R, B, n)
        B = mat_mul(B, B, n)
        e >>= 1
    return R

def cayley_purser_keygen():
    p = 101
    q = 113
    n = p * q

    while True:
        C = [[random.randrange(1, n), random.randrange(1, n)],
             [random.randrange(1, n), random.randrange(1, n)]]
        try:
            _ = mat_inv(C, n)
            break
        except ValueError:
            continue

    while True:
        A = [[random.randrange(1, n), random.randrange(1, n)],
             [random.randrange(1, n), random.randrange(1, n)]]
        try:
            _ = mat_inv(A, n)
            break
        except ValueError:
            continue

    C_inv = mat_inv(C, n)
    A_inv = mat_inv(A, n)
    B = mat_mul(mat_mul(C_inv, A_inv, n), C, n)

    r = random.randint(2, 20)
    G = mat_pow(C, r, n)

    public_key = {"A": A, "B": B, "G": G, "n": n}
    private_key = {"C": C, "p": p, "q": q, "r": r}
    return public_key, private_key

def cayley_purser_encrypt(public_key, X):
    A = public_key["A"]
    G = public_key["G"]
    n = public_key["n"]

    s = random.randint(2, 20)
    D = mat_pow(G, s, n)
    D_inv = mat_inv(D, n)
    E = mat_mul(mat_mul(D_inv, A, n), D, n)
    E_inv = mat_inv(E, n)
    Y = mat_mul(mat_mul(E_inv, X, n), E, n)
    return {"D": D, "Y": Y}

def cayley_purser_decrypt(public_key, private_key, ciphertext):

    A = public_key["A"]
    n = public_key["n"]
    D = ciphertext["D"]
    Y = ciphertext["Y"]

    D_inv = mat_inv(D, n)
    E = mat_mul(mat_mul(D_inv, A, n), D, n)
    E_inv = mat_inv(E, n)
    X = mat_mul(mat_mul(E, Y, n), E_inv, n)
    return X

if __name__ == "__main__":
    pk, sk = cayley_purser_keygen()
    n = pk["n"]
    X = [[1, 2], [3, 4]]
    ct = cayley_purser_encrypt(pk, X)
    X_rec = cayley_purser_decrypt(pk, sk, ct)
    print("Original:", X)
    print("Decriptat:", X_rec)
