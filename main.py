# simulation for FMD2 experiment
from server import Server

# number of clients produced can be changed
server = Server(20)

try:
    # false positive rate can be changed
    server.run(1/8)
except AssertionError:
    print("FMD2 experiment was unsuccessful!")
else:
    print("FMD2 experiment was successful!")
finally:
    print("Experiment done :), try with other values!")
