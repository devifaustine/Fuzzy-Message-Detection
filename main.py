# simulation for FMD2 experiment
from server import Server

# instantiate a server, number of clients produced can be changed
server = Server(200)

# value keeps track of successful experiments
x = 0
n = 10

# run this experiment n times
for i in range(n):
    try:
        # run the server/FMD2 experiment,
        # false positive rate can be changed
        server.run(1 / 2)
    except AssertionError:
        # can be triggered because there are false negatives,
        # p is not in the right form or false positive rate is false
        print("FMD2 experiment "+str(i+1)+" was unsuccessful!")
        print("Experiment done :(, try again!")
        print("")
    else:
        x += 1
        print("FMD2 experiment "+str(i+1)+" was successful!")
        print("Experiment done :), try with other values!")
        print("")

print("Experiment was "+str(x/n*100)+"% successful!")
