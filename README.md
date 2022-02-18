# Fuzzy-Message-Detection

This repository contains code implementing the FMD2 algorithm according to the research paper Fuzzy Message Detection described in https://eprint.iacr.org/2021/089.pdf. For this implementation we are using pure python library for Elliptic Curve which is ECPy. 

The algorithm from the research paper will be implemented in the FMD2.py file and the main implementation can be run in the main.py file, which runs the server and also simulate FMD2 experiment. By running the server, numerous clients will be simulated and also given a public and private key pair. One random client (sender) will then send a flag/ciphertext to the server and the server will test, whether the flag matches the detection key (dsk).