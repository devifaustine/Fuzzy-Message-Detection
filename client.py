# implement client of FMD scheme
from FMD2 import PublicKey, SecretKey, KeyGen
from ecpy.curves import Curve


class Client:
    pk: PublicKey
    sk: SecretKey

    def __init__(self):
        curve = Curve.get_curve('secp256r1')
        sk, pk = KeyGen(curve)

    def simulate(self):
        pass  # TODO: implement me!
