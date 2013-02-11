from socket import *
from thread import *
from random import randint
import struct
import os
from sys import argv

if len(argv)==2:
    ip=argv[1]
else:
    ip=raw_input("IP del servidor: ")
port=5008
sock = socket()
sock.bind((ip, port))
sock.listen(1)

clientes = []
def client(con, dir):
    a = 0
    e = 0
    n = 10
    sorteo = randint(0,n)
    while True:
        try:
            if dir[0] not in clientes:
                clientes.append(dir[0])
                print dir[0], "dice 'hola', y tiene:", sorteo
            data = con.recv(1024)
            try:
                datos = struct.unpack("i",data)
                print dir[0], "dice", datos[0], ":", sorteo
                if datos[0] == sorteo:
                    a+=1
                    if a == 10:
                        n+=5
                    con.send(struct.pack("c", "Y"))
                    sorteo = randint(0,n)
                    print dir[0], "adivino correctamente, nuevo:", sorteo
                else:
                    e+=1
                    if e == 10:
                        n-=5
                        if n<=0:
                            print dir[0], "ha perdido"
                            con.send(struct.pack("c","P"))
                            clientes.remove(dir[0])
                            con.close()
                            break
                    con.send(struct.pack("c", "N"))
            except:
                datos = struct.unpack("c",data)
                print dir[0], "quiere saber su puntuaje"
                info = ""
                info += struct.pack("i", a)
                info += struct.pack("i", e)
                con.send(info)
        except:
            con.close()
            clientes.remove((dir[0]))
            print dir[0], "se fue"
            break

while True:
    con, dir = sock.accept()
    start_new_thread(client,(con,dir))

sock.close()
