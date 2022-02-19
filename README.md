# Fuzzy-Message-Detection

This repository contains code implementing the FMD2 algorithm according to the research paper Fuzzy Message Detection described in https://eprint.iacr.org/2021/089.pdf. For this implementation we are using pure python library for Elliptic Curve which is ECPy (source code: https://ec-python.readthedocs.io/en/latest/_modules/ecpy/curves.html). 

The algorithm from the research paper will be implemented in the FMD2.py file. The main.py file basically runs the server (in server.py), which automatically simulates the FMD2 experiment. 

By running the server, numerous clients will be simulated and also given a public and private key pair. One client (sender) will then send a flag/ciphertext to the server and the server will test, whether the flag matches the detection key (dsk) of each client.

Then it will check whether this experiment is successful or not, based on the correctness of the false positive rate. 