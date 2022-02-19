# implement server of FMD scheme
import random
from client import Client
from FMD2 import extract, test, flag, curve_name
from ecpy.curves import Curve


class Server:
    clients: list
    curve: Curve

    def __init__(self, curve=None):
        if curve is None:
            self.curve = Curve.get_curve(curve_name)
        # generate 20 clients
        for i in range(20):
            self.clients[i] = Client()

    def run(self):

        # false positive rate p
        p = pow(2, -10)

        # creates a sender
        sender = Client()

        # randomly choose one client as intended receiver
        receiver_id = random.randint(0, 19)
        receiver = self.clients[receiver_id]

        # creates flag
        f = flag(receiver.get_pubkey(), self.curve)

        # keeps track of test() results
        true = 0
        false_pos = 0
        false_neg = 0

        for i in range(20):
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
        assert false_pos/len(self.clients) >= p
