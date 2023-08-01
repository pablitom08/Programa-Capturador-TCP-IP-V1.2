import socket
import sys
import CrearExcel
import time
import random

# Create a TCP/IP socket
MAX_RETRIES = 10  # número máximo de intentos de conexión
INITIAL_BACKOFF = 5  # tiempo de espera inicial en segundos
class SensorStreamingTest(object):
    def __init__(self):    
        self.bucle = None
        self.retry = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reconnecting = False  # booleano que indica si se está intentando reconectar o no
    

    def conectar(self, host, port, directorio):
        self.bucle = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        print(directorio)
        port1=int(port)
        server_address = (host, port1)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)
        
        while self.retry < MAX_RETRIES:
            try:

                # Send data
                message = b'This is the message.  It will be repeated.'
                #print('sending {!r}'.format(message))
                #sock.sendall(message)

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                while self.bucle:
                    if not self.reconnecting:
                        data = self.sock.recv(1024)
                        amount_received += len(data)
                        datos=data.decode('UTF-8')
                        #print("punto de control 1")
                        CrearExcel.registro(datos,directorio)
                        #report_txt.registro(datos,directorio)
                        #print('received {!r}'.format(data))
                        print(datos)

            except:
                self.sock.close()
                sys.exit(0)
            #sock.close()
            if retry >= MAX_RETRIES:
                print('Máximo número de intentos de conexión alcanzado. Saliendo del programa...')
                break
            else:
                backoff = exponential_backoff(retry)
                print(f'No se pudo establecer conexión. Intentando de nuevo en {backoff} segundos...')
                time.sleep(backoff)
                retry += 1
                self.reconnecting = True  # activar booleano para indicar que se está intentando reconectar
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(server_address)
                self.reconnecting = False  # desactivar booleano cuando se reconecta con éxito  
              
    def exponential_backoff(self,retry):
        """Calcula el tiempo de espera exponencial para el siguiente intento."""
        return INITIAL_BACKOFF * (2 ** retry) + random.randint(0, 2)



    def cerrar(self):
        self.sock.close()
        print('closing socket')
        time.sleep(1)
        self.bucle = False


if __name__ == '__main__':
    h= '192.168.100.141'
    p=4001
    directorio=None
    SensorStreamingTest(h, p)
    MAX_RETRIES = 10  # número máximo de intentos de conexión
    INITIAL_BACKOFF = 5  # tiempo de espera inicial en segundos
