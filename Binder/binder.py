#!/usr/bin/env python3
import signal
import os

# Getting currunt path
currunt_path_temp = os.path.abspath(__file__)
currunt_path = os.path.split(currunt_path_temp)[0] + "/"


def Shutdownhandler(signum, frame):
    exit()


    # Set the signal handler
signal.signal(signal.SIGINT, Shutdownhandler)

print("\n")

while(True):
    commend = input("\033[33mGLITCH::binder>\033[0m ")
    commend = commend.split()
    if commend[0] == "" or commend[0] == 'start':
        exec(open(currunt_path + "Binder/src/scripts/start.py").read())
    elif commend[0] == 'help':
        exec(open(currunt_path + "Binder/src/scripts/help.py").read())
