import socket

class RedisClient:
    HOST = socket.gethostbyname("localhost")
    PORT = 6543

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))

    def sets(self, key: str, value: str):
        self.client.sendall(bytes(f"s{key} {value}", "utf-8"))
        return self.client.recv(len(value))

    def setn(self, key: str, value: int | float):
        self.client.sendall(bytes(f"n{key} {value}", "utf-8"))
        return self.client.recv(len(str(value)))

    def setl(self, key: str, value: list):
        packet = ""
        for item in value:
            match type(item).__name__:
                case "str":
                    packet += f"£{item},"
                case "int" | "float":
                    packet += f"¢{item}"

        self.client.sendall(bytes(f"l{key} {packet[:len(packet) - 1]}", "utf-8"))
        return self.client.recv(1024)


client = RedisClient()
print(client.sets("Something", "Something Else"))