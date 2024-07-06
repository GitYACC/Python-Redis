import socket
import threading

"""
get(string) -> any
set(string, any)

string:
    skey string

number:
    nkey number

list:
    lkey [string],[number],...
"""

class ProtocolHandler:
    def __init__(self):
        self._storage = {}

    def _parse(self, item: str):
        match item[0]:
            case "s":
                return str(item[1:])
            case "n":
                return int(item[1:])
        
    def set(self, query: bytes):
        if len(query) == 0: return

        q = query.decode().split()
        key = q[0]
        value = " ".join(q[1:])
        
        match key[0]:
            case "s":
                self._storage[key[1:]] = str(value)
            case "n":
                self._storage[key[1:]] = int(value)
            case "l":
                self._storage[key[1:]] = list(map(
                    lambda x : self._parse(x), 
                    value.split(",")
                ))
        return self._storage[key[1:]]

    def get(self, query: str):
        return self._storage[query]

        

class Server:
    HOST = socket.gethostbyname("localhost")
    PORT = 6543

    def __init__(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.HOST, self.PORT))
        self._proto = ProtocolHandler()

    def handle_client(self, conn: socket.socket, addr):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                res = self._proto.set(data)
                conn.sendall(bytes(str(res), "utf-8"))


    def initialize(self):
        self._server.listen(10)
        while True:
            conn, addr = self._server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

    def close(self):
        self._server.close()

if __name__ == "__main__":
    server = Server()
    try:
        server.initialize()
    except KeyboardInterrupt:
        server.close()

    #proto = ProtocolHandler()
    #print(proto.set("∞key £something,¢133"))