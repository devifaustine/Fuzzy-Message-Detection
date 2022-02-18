# implement client of FMD scheme
from FMD2 import PublicKey, SecretKey, KeyGen
from ecpy.curves import Curve


class Client:
    pk: PublicKey
    sk: SecretKey

    def __init__(self):
        # TODO: find out which curve to use! 
        curve = Curve.get_curve('secp256k1')
        sk, pk = KeyGen(curve)

    def simulate(self):
        pass  # TODO: implement me!
