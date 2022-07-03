from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fifa.utils import validate_country
from fifa.models import Country, Team, Player
from fifa.serializers import CountrySerializer, PlayerSerializer


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
    Esta api se encarga de devolver cuantos equipos estan registrados
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
