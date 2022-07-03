from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fifa.utils import validate_country
from fifa.models import Country, Team, Player
from fifa.serializers import CountrySerializer, PlayerSerializer
from fifa.functions import Queries
from django.db import connection, transaction, IntegrityError


@api_view(["GET"])
def get_count_teams(request):
    """
    Esta api se encarga de devolver cuantos equipos estan registrados
    """
    count_teams = Team.own_manager.count_teams()
    return Response({"respuesta": count_teams}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_count_players(request):
    """
    Esta api se encarga de devolver cuantos equipos estan registrados
    """
    count_player = Player.own_manager.count_players()
    return Response({"respuesta": count_player}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_young_player(request):
    """
    Esta api se encarga de devolver el jugador mas joven
    """
    young_player = Player.own_manager.get_young_player()
    if young_player:
        serializer_context = {
            "request": request,
        }
        serializer = PlayerSerializer(
            young_player[0], many=False, context=serializer_context
        )
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"respuesta": "No hay jugadores registrados en la base de datos"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_old_player(request):
    """
    Esta api se encarga de devolver el jugador mas viejo
    """
    old_player = Player.own_manager.get_old_player()
    if old_player:
        serializer_context = {
            "request": request,
        }
        serializer = PlayerSerializer(
            old_player[0], many=False, context=serializer_context
        )
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {"respuesta": "No hay jugadores registrados en la base de datos"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_count_alternate_player(request):
    """
    Esta api se encarga de devolver cuantos jugadores suplentes hay
    """
    alternate_players = Player.own_manager.count_all_alternate_player()
    return Response({"respuesta": alternate_players}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_avg_alternate_player_by_team(request):
    """
    Esta api se encarga de devolver el promedio de jugadores suplentes por equipo
    """
    query = Queries.get_avg_alternate_player()
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    data = [{"equipo": i[0], "promedio": i[1]} for i in data]
    return Response(data, status=status.HTTP_200_OK)
