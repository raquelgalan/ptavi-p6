#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# Raquel Galán Montes
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import SocketServer
import sys
import os
# Para comprobar que los ficheros coinciden con el nombre
import os.path


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            # El cliente envía: METODO "sip:"RECEPTOR"@"SERVER "SIP/2.0"
            line = self.rfile.read()
            lista = line.split()
            if line != "":
                if len(lista) == 3:
                    print "El cliente nos manda: " + line
                    metodo = line.split(" ")[0]

                    if metodo == "INVITE":
                        print "Comienza INVITE"
                        trying = "SIP/2.0 100 Trying\r\n\r\n"
                        self.wfile.write(trying)
                        Ringing = "SIP/2.0 180 Ringing\r\n\r\n"
                        self.wfile.write(Ringing)
                        line = "SIP/2.0 200 OK\r\n\r\n"
                        self.wfile.write(line)
                        print "Acaba INVITE"

                    elif metodo == "ACK":
                        print "Recibido ACK"
                        print "Comienza RTP"
                        aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 < '
                        aEjecutar += FICHERO_AUDIO
                        print "Vamos a ejecutar", aEjecutar
                        os.system(aEjecutar)
                        print "Acaba RTP"

                    elif metodo == "BYE":
                        print "Comienza BYE"
                        line = "SIP/2.0 200 OK\r\n\r\n"
                        self.wfile.write(line)
                        print "Acaba BYE"
                    else:
                        print "metodo incorrecto"
                        line = "SIP/2.0 405 Method Not Allowed\r\n\r\n"
                        self.wfile.write(line)
                else:
                    print "metodo incorrecto"
                    line = "SIP/2.0 400 Bad Request\r\n\r\n"
                    self.wfile.write(line)

            # Si no hay más líneas salimos del bucle infinito
            else:
                break


if __name__ == "__main__":

    try:
        # Verificar los argumentos
        SERVER = sys.argv[1]
        PORT = int(sys.argv[2])
        FICHERO_AUDIO = str(sys.argv[3])

        # os.path.exists solo devuelve True si hay un fichero con ese nombre
        if os.path.exists(FICHERO_AUDIO) is False:
            raise SystemExit
        # Sale error si le introducimos argumentos de más
        parametros = len(sys.argv)
        if parametros != 4:
            print "parametros"
            raise SystemExit

        # Creamos servidor de eco y escuchamos
        serv = SocketServer.UDPServer(("", PORT), EchoHandler)
        print "Listening..."
        serv.serve_forever()

    except:
        print ("Usage: python server.py IP port audio_file")
        raise SystemExit
