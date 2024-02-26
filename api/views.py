
# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import AfiliadoVehiculo, Afiliado, Token, ExtractoVehiculo, PQR, DestinatarioPQR, Token2
from .utils import generadorToken, getHora, enviar_mail_token, enviar_mail2_pqr, enviar_sms_token, enviar_mail2_token, getMothStr, getCompanyStr, getNameFile, getNameFilePlanilla, getNameFileCertificado
from django.db.models import F, CharField, Func, Q
from django.db.models.functions import Cast
from sms_api.altiria_client import *
from django.db import transaction
import datetime
import requests


# Este método se usa para testear el API
class FunctionsView(APIView):
    def get(self, request, param):
        valor = getCompanyStr(param)
        return Response(valor, status=status.HTTP_200_OK)

# Devuelve los datos de contacto del afiliado.


class AfiliadoViewSet(APIView):
    def get(self, request, documento):

        afiliados = Afiliado.objects.filter(AfiliadoID=documento).first()

        afiliado = []

        if afiliados:
            text = ""
            text_2 = ""
            text_tel = ""
            existMail = False
            existMail2 = False
            existTel = False

            if afiliados.Correo != "" and afiliados.Correo != None:
                pos = afiliados.Correo.find("@")
                sub = afiliados.Correo[4:pos]
                tam = len(sub)
                star = tam * "*"
                text = afiliados.Correo.replace(sub, star)
                existMail = True

                elemento = {
                    'key': "C",
                    'llave': afiliados.Correo,
                    'name': f"Enviar correo al {text}" if text != "" else "No hay registro de Correo",
                    'exist': existMail,
                    'nombre': afiliados.Nombre
                }

                afiliado.append(elemento)

            if afiliados.Correo2 != "" and afiliados.Correo2 != None:
                pos = afiliados.Correo2.find("@")
                sub = afiliados.Correo2[4:pos]
                tam = len(sub)
                star = tam * "*"
                text_2 = afiliados.Correo2.replace(sub, star)
                existMail2 = True

                elemento = {
                    'key': "C1",
                    'llave': afiliados.Correo2,
                    'name': f"Enviar correo al {text_2}" if text_2 != "" else "No hay registro de Correo",
                    'exist': existMail2,
                    'nombre': afiliados.Nombre
                }

                afiliado.append(elemento)

            if afiliados.Telefono != "" and afiliados.Telefono != None:
                sub_tel = afiliados.Telefono[0:6]
                tam_tel = len(sub_tel)
                star_tel = tam_tel * "*"
                text_tel = afiliados.Telefono.replace(sub_tel, star_tel)
                existTel = True

                elemento = {
                    'key': "P",
                    'llave': afiliados.Telefono,
                    'name': f"Enviar mensaje de texto al {text_tel}" if text_tel != "" else "No hay registro de Teléfono",
                    'exist': existTel,
                    'nombre': afiliados.Nombre
                }

                afiliado.append(elemento)
        else:
            # afiliado = {}
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        return Response(afiliado, status=status.HTTP_200_OK)

# Actualizar datos de un Afiliado


