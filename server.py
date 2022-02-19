# implement server of FMD scheme
import random
from sender import Sender
from client import Client
from FMD2 import extract, test, flag, curve_name
from ecpy.curves import Curve


class Server:
    clients: list
    curve: Curve

    def __init__(self, curve: Curve):
        if curve is None:
            self.curve = Curve.get_curve(curve_name)
        # generate 20 clients
        for i in range(20):
            self.clients[i] = Client()

    def run(self):
        # TODO: implement server

        # false positive rate p
        p = pow(2, -10)

        # creates a sender
        sender = Sender()

        # randomly choose one client as receiver
        receiver_id = random.randint(0, 19)
        receiver = self.clients[receiver_id]
        receiver_dsk = extract(receiver.get_seckey(), p)

        # creates flag
        f = flag(receiver.get_pubkey(), self.curve)

        # TODO: use test() from FMD2 to check if flag is valid for each client (?)
