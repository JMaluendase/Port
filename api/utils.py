import random
import string
from django.conf import settings


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yagmail

from sms_api.altiria_client import *
from rest_framework import status

from rest_framework.response import Response
from rest_framework import status

def getMothStr(Per_MM, anio):
    listMoth = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    return listMoth[Per_MM - 1] + " " + str(anio)

def getCompanyStr(code):
    dicCompany = {277: "BER", 278: "BTR", 310: "CIT", 320: "TLN", 300: "COL", 2771: "TCB"}
    return dicCompany.get(code)

def getNameFile(empresa, numero, mes, anio):
    listMoth = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    dicCompany = {277: "BER", 278: "BTR", 310: "CIT", 320: "TLN", 300: "COL", 2771: "TCB"}
    return dicCompany.get(empresa) + "_EXTRACTO_VEHICULO_" + str(numero) + "_" + listMoth[mes - 1] + "_" + str(anio) + ".PDF"

def getNameFilePlanilla(empresa, numero, mes, anio):
    listMoth = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    dicCompany = {277: "BER", 278: "BTR", 310: "CIT", 320: "TLN", 300: "COL", 2771: "TCB"}
    return dicCompany.get(empresa) + "_PLANILLAS_VEHICULO_" + str(numero) + "_" + listMoth[mes - 1] + "_" + str(anio) + ".PDF"

def getNameFileCertificado(documento, empresa, mes, anio):
    dicCompany = {277: "BER", 278: "BTR", 310: "CIT", 320: "TLN", 300: "COL", 2771: "TCB"}
    return dicCompany.get(empresa) + "_CERTIFICADO_" + str(documento) + "_" + str(mes) + "-" + str(anio) + ".PDF"

def generadorToken():
    # Cargar el alfabeto
    alfabeto = string.ascii_uppercase

    # Generar números aleatorios
    n_1 = random.randint(0, 25)
    n_2 = random.randint(0, 25)
    n_3 = random.randint(0, 25)
    n_4 = random.randint(0, 9)
    n_5 = random.randint(0, 9)
    n_6 = random.randint(0, 9)

    # Generar letras aleatorias
    letra_1 = alfabeto[n_1]
    letra_2 = alfabeto[n_2]
    letra_3 = alfabeto[n_3]

    # Generar el token
    token = letra_1 + str(n_4) + letra_2 + str(n_5) + letra_3 + str(n_6)

    return token

def getHora():
    print(settings.TIME_ZONE)

def testSendEmail():
    return True

def testSendSMS():
    return True

def enviar_mail_token(destinatario, token):
    
    try:
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

        # Crear objeto de mensaje
        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = 'Código de autorización'
        mensaje['From'] = 'Token de seguridad Portal <' + smtp_username + '>'
        mensaje['To'] = destinatario

        # Contenido HTML del mensaje
        contenido_html = f""" <table border="0" width="90%" cellspacing="0" cellpadding="0" bgcolor="#FFFFFF">
                                <tbody>
                                    <tr>
                                        <td>&iexcl;Hola apreciado afiliado!</td>
                                    </tr>
                                    <tr>
                                        <td>&nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td>Este es el token de seguridad para&nbsp;<strong>Ingresar al portal web</strong>. Ingresa el siguiente&nbsp;<strong>c&oacute;digo </strong>para completar el proceso:&nbsp;
                                    <div>
                                        <h2 style="text-align: center;"><span style="background-color: #ffff00;">{token}</span></h2>
                                    </div>
                                    </td>
                                    </tr>
                                    <tr>
                                    <td>&nbsp;</td>
                                    </tr>
                                    <tr>
                                    <td>Gracias por utilizar nuestros canales virtuales.</td>
                                    </tr>
                                </tbody>
                            </table> """

        # Crear parte HTML del mensaje
        contenido_html_parte = MIMEText(contenido_html, 'html')

        # Adjuntar parte HTML al mensaje
        mensaje.attach(contenido_html_parte)

        # Establecer conexión SMTP y enviar correo
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            failed_recipients = server.send_message(mensaje, smtp_username, destinatario)
            print(failed_recipients)
            #result = server.sendmail(smtp_username, destinatario, mensaje.as_string())

        if not failed_recipients:
            # El mensaje se envió satisfactoriamente a todos los destinatarios
            print("ENTREGADO!")
            return True
        else:
            # El mensaje no se pudo entregar a algunos destinatarios
            # Puedes imprimir los detalles de los destinatarios no entregados si lo deseas
            print('No se pudo entregar el mensaje a los siguientes destinatarios:')
            for recipient in failed_recipients:
                print(f'Destinatario: {recipient}')
            return False
        
        return result
        if result.get('status') == 200:
            return True
        else:
            return False
        
            # if not result:
            #     return True
            # else:
            #     print('No se pudo entregar el mensaje a los siguientes destinatarios:')
            #     for recipient, error in result.items():
            #         print(f'Destinatario: {recipient}, Error: {error}')
            #     return False
        
    except Exception as e:
        print('MAIL Exception ERROR:', str(e))
        return False
    
