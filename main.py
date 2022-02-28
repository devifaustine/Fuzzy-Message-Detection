# simulation for FMD2 experiment
from server import Server

# instantiate a server, number of clients produced can be changed
server = Server(100)

try:
    # run the server/FMD2 experiment,
    # false positive rate can be changed
    server.run(1/16)
except AssertionError:
    # can be triggered because there are false negatives,
    # p is not in the right form or false positive rate is false
    print("FMD2 experiment was unsuccessful!")
    print("Experiment done :(, try again!")
else:
    print("FMD2 experiment was successful!")
    print("Experiment done :), try with other values!")
