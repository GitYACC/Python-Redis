import socket

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
        self._server.bind((self.HOST, self.PORT))
        self._conn = None
        self._addr = None
        self._proto = ProtocolHandler()

    def initialize(self):
        self._server.listen()
        self._conn, self._addr = self._server.accept()

    def loop(self):
        while (data := self._conn.recv(1024)) != "END":
            res = self._proto.set(data)
            self._conn.sendall(bytes(str(res), "utf-8"))

if __name__ == "__main__":
    server = Server()
    server.initialize()
    server.loop()

    proto = ProtocolHandler()
    print(proto.set("∞key £something,¢133"))