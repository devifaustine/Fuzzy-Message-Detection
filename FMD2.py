# implementation of whole FMD2 primitives
import math
import random
from ecpy.curves import Curve
from ecpy.keys import ECPrivateKey


class PublicKey:
    numKeys: int
    pubKeys: list

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
    r = random.randrange(0, 99999999)  # TODO: find out range for Zq!
    pass  # TODO: implement me!


# outputs whether flag/ciphertext matches dsk (return bool)
def Test(dsk: SecretKey, m) -> bool:
    # TODO: implement me!
    pass
