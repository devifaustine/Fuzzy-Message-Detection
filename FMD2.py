# implementation of whole FMD2 primitives
import math
import random
from ecpy.curves import Curve, Point
from ecpy.keys import ECPrivateKey


class PublicKey:
    numKeys: int
    pubKeys: list
    generator: int

    def __init__(self, num=0, pub=None):
        if pub is None:
            pub = []
        self.numKeys = num
        self.pubKeys = pub


class SecretKey:
    numKeys: int
    secKeys: list

    def __init__(self, num=0, sec=None):
        if sec is None:
            sec = []
        self.numKeys = num
        self.secKeys = sec


# use NIST P-256 (FIPS 186-3)
curve_name = 'secp256r1'
# generator for curve secp256r1
generator = Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                  0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
                  Curve.get_curve(curve_name))


# generates a public and private key pair
def KeyGen(curve: Curve, numKeys=15):
    sk = SecretKey(numKeys)
    pk = PublicKey(numKeys)

    for i in range(numKeys):
        randomNum = random.randrange(0, 9999999)  # TODO: find out range for Zq!
        sk.secKeys[i] = ECPrivateKey(randomNum, curve)
        pk.pubKeys[i] = sk.secKeys[i].get_public_key()

    return sk, pk


# generates detection key (dsk) from a secret key and false positive rate p
def Extract(sk: SecretKey, p: float):
    # p = false positive rate in form 2^(-n) with 0 <= n <= gamma (15).
    n = int(math.log(1 / p, 2))
    result = []
    for i in range(n):
        result.append(sk.secKeys[i])
    dsk = SecretKey(n, result)
    return dsk


# generates ciphertext on input public key
def Flag(pk: PublicKey, curve: Curve):
    pubKey = pk.pubKeys
    # tag:
    r = random.randrange(0, 99999999)  # TODO: find out range for Zq!
    ux, uy = curve.mul_point(r, generator)
    z = random.randrange(0, 99999999)  # TODO: find out range for Zq!
    wx, wy = curve.mul_point(z, generator)

    c = []

    # gamma is set to 15
    for i in range(15):
        # TODO: implement me! find out which python lib for SHA256
    pass


# outputs whether flag/ciphertext matches dsk (return bool)
def Test(dsk: SecretKey, m) -> bool:
    # TODO: implement me!
    pass

def hash_h():
    pass # TODO: implement me!

def hash_g():
    pass # TODO: implement me!
