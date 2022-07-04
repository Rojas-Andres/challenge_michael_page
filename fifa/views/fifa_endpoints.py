from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fifa.utils import validate_country, calculate_avg_age
from fifa.models import Country, Team, Player, CoachingStaff
from fifa.serializers import (
    CountrySerializer,
    PlayerSerializer,
    CoachingStaffSerializer,
)
from fifa.functions import Queries
from django.db import connection, transaction, IntegrityError
from django.db.models import Max


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
    pl = Player.own_manager.get_avg_alternate_player_by_team()
    data = {}
    for i in pl:
        if i["team__name_team"] not in data:
            data[i["team__name_team"]] = {"titular": 0, "suplente": 0}
        if i["titular"] == True:
            data[i["team__name_team"]]["titular"] = i["dcount"]
        else:
            data[i["team__name_team"]]["suplente"] = i["dcount"]
    prom = {}
    for key, value in data.items():
        if value["suplente"] == 0:
            prom[key] = 0
            continue
        prom[key] = value["suplente"] / (value["suplente"] + value["titular"])
    return Response(prom, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_avg_players_by_team(request):
    """
    Esta api se encarga de devolver el promedio de numero de jugadores en cada equipo
    """
    query = Queries.get_avg_players_by_team()
    cursor = connection.cursor()
    cursor.execute(query)
    datos = cursor.fetchall()
    datos = [{"equipo": i[0], "promedio": i[1]} for i in datos]
    return Response(datos, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_max_team_player(request):
    """
    Esta api se encarga de devolver el equipo que tiene mas jugadores registrados
    """
    res = {"nombre_equipo": "", "maximo": -1}
    players_team = Player.own_manager.get_agg_team_player()
    if players_team:
        for i in players_team:
            if i["dcount"] > res["maximo"]:
                res["maximo"] = i["dcount"]
                res["nombre_equipo"] = i["team__name_team"]
        return Response(res, status=status.HTTP_200_OK)
    else:
        return Response(
            {"respuesta": "No hay jugadores registrados en la base de datos!"},
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
def get_avg_players(request):
    """
    Esta api se encarga de devolver la edad promedio de los jugadores
    """
    players_birth_date = Player.own_manager.get_birth_date_all()
    avg_ages = calculate_avg_age(players_birth_date)
    return Response({"respuesta": avg_ages}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_old_coaching(request):
    """
    Esta api se encarga de devolver el tecnico mas viejo
    """
    coach = CoachingStaff.own_manager.get_old_coach("TC")
    if coach:
        serializer_context = {
            "request": request,
        }
        serializer = CoachingStaffSerializer(
            coach[0], many=False, context=serializer_context
        )
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        return Response(
            {"respuesta": "No hay tecnicos registrados en la base de datos!"},
            status=status.HTTP_200_OK,
        )
