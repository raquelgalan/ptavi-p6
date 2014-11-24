#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Raquel Galán Montes
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Verificar los argumentos
try:

    METODO = sys.argv[1]

    if METODO != "INVITE" and METODO != "BYE":
        raise SystemExit

    LOGIN = sys.argv[2]
    IP_PORT = LOGIN.split("@")[1]
    PORT = int(LOGIN.split(":")[1])
    SERVER = IP_PORT.split(":")[0]

except:
    print ("Usage: python client.py method receiver@IP:SIPport")
    raise SystemExit

# Contenido que vamos a enviar
RECEPTOR = LOGIN.split("@")[0]

LINE = METODO + " sip:" + RECEPTOR + "@" + SERVER + " SIP/2.0"

# Verificar el servidor y el puerto
try:
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    # Si el argumento 1 es invite o bye se envia el contenido
    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n\r\n')
    data = my_socket.recv(1024)
except socket.error:
    print ("Error: No server listening at " + SERVER + " port " + str(PORT))
    raise SystemExit
s = "SIP/2.0 "
e = "\r\n\r\n"
print 'Recibido -- \r\n\r\n', data

# Si se recibe 100, 180 y 200 se envia ACK con el contenido
if data == s + "100 Trying" + e + s + "180 Ringing" + e + s + "200 OK" + e:
    METODO = "ACK"
    LINE = METODO + " sip:" + RECEPTOR + "@" + SERVER + " SIP/2.0"
    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n\r\n')

print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
