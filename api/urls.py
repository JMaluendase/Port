from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('afiliadosvehiculos/consultaxafiliado/<int:documento>/',
         views.AfiliadoVehiculoPorAfiliadoView.as_view()),  # TESTED
    path('afiliadosvehiculos/actualizarafiliado/',
         views.UpdateAfiliadoView.as_view(), name='update-afiliado'),
    path('afiliadosvehiculos/consultaempresa/<int:documento>/<str:vehiculo>/',
         views.ExtractoVehiculoGetCompanyView.as_view()),  # TESTED
    path('afiliadosvehiculos/consultaperiodo/<int:documento>/<str:vehiculo>/<int:empresa>/',
         views.ExtractoVehiculoGetAniosView.as_view()),  # TESTED
    path('afiliadosvehiculos/consultames/<int:documento>/<str:vehiculo>/<int:periodo>/',
         views.ExtractoVehiculoGesMesView.as_view()),  # TESTED
    path('afiliadosvehiculos/consultaconceptos/<int:empresa>/<str:vehiculo>/<int:periodo>/<int:mes>/<int:typeconcept>/',
         views.ExtractoVehiculoConceptosView.as_view()),  # TESTED
    path('afiliadosvehiculos/consultasubconceptos/<int:empresa>/<str:vehiculo>/<int:periodo>/<int:mes>/<int:typeconcept>/<int:idconcept>/',
         views.ExtractoVehiculoSubConceptosView.as_view()),  # TESTED

    # Data Source
    path('afiliadosvehiculos/consultaextracto/<int:empresa>/<str:vehiculo>/<int:periodo>/<int:mes>/',
         views.ExtractoVehiculoMesView.as_view()),  # TESTED
    path('afiliadosvehiculos/consultaextracto/<int:empresa>/<str:vehiculo>/<int:periodo>/',
         views.ExtractoVehiculoAnioView.as_view()),  # TESTED

    # Data Extract
    path('afiliadosvehiculos/consultaextractoreport/<int:documento>/<str:vehiculo>/<int:periodo>/<int:empresa>/',
         views.ExtractoVehiculoPeriodoReportView.as_view()),  # TESTED
    path('afiliadosvehiculos/consultaextractoreport/<int:documento>/<str:vehiculo>/<int:periodo>/<int:mes>/<int:empresa>/',
         views.ExtractoVehiculoMesReportView.as_view()),  # TESTED

    # Data Token
    path('afiliados/<int:documento>/', views.AfiliadoViewSet.as_view()),  # TESTED
    path('token/', views.NuevoTokenView.as_view(), name='nuevo-token'),
    path('token/<str:tokenid>/<int:documento>/',
         views.getToken.as_view()),  # TESTED
    path('token2/<str:tokenid>/<int:documento>/',
         views.getToken2.as_view()),  # TESTED

    # PQR
    path('newpqr/', views.NewPQRView.as_view(), name='nueva-pqr'),

    # Get Data
    path('afiliados/getdatos/<int:documento>/',
         views.AfiliadoDataViewSet.as_view()),  # TESTED

    path('descargar/<str:name_file>/',
         views.DownloadFileView.as_view(), name='descargar_archivo'),

    # Get Data
    path('destinatarios/getall/', views.DestinatariosPQRView.as_view()),  # TESTED

    # Testing Funtions
    path('test/<int:param>/', views.FunctionsView.as_view()),  # TESTED
]
