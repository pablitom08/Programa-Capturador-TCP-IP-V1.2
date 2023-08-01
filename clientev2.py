import socket
import sys
import CrearExcel
import time
import random
import logging
import getpass


MAX_RETRIES = 40  # número máximo de intentos de conexión
INITIAL_BACKOFF = 5  # tiempo de espera inicial en segundos

# configuración del logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# archivo de logs
apoyodir=getpass.getuser()
log_file = f"C:/Users/{apoyodir}/Documents/TCPIP-DATALOGGER/conexion.log"
#log_file = actual+/'conexion.log'
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)

# formato del mensaje de log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# agregamos el handler al logger
logger.addHandler(handler)

class SensorStreamingTest(object):
    def __init__(self):
        self.sock = None
        self.connected = False
        self.cerrando = False
 
    def conectar(self, host, port, directorio):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (host, int(port))
            logger.info('conectando a {} puerto {}'.format(*server_address))
            self.sock.connect(server_address)
        except (TimeoutError, OSError, socket.error) as e:
            logger.error(f'Ocurrió un error al realizar la operación de socket: {e}')
            return
            
        self.connected = True
        self.cerrando = False
        logger.info('conexión establecida')
        print('conexión establecida')

        while True:
            if not self.connected:
                logger.info('perdida de conexión, intentando reconexión...')
                retry = 0
                while retry < MAX_RETRIES:
                    try:
                        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.sock.connect(server_address)
                        self.connected = True
                        logger.info('conexión restablecida')
                        break
                    except socket.error as e:
                        logger.error(f'no se pudo restablecer la conexión: {e}')
                        retry += 1
                        backoff = self.exponential_backoff(retry)
                        logger.info(f'intentando de nuevo en {backoff} segundos...')
                        time.sleep(backoff)
                if not self.connected:
                    logger.error('no se pudo restablecer la conexión después de varios intentos, deteniendo el cliente...')
                    break

            try:
                data = self.sock.recv(1024)
                if not data:
                    logger.info('conexión cerrada por el servidor')
                    self.connected = False
                    continue
                datos=data.decode('UTF-8')
                CrearExcel.registro(datos,directorio)
                logger.info(datos)
            except socket.error as e:
                logger.info(f'error de socket: {e}')
                self.connected = False
                self.cerrando = False
                logger.info('conexión perdida')
                #print('conexión perdida')
                break
            
           # if not self.cerrando:
            #    logger.info('conexión restablecida')
             #   print('conexión restablecida')

    def cerrar(self):
        self.cerrando = True
        self.connected = False
        try:
            if self.sock is not None:
                self.sock.close()
                logger.info('socket cerrado')
                print('socket cerrado')
            else:
                logger.info('socket ya cerrado')
        except socket.error as e:
            logger.error(f'error de socket al cerrar: {e}')


    def exponential_backoff(self, retry):
        backoff = INITIAL_BACKOFF * (2 ** retry) + random.randint(0, 1000)/1000
        return min(backoff, 800)  # límite de espera de 10 minutos


if __name__ == '__main__':
    h= '192.168.100.141'
    p=4001
    directorio=None
    SensorStreamingTest(h, p)
    MAX_RETRIES = 10  # número máximo de intentos de conexión
    INITIAL_BACKOFF = 5  # tiempo de espera inicial en segundos