def enviar_mail2_token(destinatario, token):
    try:
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

        #token_mail = "[" + "]-[".join(token) + "]"
        token_mail = " - ".join(token)

                # Contenido HTML del mensaje
        mensaje = f""" <div>Apreciado afiliado.</div>
                        <div><br />Este es el token de seguridad para&nbsp;<strong>Ingresar al portal web de afiliados</strong>. ingrese los&nbsp;<strong>d&iacute;gitos</strong> en las casillas de validaci&oacute;n del portal para completar el proceso:&nbsp;</div>
                        <div>
                        <h1 style="text-align: center;"><span style="background-color: #ffff00;">{token_mail}</span></h1>
                        <div style="text-align: center !important;"><input style="width: 5%; height: 40px; font-size: 18px;" type="text" value="   {token[0:1]}" /> <input style="width: 5%; height: 40px; font-size: 18px;" type="text" value="   {token[1:2]}" /> <input style="width: 5%; height: 40px; font-size: 18px;" type="text" value="   {token[2:3]}" /> <input style="width: 5%; height: 40px; font-size: 18px;" type="text" value="   {token[3:4]}" /> <input style="width: 5%; height: 40px; font-size: 18px;" type="text" value="   {token[4:5]}" /> <input style="width: 5%; height: 40px; font-size: 18px;" type="text" value="   {token[5:]}" /></div>
                        <p>Este mensaje se ha generado de manera&nbsp;<strong>AUTOM&Aacute;TICA, POR FAVOR NO RESPONDER ESTE CORREO.</strong></p>
                        <div>Gracias por utilizar nuestros canales virtuales.</div>
                        </div>  """

        yag = yagmail.SMTP(user=smtp_username, password=smtp_password, host=smtp_host, port=smtp_port)
        envio = yag.send(to=destinatario, subject='Código de autorización', contents=mensaje)
        #print(envio)
        # El mensaje se envió satisfactoriamente
        return True

    except Exception as e:
        print('MAIL Exception ERROR:', str(e))
        return False
    
def enviar_mail2_pqr(destinatario, solicitud, nombre, telefono, correo):
    try:
        smtp_host = settings.EMAIL_HOST
        smtp_port = settings.EMAIL_PORT
        smtp_username = settings.EMAIL_HOST_USER
        smtp_password = settings.EMAIL_HOST_PASSWORD

                # Contenido HTML del mensaje
        mensaje = f""" <div>Apreciado colaborador.</div>
                        <div><br />Se ha registrado una solicitud por parte de un afiliado desde el portal de propietarios.</div>
                        <div>&nbsp;</div>
                        <div><strong>Detalles de la solicitud: </strong></div>
                        <div>&nbsp;</div>
                        <div>{solicitud}.</div>
                        <div>&nbsp;</div>
                        <div><strong>Nombre del Afiliado:</strong> {nombre}</div>
                        <div><strong>Tel&eacute;fono del Afiliado:</strong> {telefono}</div>
                        <div><strong>Correo del afiliado:</strong> {correo}</div>
                        <div>
                        <div style="text-align: center !important;">&nbsp;</div>
                        <p>Este mensaje se ha generado de manera&nbsp;<strong>AUTOM&Aacute;TICA, POR FAVOR NO RESPONDER ESTE CORREO.</strong></p>
                        <div>responda la solicitud al tel&eacute;fono o correo del propietario directamente.</div>
                        </div>  """

        yag = yagmail.SMTP(user=smtp_username, password=smtp_password, host=smtp_host, port=smtp_port)
        envio = yag.send(to=destinatario, subject='Solicitud de Afiliado', contents=mensaje)
        return True

    except Exception as e:
        print('MAIL Exception ERROR:', str(e))
        return False
    
def enviar_sms_token(llave, token):
    try:
        client = AltiriaClient(settings.SMS_USER, settings.SMS_PASS)
        textMessage = AltiriaModelTextMessage('57'+llave, 'Su token de confirmación para el ingreso al portal de afiliados es: ' + token)
        jsonText = client.sendSms(textMessage)
        return {"message": settings.MESSAGE_CONFIRM, "status":status.HTTP_201_CREATED, "json": jsonText}, 
    except AltiriaGwException as ae:
        code = ae.status
        details = str(ae.message)
        return {"message": settings.MESSAGE_ERROR, "details": details, "code": code, "status":status.HTTP_500_INTERNAL_SERVER_ERROR}, 
    except JsonException as je:
        details = str(je.message)
        return {"message": settings.MESSAGE_ERROR, "details": details, "status":status.HTTP_500_INTERNAL_SERVER_ERROR}, 
    except ConnectionException as ce:
        if "RESPONSE_TIMEOUT" in ce.message: 
            details = str('Tiempo de respuesta agotado:'+ce.message)
            return {"message": settings.MESSAGE_ERROR, "details": details, "status":status.HTTP_500_INTERNAL_SERVER_ERROR}, 
        else:
            details = str('Tiempo de conexión agotado:'+ce.message)
            return {"message": settings.MESSAGE_ERROR, "details": details, "status":status.HTTP_500_INTERNAL_SERVER_ERROR}, 
