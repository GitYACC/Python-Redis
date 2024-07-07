import socket

class RedisClient:
    HOST = socket.gethostbyname("localhost")
    PORT = 6543

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))

    def set(self, key: str, value: str):
        self.client.sendall(bytes(f"SET {key} {value}", "utf-8"))
        return self.client.recv(len(value))
    
    def get(self, key: str):
        self.client.sendall(bytes(f"GET {key}", "utf-8"))
        return self.client.recv(1024)
    
    def incr(self, key: str):
        self.client.sendall(bytes(f"INCR {key}", "utf-8"))
        return self.client.recv(1024)
    
    def decr(self, key: str):
        self.client.sendall(bytes(f"DECR {key}", "utf-8"))
        return self.client.recv(1024)
    
    def lpush(self, key: str, *values):
        values = " ".join(map(lambda x: str(x), values))
        self.client.sendall(bytes(f"LPUSH {key} {values}", "utf-8"))
        return self.client.recv(1024)
    
    def rpush(self, key: str, *values):
        values = " ".join(map(lambda x: str(x), values))
        self.client.sendall(bytes(f"RPUSH {key} {values}", "utf-8"))
        return self.client.recv(1024)


client = RedisClient()
print(client.incr("bike"))