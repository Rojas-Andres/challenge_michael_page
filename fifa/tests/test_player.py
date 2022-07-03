from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from fifa.models import Country, Team, Player
import mock
from django.core.files import File

client = APIClient()
image_mock = mock.MagicMock(spec=File)
image_mock.name = "Flag_of_Colombia.svg_6RQAHOe.png"
# @pytest.mark.django_db
# def test_create_database(client):
#     print("cliente", client)
#     url = "api-create_country"
#     url = reverse("api-create_country")
#     response = client.post(url, data={"country": "venezuela"})
#     print("response ->", response)
#     assert True == True


# @pytest.mark.skip
# def test_player():
#     print("entre mor\n\n\n\n\n\n\n")
#     assert True == True
class TestAll(TestCase):
    """Test module for GET all puppies API"""

    def setUp(self):
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
            "birth_date": "2020-04-12",
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
            == "Ya se encuentra un equipo creado con ese pais"
        )

    def test_change_update_shirt_player(self):
        data = {"shirt_number": 1}
        headers = {"Content-Type": "application/json", "Accept-Encoding": None}

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
