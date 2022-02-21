# implement server of FMD scheme
import math
import random
from client import Client
from FMD2 import extract, test, flag, curve_name
from ecpy.curves import Curve


class Server:
    clients: list
    curve: Curve

    def __init__(self, num: int, curve=None):
        if curve is None:
            curve = Curve.get_curve(curve_name)
        self.curve = curve
        # generate num clients
        self.clients = []
        for i in range(num):
            self.clients.append(Client())

    # runs the FMD2 experiment with false positive rate p
    def run(self, p: float):

        # false positive rate p should be in form 1/(2^n)
        assert (math.log(1/p, 2)) % 1 == 0

        # creates a sender
        sender = Client()

        # randomly choose one client as intended receiver
        receiver_id = random.randint(0, len(self.clients)-1)
        receiver = self.clients[receiver_id]

        # creates flag
        f = flag(receiver.get_pubkey(), self.curve)

        # keeps track of test() results
        true = 0
        false_pos = 0
        false_neg = 0

        # test the flag for each client
        for i in range(len(self.clients)):
            client = self.clients[i]
            client_dsk = extract(client.get_seckey(), p)
            if test(self.curve, client_dsk, f):
                if i == receiver_id:
                    true += 1
                else:
                    false_pos += 1
            else:
                if i == receiver_id:
                    false_neg += 1

        # there should be no false negatives
        assert false_neg == 0
        # the false positives should be at minimum p%
        assert false_pos/len(self.clients) >= p
