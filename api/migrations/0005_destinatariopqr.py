# Generated by Django 4.2.5 on 2023-11-24 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_pqr'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinatarioPQR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=150, null=True)),
                ('Correo', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'DestinatarioPQR',
                'managed': True,
            },
        ),
    ]
