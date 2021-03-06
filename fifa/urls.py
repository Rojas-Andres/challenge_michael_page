from django.urls import path, include
from rest_framework import routers
from django.urls import path

from fifa.views import team, country, player, coaching_staff, fifa_endpoints


router = routers.DefaultRouter()
router.register(r"team", team.TeamViewSet)
router.register(r"player", player.PlayerViewSet)
router.register(r"coaching", coaching_staff.CoachingStaffViewSet)
urlpatterns = [
    path("create_country", country.create_country, name="CrearPais"),
    path("get_all_country", country.get_all_country, name="ObtenerTodosPaises"),
    path("count_teams", fifa_endpoints.get_count_teams, name="CantidadEquipos"),
    path("count_players", fifa_endpoints.get_count_players, name="CantidadEquipos"),
    path("get_young_player", fifa_endpoints.get_young_player, name="JugadorMasJoven"),
    path("get_old_player", fifa_endpoints.get_old_player, name="JugadorMasViejo"),
    path(
        "count_alternate_player",
        fifa_endpoints.get_count_alternate_player,
        name="CantidadJugadoresSuplentes",
    ),
    path(
        "get_avg_player_team",
        fifa_endpoints.get_avg_alternate_player_by_team,
        name="PromedioEquipoJugadorSuplente",
    ),
    path(
        "get_max_team_player",
        fifa_endpoints.get_max_team_player,
        name="ObtenerMaximoJugadoresEquipo",
    ),
    path(
        "get_avg_age_players",
        fifa_endpoints.get_avg_players,
        name="PromedioEdadJugadores",
    ),
    path(
        "get_avg_players_by_team",
        fifa_endpoints.get_avg_players_by_team,
        name="PromedioJugadoresEquipo",
    ),
    path(
        "get_old_coaching",
        fifa_endpoints.get_old_coaching,
        name="TecnicoMasViejo",
    ),
]
urlpatterns += router.urls
