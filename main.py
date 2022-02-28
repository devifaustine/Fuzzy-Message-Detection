# simulation for FMD2 experiment
from server import Server

# instantiate a server, number of clients produced can be changed
server = Server(200)

# run this experiment n times
for i in range(5):
    try:
        # run the server/FMD2 experiment,
        # false positive rate can be changed
        server.run(1 / 2)
    except AssertionError:
        # can be triggered because there are false negatives,
        # p is not in the right form or false positive rate is false
        print("FMD2 experiment "+str(i+1)+" was unsuccessful!")
        print("Experiment done :(, try again!")
    else:
        print("FMD2 experiment "+str(i+1)+" was successful!")
        print("Experiment done :), try with other values!")
