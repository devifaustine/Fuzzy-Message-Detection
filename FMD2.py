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
        print(str(sk.secKeys[i]))
        pk.add_pubkey(sk.secKeys[i].get_public_key())
        print(str(pk.pubKeys[i]))

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
        k.append(hash_h(curve, u.x, u.y, h.x, h.y, w.x, w.y))
        c.append(k[i] ^ 1)

    m = hash_g(u.x, u.y, c)
    y = ((z - m) * pow(r, -1)) % q
    result = Flag(u, y, c)
    return result


# outputs whether flag/ciphertext matches dsk (return bool)
def test(curve: Curve, dsk: SecretKey, f: Flag) -> bool:
    # TODO: Fix this accordingly!
    key = dsk.secKeys
    u = f.get_u()
    y = f.get_y()
    c = f.get_c()
    message = hash_g(u.x, u.y, c)
    # w = g^m * u^y --> TODO: find out how to compute thi
    # TODO: this is wrongly implemented! Fix this!
    w1 = curve.mul_point(message, generator)
    w2 = curve.mul_point(y, u)
    wx = w1.x * w2.x
    wy = w1.y * w2.y
    k = []

    for i in range(dsk.numKeys):
        hx, hy = curve.mul_point(key[i], u)
        k[i] = hash_h(curve, u.x, u.y, hx, hy, wx, wy)
    return False


# encrypts a string using SHA256
def encrypt_string(hash_string) -> bytes:
    sha_signature = hashlib.sha256(hash_string.encode()).digest()
    return sha_signature


def hash_h(curve: Curve, ux: int, uy: int, hx: int, hy: int, wx: int, wy: int):
    string = str(ux) + str(uy) + str(hx) + str(hy) + str(wx) + str(wy)
    # returns a single bit of the resulting hash
    return encrypt_string(string)[0] & 0x01


def hash_g(ux: int, uy: int, c: list) -> int:
    # returns an integer in range(0, group order - 1)
    return 0  # TODO: implement me!
