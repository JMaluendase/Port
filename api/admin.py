from django.contrib import admin
from .models import AfiliadoVehiculo, Afiliado, Token, ExtractoVehiculo, DestinatarioPQR, PQR 
# Register your models here.

admin.site.register(AfiliadoVehiculo)
admin.site.register(Afiliado)
admin.site.register(Token)
admin.site.register(ExtractoVehiculo)
admin.site.register(DestinatarioPQR)
admin.site.register(PQR)
