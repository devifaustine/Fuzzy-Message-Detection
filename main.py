# simulation for FMD2 experiment
from server import Server

# instantiate a server, number of clients produced can be changed
server = Server(20)

try:
    # run the server/FMD2 experiment,
    # false positive rate can be changed
    server.run(1/8)
except AssertionError:
    # can be triggered because there are false negatives,
    # p is not in the right form or false positive rate is false
    print("FMD2 experiment was unsuccessful!")
else:
    print("FMD2 experiment was successful!")
finally:
    print("Experiment done :), try with other values!")
