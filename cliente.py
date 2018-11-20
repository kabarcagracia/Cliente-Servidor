#----------------------------------
#librerias
import socket
#----------------------------------
#consulta ip equipo cliente
equipo = socket.gethostname()
ip1 = socket.gethostbyname(equipo)
#----------------------------------
#separo los octetos de la ip y recolecto el ultimo octeto.
lista_octetos = ip1.split('.')
ip_origen = lista_octetos[3]
ip_origen1 = hex(int(ip_origen))
#----------------------------------
#direccion de destino es sabida y se recolecta el ultimo octeto.
ip = '172.20.10.3'
lista_octetos1 = ip.split('.')
ip_destino = lista_octetos1[3]
ip_destino1 = hex(int(ip_destino))
start_byte = '0xc5'
largo = '0x07'
checksum = ''
#----------------------------------
#conexion tcp/ip
s = socket.socket()
s.connect((ip, 9999))
while True:
    print 'PROTOCOLO COMUNICACIÓN'
    print '======================='
    print '=  INGRESAR OPCIÓN    ='
    print '=  a) Activar         ='
    print '=  b) Desactivar      ='
    print '======================='
    seleccion_cmd = raw_input()
    if(seleccion_cmd == 'a'):
        cmd = '0xff'
        mensaje = 'ACTIVANDO GPIO:'
    elif(seleccion_cmd == 'b'):
        cmd = '0x00'
        mensaje = 'DESACTIVANDO GPIO:'
    print '======================='
    print '=  ¿Cual GPIO? (1-5)  ='
    print '======================='
    seleccion_data = raw_input()
    data = hex(int(seleccion_data))
    print '-----------------------'
    print mensaje+data
    print '-----------------------'
    #================================
    #checksum
    c1 = int(start_byte, 16)
    c2 = int(largo, 16)
    c3 = int(ip_origen)
    c4 = int(ip_destino)
    c5 = int(cmd, 16)
    c6 = int(data, 16)
    ct = c1+c2+c3+c4+c5+c6
    check = hex(ct)
    checksum = check[0:4]
    #trama final
    trama = start_byte +','+largo+','+ip_origen1+','+ip_destino1+','+cmd+','+data+','+checksum
    s.send(trama)

