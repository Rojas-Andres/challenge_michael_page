from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fifa.utils import validate_country
from fifa.models import Country, Team, Player
from fifa.serializers import CountrySerializer


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
