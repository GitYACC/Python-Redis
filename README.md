# REDIS-like Database in Python

Implementation of a REDIS like database utilizing sockets and threading. Works in the same way as REDIS CLI, where commands can be sent to the server to execute actions. An interface in the form of the class `RedisClient` for this CLI implementation is included in `client.py`. Example use case:

➡️ client.py
```python
client = RedisClient()
client.set("mykey", "1")
print( client.get("mykey") )
```
```
(venv) user@computer Project % python3 client.py
b'1'
```
```python
client.incr("mykey")
print( client.get("mykey") )
```
```
(venv) user@computer Project % python3 client.py
b'2'
```

More functionality and data types of REDIS are being implemented
