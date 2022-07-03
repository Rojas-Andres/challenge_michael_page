# Michael Page - Prueba Backend

Versión Python: `^3.5`

Versión django: `3.1.7`

#### Configuración del proyecto (Linux/Windows)

git clone https://github.com/Rojas-Andres/challenge_michael_page
cd rebus

### Cree virtulenv
    primero instale virtualenv
        pip install virtualenv
    
    crear virtualenv
        virtualenv entorno
    Activar entorno virtual en powershell
        .\entorno\Scripts\activate.ps1 
    Activar entorno virtual en terminal de windows
        .\entorno\Scripts\activate.bat 


### Instale requerimientos


pip3 install -r requeriments.txt

pip install -r requeriments.txt


### Ejecute migraciones:


python manage.py makemigrations

python manage.py migrate


## Correr server

python3 manage.py runserver

python manage.py runserver


### Test

python3 manage.py test

python manage.py test