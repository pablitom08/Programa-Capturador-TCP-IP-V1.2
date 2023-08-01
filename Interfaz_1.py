from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font

import pystray
from PIL import Image

import time
from threading import Thread
import os

import pystray
from PIL import Image
import re
import clientev2
import getpass

import ipaddress

cnx = clientev2.SensorStreamingTest()
directorio=""

# Establecer la carpeta predeterminada
username = getpass.getuser()
default_folder = os.path.join('C:', os.sep, 'Users', username, 'Documents', 'mi_carpeta')
default_folder2 = os.path.join('C:', os.sep, 'Users', username, 'Documents', 'TCPIP-DATALOGGER')


# Crear una variable de cadena para almacenar la ruta de la carpeta seleccionada
##selected_folder = StringVar(value=default_folder)

def confirmar_salida():
    respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas salir?")
    if respuesta:
        raiz.quit()


def minimize_to_tray():
    # Ocultar la ventana principal
    raiz.withdraw()
    # Crear el icono de la bandeja del sistema
    icon = pystray.Icon("example_icon", Image.open(default_folder2+'/'+'tecni.png'))
    # Agregar una acción para restaurar la ventana al hacer clic en el icono
    def restore_window(icon, item):
        raiz.deiconify()
        icon.stop()
    icon.menu = pystray.Menu(pystray.MenuItem("Restaurar", restore_window))
    # Mostrar el icono en la bandeja del sistema
    icon.run()

def validar_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def conexion():
    time.sleep(1)
    Ip=IP_es.get()
    Verificacion=validar_ip(Ip)
    puerto=Port_ip.get()
    apoyodir=getpass.getuser()
    actual ="C:/Users/"+apoyodir+"/Documents/Informes"

    if Ip!="" and puerto!= "" and Verificacion == True:
        botonenvio['state'] = DISABLED
        estado=1
        #clientev2.SensorStreamingTest(Ip,puerto)
        cuadroTexto2=Label(miFrame, bg="white", text="")
        cuadroTexto2.place(x=150, y=360)
        cuadroTexto2=Label(miFrame, bg="white", text="CONECTADO", font=('Classic Robot', 20), fg="green")
        cuadroTexto2.place(x=110, y=150)
        fondo3 = PhotoImage(file=default_folder2+'/'+'wifi.png')
        fondo4=Label(miFrame,bg="white",image=fondo3).place(x=298,y=147)
        #print(directorio)
        if os.path.exists(directorio):
            #print(directorio)
            cnx.conectar(Ip,puerto,directorio)
        elif not os.path.exists(directorio):
            #print(actual)
            cnx.conectar(Ip,puerto,actual)  
        else:
            messagebox.showwarning('Mensaje','NO HA INGRESADO UN DIRECTORIO DONDE ALMACENAR EL ARCHIVO!!')
            print("The path is either for a file or not valid")  
    else:
         botonenvio['state']==NORMAL
         messagebox.showwarning('Mensaje','Debe ingresar una IP o Puerto correcto')

def desconexion():
    time.sleep(1)
    cnx.cerrar()
    if botonsalir['state']==NORMAL:
        botonenvio['state'] = NORMAL
        cuadroTexto2=Label(miFrame, bg="white", text="")
        cuadroTexto2.place(x=130, y=360)
        cuadroTexto2=Label(miFrame, bg="white", text="NO CONECTADO",font=('Classic Robot', 17), fg="red")
        cuadroTexto2.place(x=107, y=150)
        #sys.exit(0)

def codigoBoton():
    hilo1=Thread(target=conexion)
    hilo1.daemon = True 
    hilo1.start()

def codigoBoton2():
    desconexion()

        #print("lo logre")


def carpeta():
    global directorio, actual
    directorio=filedialog.askdirectory()
    selected_folder.set(directorio)
    cuadroTexto2=Label(miFrame, bg="white", text=directorio,font=('Classic Robot', 8))
    cuadroTexto2.place(x=30, y=290)
    if directorio!="":
        os.chdir(directorio)
        #print(directorio)

##########entradas

if __name__ == "__main__" :
    global Ip, puerto, hilo1
        #directorio=None
    ##########entradas
    raiz=Tk()   

    IP_es=StringVar()
    Port_ip=StringVar()
    Save_R=StringVar()
        
    # Establecer la carpeta predeterminada
    username = getpass.getuser()
    default_folder = os.path.join('C:', os.sep, 'Users', username, 'Documents', 'Prueba')

    # Crear una variable de cadena para almacenar la ruta de la carpeta seleccionada
    selected_folder = StringVar(value=default_folder)

    raiz.title("Data Logger simple")
    raiz.resizable(0,0) #ancho, #alto de tipo booleano, sirve para redimensionar
    raiz.iconbitmap(default_folder2+'/'+'tecni.ico')
    miFrame=Frame(raiz, width=400,height=500)
    miFrame.pack()
    
    miFrame.config(bg="white",bd="5",width="400",height="400", relief="groove")
    miLabel= Label(miFrame, bg="white",text="CAPTURADOR DE DATOS POR TCP",font=('Classic Robot', 14))
    miLabel.place(x=10, y=100)

    fondo = PhotoImage(file=default_folder2+'/'+'LOGOT2.png')
    fondo1=Label(miFrame,bg="white",image=fondo).place(x=150,y=30)


    fondo4 = PhotoImage(file=default_folder2+'/'+'wifiN.png')
    fondo5=Label(miFrame,bg="white",image=fondo4).place(x=296,y=145)

    cuadroTexto2=Label(miFrame, bg="white", text="NO CONECTADO",font=('Classic Robot', 16), fg="red")
    cuadroTexto2.place(x=107, y=150)

    cuadroTexto=Entry(miFrame, textvar=IP_es,font=('Classic Robot', 11))
    cuadroTexto.place(x=145, y=200)
    cuadroTexto.insert(0, "192.168.3.54")

    nombreLabel1= Label(miFrame, bg="white",text="IP:",font=('Classic Robot', 10))
    nombreLabel1.place(x=70, y=200)

    cuadroTexto1=Entry(miFrame, textvar=Port_ip,font=('Classic Robot', 11))
    cuadroTexto1.place(x=145, y=230)
    cuadroTexto1.insert(0, "4001")

    nombreLabel2= Label(miFrame, bg="white",text="PUERTO:",font=('Classic Robot', 10))
    nombreLabel2.place(x=70, y=230)

    nombreLabel3= Label(miFrame, bg="white", text="GUARDAR:",font=('Classic Robot', 10))
    nombreLabel3.place(x=70, y=265)


    botonenvio=Button(miFrame, text="Iniciar", command=codigoBoton,state=NORMAL,font=('Classic Robot', 10))
    botonenvio.place(x=100, y=320)
    raiz.after(1000, codigoBoton)

    botonsalir=Button(miFrame, text="Detener", command=codigoBoton2, state=NORMAL,font=('Classic Robot', 10))
    botonsalir.place(x=200, y=320)

    botonminimizar=Button(miFrame, text="Mini", command=minimize_to_tray,font=('Classic Robot', 10))
    botonminimizar.place(x=350, y=365)
    raiz.after(4000, minimize_to_tray)

    botondirectorio=Button(miFrame, text="seleccionar", command=carpeta, state=NORMAL,font=('Classic Robot', 10))
    botondirectorio.place(x=150, y=260)
    
#Para salir de la ventana se crea una confirmacio
    raiz.protocol("WM_DELETE_WINDOW", confirmar_salida)
    raiz.mainloop()