class UpdateAfiliadoView(APIView):
    def put(self, request, format=None):
        try:
            afiliado_id = request.data.get('id')
            nombre = request.data.get('nombre')
            correo = request.data.get('correo')
            correo2 = request.data.get('correo2')
            telefono = request.data.get('telefono')

            afiliado = Afiliado.objects.get(AfiliadoID=afiliado_id)

            afiliado.Nombre = nombre
            afiliado.Correo = correo
            afiliado.Correo2 = correo2
            afiliado.Telefono = telefono

            afiliado.save()

            return Response({"message": settings.MESSAGE_CONFIRM}, status=status.HTTP_200_OK)

        except Afiliado.DoesNotExist:
            return Response({"message": "Afiliado no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            details = str(e)
            return Response({"message": settings.MESSAGE_ERROR, "details": details}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AfiliadoDataViewSet(APIView):
    def get(self, request, documento):

        afiliados = Afiliado.objects.filter(AfiliadoID=documento).first()

        afiliado = []

        if afiliados:

            elemento = {
                'AfiliadoID': afiliados.AfiliadoID,
                'Nombre': afiliados.Nombre,
                'Correo': afiliados.Correo,
                'Telefono': afiliados.Telefono,
                'Correo2': afiliados.Correo2,
            }

            afiliado.append(elemento)

        else:
            # afiliado = {}
            return Response({}, status=status.HTTP_404_NOT_FOUND)

        return Response(afiliado, status=status.HTTP_200_OK)

# Devuelve los vehículos que pueda tener el Afiliado


class AfiliadoVehiculoPorAfiliadoView(APIView):
    def get(self, request, documento):
        query = AfiliadoVehiculo.objects.filter(Q(AfiliadoID1=documento) | Q(AfiliadoID2=documento)).values(
            code=F('VehiculoID'),  # Renombra 'VehiculoPK' a 'code'
            name=F('NumVehiculo'),  # Renombra 'NumVehiculo' a 'name'
        ).distinct()

        return Response(query, status=status.HTTP_200_OK)

# Consulta la valides del Token digitado


class getToken2(APIView):
    def get(self, request, tokenid, documento):

        token2 = Token2.objects.filter(
            Numero=tokenid, Vencido=False, IdAfiliado=documento).first()
        print(token2)
        request.session['documento'] = documento
        # .annotate(
        # resta=F('Hora') - hora_actual_local,
        # )

        if token2:
            timezone.activate('America/Bogota')
            hora_actual_utc = timezone.now()
            hora_actual_local = timezone.localtime(
                hora_actual_utc, timezone.get_current_timezone())
            print(hora_actual_local)
            hora_col = token2.Hora.astimezone(timezone.get_current_timezone())
            print(hora_col)
            resta = hora_col.year - hora_actual_local.year + hora_col.month - hora_actual_local.month + \
                hora_col.day - hora_actual_local.day + hora_actual_local.hour - hora_col.hour

            token_data = {
                'Numero': token2.Numero,
                'Fecha': token2.Fecha,
                'Hora': hora_col,
                'Now': hora_actual_local,
                'Vencido': token2.Vencido,
                'Resta': resta,
                'Llave': token2.Llave,
                'documento': documento
            }
            #     print("Paso 2nd Print")
            # else:
            #     return Response({'message': 'Token no disponible'}, status=status.HTTP_404_NOT_FOUND)

            return Response(token_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Token no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class getToken(APIView):
    def get(self, request, tokenid, documento):

        token = Token.objects.filter(Numero=tokenid, Vencido=False).first()
        print(token)
        request.session['documento'] = documento
        # .annotate(
        # resta=F('Hora') - hora_actual_local,
        # )

        if token:
            timezone.activate('America/Bogota')
            hora_actual_utc = timezone.now()
            hora_actual_local = timezone.localtime(
                hora_actual_utc, timezone.get_current_timezone())
            print(hora_actual_local)
            hora_col = token.Hora.astimezone(timezone.get_current_timezone())
            print(hora_col)
            resta = hora_col.year - hora_actual_local.year + hora_col.month - hora_actual_local.month + \
                hora_col.day - hora_actual_local.day + hora_actual_local.hour - hora_col.hour

            token_data = {
                'Numero': token.Numero,
                'Fecha': token.Fecha,
                'Hora': hora_col,
                'Now': hora_actual_local,
                'Vencido': token.Vencido,
                'Resta': resta,
                'Llave': token.Llave,
                'documento': documento
            }
            #     print("Paso 2nd Print")
            # else:
            #     return Response({'message': 'Token no disponible'}, status=status.HTTP_404_NOT_FOUND)

            return Response(token_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Token no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Genera un nuevo Token y lo envía por correo o Telefono


class NuevoTokenView(APIView):

    def post(self, request, format=None):

        try:
            with transaction.atomic():
                tokenGenerico = generadorToken()
                vencimiento = False
                llave = request.data.get('llave')
                type = request.data.get('key')

                timezone.activate('America/Bogota')
                hora_actual_utc = timezone.now()
                hora_actual_local = timezone.localtime(
                    hora_actual_utc, timezone.get_current_timezone())

                token = Token(Numero=tokenGenerico, Fecha=hora_actual_local.date(), Hora=hora_actual_local,
                              Vencido=vencimiento, Llave=llave)
                token.save()

                if (type == "C" or type == "C1"):
                    mail = enviar_mail2_token(llave, tokenGenerico)
                    if mail:
                        return Response({"message": settings.MESSAGE_CONFIRM}, status=status.HTTP_201_CREATED)
                    else:
                        transaction.set_rollback(True)
                        return Response({"message": settings.MESSAGE_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    sms = enviar_sms_token(llave, tokenGenerico)
                    if sms[0].get("status") == 201:
                        return Response({"message": settings.MESSAGE_CONFIRM}, status=status.HTTP_201_CREATED)
                    else:
                        transaction.set_rollback(True)
                        return Response(sms, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            details = str(e)
            transaction.set_rollback(True)
            return Response({"message": settings.MESSAGE_ERROR, "details": details}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewPQRView(APIView):
    def post(self, request, format=None):
        try:
            with transaction.atomic():
                estado = False

                afiliado = request.data.get('afiliado')
                detalle = request.data.get('mensaje')
                nombre = request.data.get('nombre')
                telefono = request.data.get('telefono')
                correo = request.data.get('correo')
                destinatario = request.data.get('destinatario')
                destinatarioId = request.data.get('destinatarioId')

                timezone.activate('America/Bogota')
                hora_actual_utc = timezone.now()
                hora_actual_local = timezone.localtime(
                    hora_actual_utc, timezone.get_current_timezone())

                # Radicado, Fecha, Hora, Estado, Detalle, AfiliadoPQRID

                cuerpofecha = f"{str(hora_actual_local.date().year)}{str(hora_actual_local.date().month)}{str(hora_actual_local.date().day)}"
                cuerpohora = f"{str(hora_actual_local.hour)}{str(hora_actual_local.minute)}"
                radicado = f"{cuerpofecha}{cuerpohora}"

                afiliadoObject = Afiliado.objects.get(AfiliadoID=afiliado)
                destinatarioObject = DestinatarioPQR.objects.get(
                    id=destinatarioId)

                pqr = PQR(Radicado=radicado, Fecha=hora_actual_local.date(), Hora=hora_actual_local, Estado=estado,
                          Detalle=detalle, AfiliadoPQRID=afiliadoObject, DestinatarioPQRID=destinatarioObject)
                pqr.save()

                mail = enviar_mail2_pqr(
                    destinatario, detalle, nombre, telefono, correo)
                if mail:
                    return Response({"message": settings.MESSAGE_CONFIRM}, status=status.HTTP_201_CREATED)
                else:
                    transaction.set_rollback(True)
                    return Response({"message": settings.MESSAGE_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            details = str(e)
            transaction.set_rollback(True)
            return Response({"message": settings.MESSAGE_ERROR, "details": details}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExtractoVehiculoGetCompanyView(APIView):
    def get(self, request, documento, vehiculo):
        query = AfiliadoVehiculo.objects.filter(Q(AfiliadoID1=documento) | Q(AfiliadoID2=documento), VehiculoID=vehiculo).values(
            'EmpresaID',
        ).distinct()
        return Response(query, status=status.HTTP_200_OK)

# Devuelve los años para los cuales el vehículo contiene información


class ExtractoVehiculoGetAniosView(APIView):
    def get(self, request, documento, vehiculo, empresa):
        query = AfiliadoVehiculo.objects.filter(Q(AfiliadoID1=documento) | Q(AfiliadoID2=documento), VehiculoID=vehiculo, EmpresaID=empresa).values(
            'EmpresaID',
            code=F('Per_AA'),  # Devuelve entero
            name=Cast(F('Per_AA'), CharField()),  # Devuelve texto CAST
        ).distinct()
        return Response(query, status=status.HTTP_200_OK)

# Devuelve los meses para los cuales el vehículo contiene información


class ExtractoVehiculoGesMesView(APIView):
    def get(self, request, documento, vehiculo, periodo):
        query = AfiliadoVehiculo.objects.filter(Q(AfiliadoID1=documento) | Q(AfiliadoID2=documento), VehiculoID=vehiculo, Per_AA=periodo).values(
            ('Per_MM')
        ).distinct()
        return Response(query, status=status.HTTP_200_OK)

# Devuelve la data de un vehículo para un determinado mes, año, de x empresa


class ExtractoVehiculoMesView(APIView):
    def get(self, request, empresa, vehiculo, periodo, mes):
        # empresa-periodo-mes-pkVehiculo
        mes_formato = mes if mes > 9 else f"0{mes}"
        criterio = f"{empresa}{vehiculo}{periodo}{mes_formato}"
        query = ExtractoVehiculo.objects.filter(
            EmpresaPeriodoVehID=criterio).values()
        # return Response({'criterio': criterio}, status=status.HTTP_200_OK)
        return Response(query, status=status.HTTP_200_OK)

# Evaluar por el mes


class ExtractoVehiculoAnioView(APIView):
    def get(self, request, empresa, vehiculo, periodo):
        criterio = f"{empresa}{vehiculo}{periodo}"
        # query = ExtractoVehiculo.objects.filter(EmpresaPeriodoVehID__icontains=criterio).values()
        query = ExtractoVehiculo.objects.filter(
            VehiculoID=vehiculo, EmpresaID=empresa, Per_AA=periodo).values()
        return Response(query, status=status.HTTP_200_OK)

# Devuelve la lista de conceptos por tipo: Ingresos/Egresos


class ExtractoVehiculoConceptosView(APIView):
    def get(self, request, empresa, vehiculo, periodo, mes, typeconcept):
        # empresa-periodo-mes-pkVehiculo
        mes_formato = mes if mes > 9 else f"0{mes}"
        criterio = f"{empresa}{periodo}{mes_formato}{vehiculo}"
        query = ExtractoVehiculo.objects.filter(EmpresaPeriodoVehID=criterio, Nivel0=typeconcept).values(
            ('NivelID'),
            ('Nvl_Name')
        ).distinct()
        return Response(query, status=status.HTTP_200_OK)

# Devuelve la lista de subconceptos por concepto y por tipo: Ingresos/Egresos


class ExtractoVehiculoSubConceptosView(APIView):
    def get(self, request, empresa, vehiculo, periodo, mes, typeconcept, idconcept):
        # empresa-pkVehiculo-periodo-mes
        mes_formato = mes if mes > 9 else f"0{mes}"
        criterio = f"{empresa}{vehiculo}{periodo}{mes_formato}"
        query = ExtractoVehiculo.objects.filter(EmpresaPeriodoVehID=criterio, Nivel0=typeconcept, NivelID=idconcept).values(
            ('ConceptoID'),
            ('Cto_Des')
        ).distinct()
        return Response(query, status=status.HTTP_200_OK)


class ExtractoVehiculoPeriodoReportView(APIView):
    def get(self, request, documento, vehiculo, periodo, empresa):
        query = AfiliadoVehiculo.objects.filter(Q(AfiliadoID1=documento) | Q(AfiliadoID2=documento), VehiculoID=vehiculo, Per_AA=periodo, EmpresaID=empresa).values(
            'EmpresaPeriodoVeh',
            'Per_AA',
            'Per_MM',
            'NumVehiculo',
            'EmpresaID',
            'TIngresos',
            'TEgresos'
        ).order_by('Per_MM')

        results = [
            {
                'RegistroID': item['EmpresaPeriodoVeh'],
                'NumVehiculo': item['NumVehiculo'],
                'Per_MM': item['Per_MM'],
                'Periodo': getMothStr(item['Per_MM'], item['Per_AA']),
                'TIngresos': item['TIngresos'],
                'TEgresos': item['TEgresos'],
                'Certificado': getNameFileCertificado(documento, item['EmpresaID'], item['Per_MM'], item['Per_AA']),
                'Extracto': getNameFile(item['EmpresaID'], item['NumVehiculo'], item['Per_MM'], item['Per_AA']),
                'Planilla': getNameFilePlanilla(item['EmpresaID'], item['NumVehiculo'], item['Per_MM'], item['Per_AA'])
            }
            for item in query
        ]
        return Response(results, status=status.HTTP_200_OK)


class ExtractoVehiculoMesReportView(APIView):
    def get(self, request, documento, vehiculo, periodo, mes, empresa):
        query = AfiliadoVehiculo.objects.filter(Q(AfiliadoID1=documento) | Q(AfiliadoID2=documento), VehiculoID=vehiculo, Per_AA=periodo, Per_MM=mes, EmpresaID=empresa).values(
            'EmpresaPeriodoVeh',
            'Per_AA',
            'Per_MM',
            'NumVehiculo',
            'EmpresaID',
            'TIngresos',
            'TEgresos'
        )

        results = [
            {
                'RegistroID': item['EmpresaPeriodoVeh'],
                'NumVehiculo': item['NumVehiculo'],
                'Per_MM': item['Per_MM'],
                'Periodo': getMothStr(item['Per_MM'], item['Per_AA']),
                'TIngresos': item['TIngresos'],
                'TEgresos': item['TEgresos'],
                'Certificado': getNameFileCertificado(documento, item['EmpresaID'], item['Per_MM'], item['Per_AA']),
                'Extracto': getNameFile(item['EmpresaID'], item['NumVehiculo'], item['Per_MM'], item['Per_AA']),
                'Planilla': getNameFilePlanilla(item['EmpresaID'], item['NumVehiculo'], item['Per_MM'], item['Per_AA'])
            }
            for item in query
        ]

        return Response(results, status=status.HTTP_200_OK)


class DownloadFileView(APIView):
    def get(self, request, name_file):
        # Pasa la cédula y el nameFile
        # Descomponer el nameFile
        # http://gestor.berlinasdelfonce.com:9000/api/descargar/BER_EXTRACTO_VEHICULO_9025_ENE_2023.PDF/
        # http://127.0.0.1:9000/api/descargar/BER_PLANILLAS_VEHICULO_9025_ENE_2023.PDF/
        # Consultar si la consulta es !empty
        # if descarga el archivo
        # else devuelve un error
        # arreglo = name_file.split("_")

        # print(arreglo)
        # vehiculo = arreglo[3]
        # print(vehiculo)
        # afiliado = request.session.get('documento', None)
        # print(afiliado)

        # AfiliadoVehiculosObject = AfiliadoVehiculo.objects.filter(AfiliadoID1=afiliado, NumVehiculo=vehiculo).first()
        # print(AfiliadoVehiculosObject)

        url_fuente_externa = "http://gestor.berlinasdelfonce.com/pdf_extractos/" + name_file

        try:
            # if AfiliadoVehiculosObject != None:
            response = requests.get(url_fuente_externa)
            response.raise_for_status()  # Verificar si la solicitud fue exitosa

            contenido = response.content

            response = HttpResponse(
                contenido, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{name_file}"'

            return response
            # else:
            raise Http404(
                "No se pudo descargar el archivo de la fuente externa.")
        except requests.exceptions.RequestException as e:
            print("Error al realizar la solicitud a la fuente externa:", str(e))
            raise Http404(
                "No se pudo descargar el archivo de la fuente externa.")


class DestinatariosPQRView(APIView):
    def get(self, request):
        query = DestinatarioPQR.objects.order_by('Nombre').values()
        return Response(query, status=status.HTTP_200_OK)
