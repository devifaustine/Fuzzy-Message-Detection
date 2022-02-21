# implement client of FMD scheme
from FMD2 import PublicKey, SecretKey, keyGen
from ecpy.curves import Curve


class Client:
    pk: PublicKey
    sk: SecretKey

    # generate a client and public private key pair
    def __init__(self, curve=None):
        if curve is None:
            curve = Curve.get_curve('secp256r1')
        self.sk, self.pk = keyGen(curve)

