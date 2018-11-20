#LIBRERIAS
import time
import socket
import RPi.GPIO as GPIO
#IP SERVIDOR
equipo = socket.gethostname()
ip = socket.gethostbyname(equipo)
#CONEXION TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 9998))
s.listen(1)
sc, addr = s.accept()
#=======================================
#DECLARACION PINES
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#=======================================
rojo = 5
azul = 6
blanco = 13
amarillo = 19
verde = 26
GPIO.setup(rojo, GPIO.OUT)
GPIO.setup(azul, GPIO.OUT)
GPIO.setup(blanco, GPIO.OUT)
GPIO.setup(amarillo, GPIO.OUT)
GPIO.setup(verde, GPIO.OUT)
print ("=========================================")
print ("==         Conexion Establecida        ==")
print ("==                                     ==")
print ("==           ESPERANDO TRAMA           ==")
print ("==                                     ==")
print ("=========================================")
mensaje = '' 
while True:
    trama = sc.recv(1024)
    while (trama !=' '):
        lista_trama = trama.split(',')
        byte_inicio = lista_trama[0]
        largo = lista_trama[1]
        ip_origen = lista_trama[2]
        ip_destino = lista_trama[3]
        cmd = lista_trama[4]
        data = lista_trama[5]
        checksum = lista_trama[6]
        x1 = int(byte_inicio, 16)
        x2 = int(largo, 16)
        x3 = int(ip_origen, 16)
        x3a = str(x3)
        x4 = int(ip_destino, 16)
        x5 = int(cmd, 16)
        x6 = int(data, 16)
        x6a = str(x6)
        #calculo checksum
        xt = x1+x2+x3+x4+x5+x6
        check = hex(xt)
        checksum1 = check[0:4]
        if(checksum1 == checksum):
            print '--------------------------------------'
            print '         CHECKSUM CORRECTO            '
            print '--------------------------------------'
            print '    DESPLEGANDO INFORMACION ESPERE....'
            time.sleep(1)
            print cmd
            if(cmd == '0xff'):
                mensaje = 'ACTIVANDO GPIO:'
                GPIO.output(rojo, GPIO.HIGH)
            elif(cmd == '0x00'):
                mensaje = 'DESACTIVANDO GPIO:'
                GPIO.output(rojo, GPIO.LOW)
            print '======================================'
            print '    IP ORIGEN: 192.168.0.'+x3a
            print '    IP DESTINO : '+ip
            print '    '+mensaje+x6a
            print '======================================'
        else:
            print '--------------------------------------'
            print '        CHECKSUM INCORRECTO           '
            print '--------------------------------------'
        trama = ' '
            
sc.close()
s.close()
