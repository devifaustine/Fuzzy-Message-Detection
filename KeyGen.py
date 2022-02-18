# implement client of FMD scheme
from ctypes import c_uint32

from ecpy.curves import Curve
from ecpy.keys import ECPrivateKey
import random
import ctypes


class GroupElement:
    X: int
    Y: int


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
    prob: ctypes.c_uint32[int]

    def __init__(self, num=0, sec=None, prob=0):
        if sec is None:
            sec = []
        self.numKeys = num
        self.secKeys = sec
        self.prob = prob


# TODO: find out which elliptic curve is used in implementation!
cv = Curve.get_curve('secp256k1')
# numKeys / gamma in the research paper is determined to be  15
numKeys = 15


# TODO: implement KeyGen() algorithm FMD2
def keyGen(curve: Curve, numKeys: int):
    #  Public Key
    pub = PublicKey(numKeys, [GroupElement] * numKeys)

    # Secret Key
    prob: c_uint32[int] = ctypes.c_uint32(numKeys)
    priv = SecretKey(numKeys, [GroupElement] * numKeys, prob)

    # generate each public and secret key
    for i in range(numKeys):
        randomNum = random.randrange(0, 9999999)
        priv.secKeys[i] = ECPrivateKey(randomNum, curve)
        pub.pubKeys[i] = priv.secKeys[i].get_public_key()
    print(priv.secKeys)
    print(pub.pubKeys)
    return priv.secKeys, pub.pubKeys
