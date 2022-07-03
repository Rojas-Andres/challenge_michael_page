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
        response = client.get("/api/get_all_country")
        assert len(response.json()) == 32

    def test_create_country(self):
        response = client.post(reverse("CrearPais"), data={"country": "COLOMBIA"})
        assert (
            response.json()["respuesta"]
            == "El pais COLOMBIA ya existe en la base de datos."
        )

    def test_create_team(self):
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

    def test_change_update_shirt_player(self):
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

    def test_not_found_player(self):
        """
        no encuentra jugador
        """
        data = {"titular": True}
        response = client.patch("/api/player/13/", data=data)
        assert response.json()["respuesta"] == "No se encuentra el equipo con el id 13"

    def test_create_player_required(self):
        data = {
            "player_photo": image_mock,
            "name": "Andres",
        }
        response = client.post("/api/player/", data=data)
        assert response.json()["'last_name'"] == "Este campo es requerido"

    def test_create_player(self):
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
            == "Ya tiene 11 jugadores titulares no puede colocar otro mas como titular"
        )
        data["titular"] = False
        response = client.post("/api/player/", data=data)
        assert response.json()["respuesta"] == "Jugador creado correctamente!"
