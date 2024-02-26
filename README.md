# Portal de propietarios

Este proyecto contiene el Backend del portal de propietarios, el cual será consumido por un Frontend en VueJS 3, permite la consulta de información de extractos de propietarios de las empresas Compañía Libertador SA y Berlinas del Fonce SA.

## Caracteristicas

- Python 3 (Lenguaje base)
- Django (Backend Framework - https://www.django-rest-framework.org/)
- PostgreSQL v14 (Gestor de bases de datos)
- Yagmail (API de envío de Emails)
- Altiria SMS (API de evío de mensajes de texto)

## Requirimientos
- pip o pip3
- Python
- Django
- Apache2.
- PostgreSQL

## Versionado 
```
La estructura del versionado consta de 3 numero separados por punto (.):

Primer número: Versión principal, es la versión que indica las caracteristicas 
generales de la plataforma: Infraestructura, tecnología, caracteristicas principales.

Segundo número: Versión secundaria, es la versión que indica las nuevas funcionalidades
agregadas al aplicativo.

Tercer número: Versión Parche/Commit, es la versión que indica un nuevo cambio realizado 
en el código para efectos de corrección de problemas, ajustes pequeños, ajustes de forma, etc.
```
- 1.0.22 (Versión actual)
```
Las versiones especificas se encuentran establecidas en los Commit realizados.
```

## Instalación (Actualice servidor)
```
sudo apt update
sudo apt upgrade
```

### Clona el repositorio
```
git config --global user.name "Su nombre"
git config --global user.email "sucorreo@sudominio.com"
git clone https://github.com/solincosta/backendportal.git
```

### Crear entorno virtual
```
virtualenv venv
source venv/bin/activate
```
### Instalar Python
```
python.exe -m pip install --upgrade pip
```
### Instalar Django
```
pip install Django
```
### Instalar Dependencias
```
pip3 install psycopg2-binary  (ORM PostgreSQL)
python3 -m pip install django-cors-headers (Cors Headers)
pip3 install djangorestframework  (Django RestFamework - API Rest)
pip3 install django-send-email   (Send Email)
pip3 install yagmail (Yagmail correos electrónicos)
pip install sms-python-client  ((API de mensajería SMS)
```

### Crear el archivo settings.py en backendportal/
```
solicite las configuraciones y accesos al desarrollador principal del proyecto
```

### Crear y configurar la Base de datos
```
postgres=# CREATE DATABASE myproject;
postgres=# CREATE USER myprojectuser WITH PASSWORD 'password';
postgres=# ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
postgres=# ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE myprojectuser SET timezone TO 'America/Bogota';
postgres=# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
postgres=# \q
```
### Ejecute las migraciones
```
python3 manage.py makemigrations
python3 manage.py migrate
```
### Corra el servidor
```
python3 manage.py runserver 0.0.0.0:9000
```
### Cargar cambios - otro desarrollador (Trabaje en otra rama)
```
La primera recomendación es trabajar en otra rama y subir los cambios desde una rama diferente a la main

git checkout -b [otra-rama]

git add .
git commit -m "Mensaje del commit"
git push origin [otra-rama]
```

### Actualizar cambios en el Servidor
```
Buscar la ruta raiz del proyecto en el servidor:

cd backendportal

Luego ejecutar un pull para bajar los cambios del repositorio al servidor:

git pull origin main

Introducir la clave del usuario autorizado en el repositorio compartido:

xXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxX
git checkout -b [otra-rama]

```
# backendportal2
