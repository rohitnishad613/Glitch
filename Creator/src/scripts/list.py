#!/usr/bin/env python3

import sys

if len(sys.argv) > 1:
    if sys.argv[1] == "platform":
        print("List of platform supported by Glitch framework.\n")

        print("1) Windows")
        print("2) macOS")
        print("3) iOS")
        print("4) Linux")
        print("5) Android")
    else:
        print("Invaid option " + sys.argv[1])
else:
    print("No argument passed.\n")
    print("Usage: list <options>")
    print("  Options:")
    print("     platform")
