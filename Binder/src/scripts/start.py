#!/usr/bin/env python3
import os
import signal


def Shutdownhandler(signum, frame):
    exit()


    # Set the signal handler
signal.signal(signal.SIGINT, Shutdownhandler)

print("\033[32mChoose target platform.\033[0m\n")

print("[1] Window")
print("[2] macOS")
print("[3] iOS")
print("[4] Linux")
print("[5] Android\n")

platform = input('[?] Select>: ')

print("\n\033[32mMalware file path.\033[0m\n")
malware_path = input("[?] Malware>: ")

if os.path.isfile(malware_path):
    f = open(malware_path, "r+")
else:
    print("\033[31mThis Malware file (" +
          malware_path+") does not exist.\033[0m")

print("\n\033[32mExecutable file path.\033[0m\n")
executable_path = input("[?] Executable>: ")

if os.path.isfile(executable_path):
    f = open(executable_path, "r+")
else:
    print("\033[31mThis executable file (" +
          executable_path+") does not exist.\033[0m")
