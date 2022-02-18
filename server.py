# implement server of FMD scheme
from client import Client

class Server:
    clients: list

    def __init__(self):
        # generate 20 clients
        for i in range(20):
            self.clients[i] = Client()

    def run(self):
        # TODO: implement server
        pass
