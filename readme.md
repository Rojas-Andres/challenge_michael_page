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

# Validaciones 

## Team

	Creacion del equipo(Metodo POST):
		Se valida que solo exista un equipo por pais.

		Se valida que el nombre del equipo no se repita.

		Se valida que el pais exista en la base de datos.

        Se valida que no se puedan crear mas de 32 equipos ya que solo son 32 equipos que van al mundial.

	Actualizacion equipo(Metodo PATCH):

		Se valida que el pais exista para la actualizacion del equipo

		Se valida que al actualizar el equipo solo exista un pais por equipo.

		Se valida que solo exista un nombre por equipo.
## Player
	
	Creacion del jugador(Metodo POST):
    	
        Se valida el formato de fecha (YYYY-MM-DD).
        
		Se valida que el equipo con el que se registra el jugador ya este creado en la base de datos.
        
		Se valida que no hayan 11 jugadores titulares por equipo.

		Se valida que no se repita una mismo numero de camiseta por equipo.

        Se valida que la posicion exista (posiciones [Arquero,Defensa,Centrocampista,Delantero])

        Se valida que un equipo no pueda registrar mas de 23 jugadores 
        
	Actualizacion del jugador metodo (PATCH permite actualizar solo los campos que se le envian):

		Se valida el formato de fecha (YYYY-MM-DD).

		Se valida que al actualizar el equipo del jugador ya se encuentre en la base de datos.

		Se valida que al actualizar el jugador (titular)este no vaya a superar los 11 titulares por reglamento .

		Se valida que al actualizar no se repita una mismo numero de camiseta por equipo.

        Se valida que la posicion exista (posiciones [Arquero,Defensa,Centrocampista,Delantero])

# Coaching

    Creacion del cuerpo tecnico(METODO POST):

        Se valida el formato de fecha (YYYY-MM-DD).

		Se valida que el equipo con el que se registra el cuerpo tecnico ya este creado en la base de datos.

		Se valida que la nacionalidad con la que se crea el cuerpo tecnico exista en la base de datos.

		Se valida que la rol exista (roles [Tecnico,Asistente,Medico,Preparador])

    Actualizacion del cuerpo tecnico:
        Se valida el formato de fecha (YYYY-MM-DD).

        Se valida que el equipo con el que se registra el cuerpo tecnico ya este creado en la base de datos.

        Se valida que la nacionalidad con la que se va actualizar exista en la base de datos.

        Se valida que la rol exista (roles [Tecnico,Asistente,Medico,Preparador]).