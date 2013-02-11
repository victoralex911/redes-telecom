from socket import *
from thread import *
import struct
import time
from sys import argv

if len(argv)==2:
    ip=argv[1]
else:
    ip=raw_input("IP del servidor: ")
port=5008
data = ""

sock = socket()
sock.connect((ip, port))

while True:
    numero = raw_input("Numero: ")
    try:
        valor = int(numero)
        sock.send(struct.pack("i", valor))
    except:
        sock.send(struct.pack("c", numero))
    inf = sock.recv(1024)
    try:
        datos = struct.unpack("c", inf)
        if datos[0] == "N":
            print "no es"
        if datos[0] == "Y":
            print "si es"
            print "Espera..."
            time.sleep(2)
        if datos[0] == "P":
            print "Has perdido"
            sock.close()
            break
    except:
        datos = struct.unpack("ii", inf)
        print "Tu puntuacion actual es:", datos[0]
        print "Llevas",datos[1], "errores"
