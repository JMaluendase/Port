from django.db import models
import json


class Afiliado(models.Model):
    AfiliadoID = models.CharField(primary_key=True, max_length=20)
    Nombre = models.CharField(max_length=100, null=True)
    Correo = models.CharField(max_length=45, null=True)
    Correo2 = models.CharField(max_length=45, null=True)
    Telefono = models.CharField(max_length=15, null=True)

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'Afiliado'


class AfiliadoVehiculo(models.Model):
    EmpresaPeriodoVeh = models.CharField(max_length=20, primary_key=True)
    EmpresaID = models.IntegerField(null=True)  # Integer 4
    AfiliadoID1 = models.ForeignKey(Afiliado, on_delete=models.CASCADE,
                                    default=1, db_column='AfiliadoID1', related_name='afiliado1_set')
    AfiliadoID2 = models.ForeignKey(Afiliado, on_delete=models.CASCADE,
                                    default=1, db_column='AfiliadoID2', related_name='afiliado2_set')
    Per_AA = models.IntegerField(null=True)  # Integer 4
    Per_MM = models.IntegerField(null=True)  # Integer 2
    VehiculoID = models.CharField(max_length=10, null=True)  # ChardField 10
    NumVehiculo = models.IntegerField(null=True)  # Integer 6
    Placa = models.CharField(max_length=6, null=True)  # ChardField 6
    NumFirmas = models.IntegerField(null=True)
    TIngresos = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    TEgresos = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    Veh_Area = models.CharField(max_length=1, null=True)
    # Extracto = models.CharField(max_length=45, null=True)

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'AfiliadoVehiculos'


class ExtractoVehiculo(models.Model):
    Id = models.AutoField(primary_key=True)
    EmpresaID = models.IntegerField(null=True)
    Per_AA = models.IntegerField(null=True)
    Per_MM = models.IntegerField(null=True)
    VehiculoID = models.CharField(max_length=10, null=True)  # ChardField 10
    NumVehiculo = models.IntegerField(null=True)  # Integer 6
    Placa = models.CharField(max_length=6, null=True)  # ChardField 6
    Nivel0 = models.IntegerField(null=True)
    NivelID = models.IntegerField(null=True)
    Nvl_Name = models.CharField(max_length=45, null=True)
    ConceptoID = models.CharField(max_length=10, null=True)
    Cto_Des = models.CharField(max_length=75, null=True)
    ValorBase = models.DecimalField(max_digits=12, decimal_places=2)
    PorBase = models.DecimalField(max_digits=10, decimal_places=2)
    porCal = models.DecimalField(max_digits=10, decimal_places=2)
    ValorIng = models.DecimalField(max_digits=10, decimal_places=2)
    ValorEgr = models.DecimalField(max_digits=10, decimal_places=2)
    Ref1 = models.IntegerField(null=True)
    Ref2 = models.IntegerField(null=True)
    Ref3 = models.IntegerField(null=True)
    EmpresaPeriodoVehID = models.ForeignKey(
        AfiliadoVehiculo, on_delete=models.CASCADE, default=1, db_column='EmpresaPeriodoVehID')

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'ExtractoVehiculo'


class Token(models.Model):
    Numero = models.CharField(max_length=6, null=True)
    Fecha = models.DateField(null=True)
    Hora = models.DateTimeField(null=True)
    Vencido = models.BooleanField(default=True)
    Llave = models.CharField(max_length=45, null=True)

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'Token'


class Token2(models.Model):
    Numero = models.CharField(max_length=6, null=True)
    Fecha = models.DateField(null=True)
    Hora = models.DateTimeField(null=True)
    Vencido = models.BooleanField(default=True)
    IdAfiliado = models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    Llave = models.CharField(max_length=45, null=True)

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'Token2'


class DestinatarioPQR(models.Model):
    Nombre = models.CharField(max_length=150, null=True)
    Correo = models.CharField(max_length=45, null=True)

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'DestinatarioPQR'


class PQR(models.Model):
    Radicado = models.CharField(max_length=16, null=True)
    Fecha = models.DateField(null=True)
    Hora = models.DateTimeField(null=True)
    Estado = models.BooleanField(default=True)
    Detalle = models.CharField(max_length=355, null=True)
    AfiliadoPQRID = models.ForeignKey(
        Afiliado, on_delete=models.CASCADE, default=1, db_column='AfiliadoPQRID')
    # DestinatarioPQRID = models.ForeignKey(DestinatarioPQR, on_delete=models.CASCADE, default=1, db_column='DestinatarioPQRID')
    DestinatarioPQRID = models.ForeignKey(
        DestinatarioPQR, null=True, blank=True, on_delete=models.CASCADE, db_column='DestinatarioPQRID')

    class Meta:
        app_label = 'api'
        managed = True
        db_table = 'PQR'
