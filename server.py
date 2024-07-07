import socket
import threading
import re

"""
strings / numbers:
    INCR value      => increments value or creates value if not already created
    DECR value      => decrements value or creates value if not already created
    GET key         => returns value associated with key
    SET key value   => sets key value pair

lists:
    LPUSH list ...  => appends one or more items to head of list
    RPUSH list ...  => appends one or more items to tail of list
"""

class Database:
    def __init__(self):
        self._storage = {}

    def parse(self, query: bytes):
        query = query.decode("utf-8")

        print(query)
        if re.search("^INCR", query):
            key = re.findall(r"^INCR (\w+)", query)[0]
            return self._incr(key)
        elif re.search("^DECR", query):
            key = re.findall(r"^DECR (\w+)", query)[0]
            return self._decr(key)
        elif re.search("^GET", query):
            key = re.findall(r"GET (\w+)", query)[0]
            return self._get(key)
        elif re.search("^SET", query):
            kvpair = re.findall(r"SET (\w+) (\w+|\"\w+\")", query)[0]
            return self._set(*kvpair)
        elif re.search("^LPUSH", query):
            ls = re.findall(r"LPUSH (\w+) (.+)", query)[0]
            return self._lpush(*ls)
        elif re.search("^RPUSH", query):
            ls = re.findall(r"RPUSH (\w+) (.+)", query)[0]
            return self._rpush(*ls)
        else:
            return "invalid instruction"

    def __interpret(self, value: str):
        if re.search(r"^\d+(\.\d+)*", value):
            if re.search(r"\.", value):
                return float(value)
            else:
                return int(value)
        elif re.search(r"\".+\"", value):
            return value[1:len(value) - 1]
        else:
            return value
        
    def _incr(self, key: str):
        self._storage[key] += 1
        return self._storage[key]
    
    def _decr(self, key: str):
        self._storage[key] -= 1
        return self._storage[key]

    def _get(self, key: str):
        return self._storage[key]
    
    def _set(self, key: str, value: str):
        self._storage[key] = self.__interpret(value)
        return self._storage[key]
    
    def _lpush(self, key: str, value: str):
        filtered = [self.__interpret(item) for item in value.split()]
        if self._storage.get(key):
            self._storage[key] = filtered[::-1] + self._storage[key]
        else:
            self._storage[key] = filtered[::-1]
        return self._storage[key]
    
    def _rpush(self, key: str, value: str):
        filtered = [self.__interpret(item) for item in value.split()]
        if self._storage.get(key):
            self._storage[key] += filtered
        else:
            self._storage[key] = filtered
        return self._storage[key]

class Server:
    HOST = socket.gethostbyname("localhost")
    PORT = 6543

    def __init__(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.HOST, self.PORT))
        self._db = Database()

    def handle_client(self, conn: socket.socket, addr):
        with conn:
            while True:
                query = conn.recv(1024)
                if not query:
                    break
                res = self._db.parse(query)
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
    db = Database()
    try:
        server.initialize()
    except KeyboardInterrupt:
        server.close()