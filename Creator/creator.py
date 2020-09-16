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
    commend = input("\033[33mGLITCH::creator>\033[0m ")
    commend = commend.split()
    if commend[0] == "" or commend[0] == 'start':
        exec(open(currunt_path + "Creator/src/scripts/start.py").read())
    elif commend[0] == 'help':
        exec(open(currunt_path + "Creator/src/scripts/help.py").read())
    elif commend[0] == 'list':
        if len(commend) > 1:
            script_descriptor = open(
                currunt_path + "Creator/src/scripts/list.py")
            script = script_descriptor.read()
            sys.argv = ["list.py", commend[1]]
            exec(script)
            script_descriptor.close()
        else:
            exec(open(currunt_path + "Creator/src/scripts/list.py").read())
    else:
        print("\033[31mInvalid syntex.\033[0m")
