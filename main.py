# simulation for FMD2 experiment
from server import Server

# number of clients produced can be changed
server = Server(20)
# false positive rate can be changed
server.run(1/8)
