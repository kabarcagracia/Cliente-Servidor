import smtplib
import picamera
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(5, GPIO.OUT)
estado_actual = '0'
estado = int('0')
while True:
    time.sleep(5)
    estado_actual = GPIO.input(4)
    if (estado_actual >> estado):
        GPIO.output(5, GPIO.HIGH)
        with picamera.PiCamera() as picam:
            picam.capture('alerta.jpg')
            picam.stop_preview()
            picam.close()
        # Iniciamos los parámetros del script
        remitente = 'redesdedatos2197@gmail.com'
        destinatarios = ['kevinabarca1197@gmail.com']
        asunto = '[RPI] Correo de prueba'
        cuerpo = 'CUIDADO PERSONA DETECTADA'
        ruta_adjunto = 'alerta.jpg'
        nombre_adjunto = 'alerta.jpg'
        # Creamos el objeto mensaje
        mensaje = MIMEMultipart()
        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto
        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        # Abrimos el archivo que vamos a adjuntar
        archivo_adjunto = open(ruta_adjunto, 'rb')
         
        # Creamos un objeto MIME base
        adjunto_MIME = MIMEBase('application', 'octet-stream')
        # Y le cargamos el archivo adjunto
        adjunto_MIME.set_payload((archivo_adjunto).read())
        # Codificamos el objeto en BASE64
        encoders.encode_base64(adjunto_MIME)
        # Agregamos una cabecera al objeto
        adjunto_MIME.add_header('Content-Disposition', "attachment; filename=      %s" % nombre_adjunto)
        # Y finalmente lo agregamos al mensaje
        mensaje.attach(adjunto_MIME)
         
        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
         
        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login('redesdedatos2197@gmail.com','mentiras2018')

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)

        # Cerramos la conexión
        sesion_smtp.quit()
    else:
        GPIO.output(5, GPIO.LOW)
        print 'NORMAL'
