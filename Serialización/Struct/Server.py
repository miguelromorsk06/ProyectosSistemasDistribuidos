import socket
import struct
host="127.0.0.1"
port = 1234
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((host,port))
    print("Entrando en el bucle ")
    while 1:
        print("Esperando a recibir")
        binary, client = s.recvfrom(1024)
        print("Se ha recibido con éxito")
        drink_length = struct.unpack("!I", binary[:4])[0]
        drink_start = 4
        drink_end = drink_start + drink_length
        
        drink = binary[drink_start:drink_end].decode("utf-8")
        price = struct.unpack("!f", binary[drink_end:drink_end + 4])[0]
        print("Decodificado")
        decoded = {"drink": drink, "price": price}
        print(decoded)
    