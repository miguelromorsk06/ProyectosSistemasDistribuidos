import struct 
import socket 
host="127.0.0.1"
port = 1234

data = {
"drink": "cafe",
"price": 1.5
}
drink_bytes = data["drink"].encode("utf-8")
binary = struct.pack(f"!I{len(drink_bytes)}sf", len(drink_bytes), drink_bytes, data["price"])

with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
    s.sendto(binary,(host,port))
