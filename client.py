# implement client of FMD scheme
from FMD2 import PublicKey, SecretKey, keyGen
from ecpy.curves import Curve


class Client:
    pk: PublicKey
    sk: SecretKey

    def __init__(self):
        curve = Curve.get_curve('secp256r1')
        sk, pk = keyGen(curve)

    def get_pubkey(self) -> PublicKey:
        return self.pk

    def get_seckey(self) -> SecretKey:
        return self.sk

    def simulate(self):
        pass  # TODO: implement me!
