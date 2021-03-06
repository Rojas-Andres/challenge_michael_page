from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from fifa.models import Country, Team, Player
import mock
from django.core.files import File
import json
import os

client = APIClient()
image_mock = mock.MagicMock(spec=File)
image_mock.name = "Flag_of_Colombia.svg_6RQAHOe.png"


class TestAll(TestCase):
    """Test module for GET all puppies API"""

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        Country.own_manager.create_country("COLOMBIA")
        data = {
            "name_team": "Colombia",
            "flag_photo": image_mock,
            "shield_photo": image_mock,
            "country": "COLOMBIA",
        }
        Team.own_manager.create_team(data, 1)

        number_shirt = 1
        titular = True
        data = {
            "player_photo": image_mock,
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "2000-04-12",
            "team_id": 1,
            "shirt_number": number_shirt,
            "titular": True,
            "position": "Delantero",
        }
        # Creamos los 11 jugadores titulares
        for i in range(11):

            data["shirt_number"] = number_shirt
            Player.own_manager.create_player(data)
            number_shirt += 1

        # Crear pais and equipo
        with open(f"{dir_path}/files/country.json") as json_data_file:
            data = json.load(json_data_file)
            indice = 2
            for i in data:
                Country.own_manager.create_country(i.upper())
                country = Country.own_manager.filter_country_by_name(i.upper()).get().id
                dic = {
                    "name_team": i.capitalize(),
                    "flag_photo": image_mock,
                    "shield_photo": image_mock,
                    "country": i.upper(),
                }
                Team.own_manager.create_team(dic, country)

    def test_get_all_country(self):
        """
        Test obtener todos los paises
        """
        response = client.get("/api/get_all_country")
        assert len(response.json()) == 32

    def test_create_country(self):
        """
        Test creando pais , no puede crear un pais con el mismo nombre
        """
        response = client.post(reverse("CrearPais"), data={"country": "COLOMBIA"})
        assert (
            response.json()["respuesta"]
            == "El pais COLOMBIA ya existe en la base de datos."
        )

    def test_create_team(self):
        """
        Test 32 equipos creados no permite crear otro
        """
        data = {
            "name_team": "Colombia",
            "flag_photo": image_mock,
            "shield_photo": image_mock,
            "country": "COLOMBIA",
        }
        response = client.post("/api/team/", data=data)
        assert (
            response.json()["respuesta"]
            == "No puede crear mas equipos, la fifa solo permite 32"
        )

    def test_change_patch_shirt_player(self):
        """
        Test la camiseta de un jugador no se puede repetir para un equipo
        """
        data = {"shirt_number": 1}
        response = client.patch("/api/player/9/", data=data)
        assert (
            response.json()["respuesta"]
            == "No puede registrar a otro jugador con la misma camiseta en ese equipo"
        )

    def test_get_all_players(self):
        """
        Obtenemos todos los jugadores
        """
        response = client.get("/api/player/")
        assert len(response.json()) == 11

    def test_patch_not_found_player(self):
        """
        no encuentra jugador
        """
        data = {"titular": True}
        response = client.patch("/api/player/13/", data=data)
        assert response.json()["respuesta"] == "No se encuentra el equipo con el id 13"

    def test_create_player_required(self):
        """ "
        Test el campo last_name es requerido
        """
        data = {
            "player_photo": image_mock,
            "name": "Andres",
        }
        response = client.post("/api/player/", data=data)
        assert response.json()["'last_name'"] == "Este campo es requerido"

    def test_create_player_age(self):
        """
        Test el jugador no puede tener menos de 15 a??os
        """
        data = {
            "player_photo": image_mock,
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "2020-04-12",
            "team_id": 1,
            "shirt_number": 13,
            "titular": True,
            "position": "Delantero",
        }
        response = client.post("/api/player/", data=data)
        assert (
            response.json()["respuesta"]
            == "El jugador que desea inscribir no puede tener menos de 15 a??os"
        )

    def test_create_player_titular(self):
        """
        Test no puede colocar mas de 11 jugadores como titulares
        """
        data = {
            "player_photo": image_mock,
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "2005-04-12",
            "team_id": 1,
            "shirt_number": 13,
            "titular": True,
            "position": "Delantero",
        }
        response = client.post("/api/player/", data=data)
        assert (
            response.json()["respuesta"]
            == "Ya tiene 11 jugadores titulares no puede colocar otro mas como titular"
        )

    def test_create_player_not_found_team(self):
        """
        Test id del equipo no encontrado
        """
        data = {
            "player_photo": image_mock,
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "2005-04-12",
            "team_id": 1111,
            "shirt_number": 13,
            "titular": False,
            "position": "Delantero",
        }
        response = client.post("/api/player/", data=data)
        assert (
            response.json()["respuesta"]
            == "No existe el equipo con el id 1111 en la bd!"
        )

    def test_create_player_bad_birth_date(self):
        """
        Test envia fecha de nacimiento erronea
        """
        data = {
            "player_photo": image_mock,
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "2000-04-112312",
            "team_id": 1,
            "shirt_number": 13,
            "titular": False,
            "position": "Delantero",
        }
        response = client.post("/api/player/", data=data)
        assert (
            response.json()["respuesta"]
            == "Recuerde el formato fecha YYYY-MM-DD (A??O-MES-DIA)"
        )

    def test_create_player_not_found_position(self):
        """
        Test no encuentra la posicion al crear el jugador
        """
        data = {
            "player_photo": image_mock,
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "2000-04-12",
            "team_id": 1,
            "shirt_number": 13,
            "titular": False,
            "position": "CentrocampistaDelantero",
        }
        response = client.post("/api/player/", data=data)
        assert (
            response.json()["respuesta"]
            == "No existe la posicion CentrocampistaDelantero recuerde que solo estan estas ['Arquero', 'Defensa', 'Centrocampista', 'Delantero']"
        )

    def test_delete_player(self):
        """
        Test eliminar jugador
        """
        response = client.delete("/api/player/1/")
        assert response.json()["respuesta"] == "Jugador eliminado correctamente"

    def test_get_all_player(self):
        """
        Test obtener todos los jugadores
        """
        response = client.get("/api/player/")
        assert len(response.json()) == 11

    def test_get_one_player(self):
        """
        Test obtener un jugador
        """
        response = client.get("/api/player/?id=1")
        assert response.json()["titular"] == True

    def test_patch_player_bad_birth_date(self):
        """
        Test actualizar un jugador con fecha de nacimiento erronea
        """

        data = {"birth_date": "2000-04-121"}
        response = client.patch("/api/player/9/", data=data)
        assert (
            response.json()["respuesta"]
            == "Recuerde el formato fecha YYYY-MM-DD (A??O-MES-DIA)"
        )

    def test_patch_player_not_found_team(self):
        """
        Test actualizar un jugador con el team_id que no existe
        """
        data = {"team_id": 12312312}
        response = client.patch("/api/player/9/", data=data)
        assert (
            response.json()["respuesta"]
            == "No existe el equipo con el id 12312312 en la bd!"
        )

    def test_patch_player_not_permission_age(self):
        """
        Test actualizar un jugador con la edad menor a 15 a??os
        """
        data = {"birth_date": "2015-04-12"}
        response = client.patch("/api/player/9/", data=data)
        assert (
            response.json()["respuesta"]
            == "El jugador que desea inscribir no puede tener menos de 15 a??os"
        )

    def test_patch_player_position_not_found(self):
        """
        Test actualizar un jugador con la edad menor a 15 a??os
        """
        data = {"position": "holas"}
        response = client.patch("/api/player/9/", data=data)
        assert (
            response.json()["respuesta"]
            == "No existe la posicion holas recuerde que solo estan estas ['Arquero', 'Defensa', 'Centrocampista', 'Delantero']"
        )

    def test_create_coach(self):
        """
        Tesct crear coach
        """
        data = {
            "name": "Andres",
            "last_name": "Rojas",
            "birth_date": "1999-03-12",
            "nacionality_id": 1,
            "rol": "Tecnico",
            "team_id": 1,
        }
        response = client.post("/api/coaching/", data=data)
        assert response.json()["respuesta"] == "Cuerpo tecnico creado correctamente!"
