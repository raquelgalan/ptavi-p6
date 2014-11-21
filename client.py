#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.

try:

    METODO = sys.argv[1]
    
    if METODO != "INVITE" and METODO != "BYE":
        raise SystemExit
        
    LOGIN = sys.argv[2]
    IP_PORT = LOGIN.split("@")[1]
    PORT = int(LOGIN.split(":")[1]) 
    print PORT
    SERVER = IP_PORT.split(":")[0]
    print SERVER

#except ValueError:
#    print ("Error: El puerto necesita ser entero")

#except IndexError:
except:
    print ("Usage: python client.py method receiver@IP:SIPport")
    raise SystemExit


# Contenido que vamos a enviar

RECEPTOR = LOGIN.split("@")[0]

LINE = METODO + " sip:" + RECEPTOR + "@" + SERVER + " SIP/2.0"
try:
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)
except socket.error:
    print ("Error: No server listening at " + SERVER + " port " + str(PORT))
    raise SystemExit

print 'Recibido -- \r\n', data
if data == " SIP/2.0 100 Trying\r\n\r\n" + " SIP/2.0 180 Ring\r\n\r\n" + " SIP/2.0 200 OK\r\n\r\n":
    METODO = "ACK"
    LINE = METODO + " sip:" + RECEPTOR + "@" + SERVER + " SIP/2.0"
    my_socket.send(LINE + '\r\n')

    
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
