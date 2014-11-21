#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            lista = line.split()
            
            if line != "":
                if len(lista) == 3:
                    #print len(lista)
                    print "El cliente nos manda: " + line
                    metodo = line.split(" ")[0]
                    print metodo
                    
                    if metodo == "INVITE":
                        trying = " SIP/2.0 100 Trying\r\n"
                        self.wfile.write(trying)
                        Ring = " SIP/2.0 180 Ring\r\n"
                        self.wfile.write(Ring)
                        line = " SIP/2.0 200 OK\r\n"
                        self.wfile.write(line)
                     
                    elif metodo == "ACK":
                        print "RTP"
                        aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < ' + fichero_audio
                        print "Vamos a ejecutar", aEjecutar
                        os.system(aEjecutar)
                        print "Finaliza"

                    elif metodo == "BYE":
                        line = " SIP/2.0 200 OK\r\n"
                        self.wfile.write(line)
                    else:
                        print "metodo incorrecto"
                        line = " SIP/2.0 405 Method Not Allowed\r\n"
                        self.wfile.write(line)
                else:
                    print "metodo incorrecto"
                    line = " SIP/2.0 400 Bad Request\r\n\r\n"
                    self.wfile.write(line)

            # Si no hay más líneas salimos del bucle infinito
            else:
                break


if __name__ == "__main__":
    
    try:

        SERVER = sys.argv[1]
        PORT = int(sys.argv[2])
        fichero_audio = str(sys.argv[3])

        # Creamos servidor de eco y escuchamos
        serv = SocketServer.UDPServer(("", PORT), EchoHandler)
        print "Listening..."
        serv.serve_forever()

    except:
        print ("Usage: python server.py IP port audio_file")
        raise SystemExit
