# implementation of whole FMD2 primitives
import math
import random
from ecpy.curves import Curve, Point
from ecpy.keys import ECPrivateKey, ECPublicKey
import hashlib


class PublicKey:
    numKeys: int
    pubKeys: list

    def __init__(self, num=0, pub=None):
        if pub is None:
            pub = []
        self.numKeys = num
        self.pubKeys = pub

    def add_pubkey(self, pk: ECPublicKey):
        self.pubKeys.append(pk)


class SecretKey:
    numKeys: int
    secKeys: list

    def __init__(self, num=0, sec=None):
        if sec is None:
            sec = []
        self.numKeys = num
        self.secKeys = sec

    def add_seckey(self, sk: ECPrivateKey):
        self.secKeys.append(sk)


class Flag:
    u: Point
    y: int
    c: list

    def __init__(self, u: Point, y: int, c: list):
        if c is None:
            c = []
        self.c = c
        self.u = u
        self.y = y

    def get_u(self):
        return self.u

    def get_y(self):
        return self.y

    def get_c(self):
        return self.c


# use NIST P-256 (FIPS 186-3)
curve_name = 'secp256r1'

# generator for curve secp256r1
generator = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                  0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
                  Curve.get_curve(curve_name))

# order of group for curve 'secp256r1'
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551


# generates a public and private key pair
def keyGen(curve: Curve, numKeys=15):
    sk = SecretKey(numKeys)
    pk = PublicKey(numKeys)

    for i in range(numKeys):
        randomNum = random.randrange(0, q)
        sk.add_seckey(ECPrivateKey(randomNum, curve))
        #  print(str(sk.secKeys[i]))
        pk.add_pubkey(sk.secKeys[i].get_public_key())
        #  print(str(pk.pubKeys[i]))

    return sk, pk


# generates detection key (dsk) from a secret key and false positive rate p
def extract(sk: SecretKey, p: float):
    # p = false positive rate in form 2^(-n) with 0 <= n <= gamma (15).
    n = int(math.log(1 / p, 2))
    result = []
    for i in range(n):
        result.append(sk.secKeys[i])
    dsk = SecretKey(n, result)
    return dsk


# generates ciphertext/flag on input public key
def flag(pk: PublicKey, curve: Curve) -> Flag:
    pubKey = pk.pubKeys
    # tag:
    r = random.randrange(0, q)
    u = curve.mul_point(r, generator)
    z = random.randrange(0, q)
    w = curve.mul_point(z, generator)

    c = []
    k = []

    # gamma is set to 15
    for i in range(15):
        # according to GO implementation h = u^{sk_i}
        # h = pubKey * r
        h = curve.mul_point(r, pubKey[i].W)
        k.append(hash_h(u, h, w))
        c.append(k[i] ^ 1)

    m = hash_g(u.x, u.y, c)
    y = ((z - m) * pow(r, -1, q)) % q
    result = Flag(u, y, c)
    return result


# outputs whether flag/ciphertext matches dsk (return bool)
# default output of this function is True if the dsk has zero sub-keys,
# then it will always return True
def test(curve: Curve, dsk: SecretKey, f: Flag) -> bool:
    result = True

    key = dsk.secKeys
    u = f.get_u()
    y = f.get_y()
    c = f.get_c()

    # compute hash_G
    message = hash_g(u.x, u.y, c)

    # compute Z = mP + yU --> from implementation in GO
    z = curve.mul_point(message, generator)
    t = curve.mul_point(y, u)
    z = curve.add_point(z, t)

    # for each subkey 1...numKeys in the secret key, decrypt that bit
    for i in range(dsk.numKeys):
        pkr = curve.mul_point(key[i].d, u)

        # compute padding = H(pk_i || pkR || Z) XOR the i^th bit of c from Flag
        padding = hash_h(u, pkr, z)
        padding ^= c[i] & 0x01  # following GO implementation

        if padding == 0:
            result = False

    return result


# encrypts a string using SHA256
def encrypt_string(hash_string) -> bytes:
    sha_signature = hashlib.sha256(hash_string.encode()).digest()
    return sha_signature


# compute hash function H(U, X, W) where U,X and W are points
def hash_h(u: Point, h: Point, w: Point):
    string = str(u.x) + str(u.y) + str(h.x) + str(h.y) + str(w.x) + str(w.y)
    # returns a single bit of the resulting hash
    return encrypt_string(string)[0] & 0x01


# returns an integer in range(0, group order - 1)
def hash_g(ux: int, uy: int, c: list) -> int:
    # concatenate all values
    string = str(ux) + str(uy)
    for i in c:
        string += str(i)

    # size of the supposed hashed value should be at least 64 bits too long
    size = q.bit_length() + 64
    result = b''
    bit_hashed = 0

    while bit_hashed < size:
        # hash the serialized value and append to result
        hashed = encrypt_string(string)
        result += (hashed[:32])
        bit_hashed = len(result) / 8

        # concatenate an 'X' onto the end of string each time through this loop
        # this ensures that string is different each time we hash it
        if bit_hashed < size:
            string += "X"

    # cast the resulting byte array into integer and compute % q
    res = int.from_bytes(result, "big") % q

    return res
