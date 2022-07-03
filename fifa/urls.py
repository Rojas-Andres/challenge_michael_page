from django.urls import path, include
from rest_framework import routers
from django.urls import path

# from . import views
from fifa.views import team, country, player, coaching_staff, fifa_endpoints

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(r"team", team.TeamViewSet)
router.register(r"player", player.PlayerViewSet)
router.register(r"coaching", coaching_staff.CoachingStaffViewSet)
# router.register(r"accounts", AccountViewSet)
urlpatterns = [
    path("create_country", country.create_country, name="CrearPais"),
    path("get_all_country", country.get_all_country, name="ObtenerTodosPaises"),
    path("count_teams", fifa_endpoints.get_count_teams, name="CantidadEquipos"),
    path("count_players", fifa_endpoints.get_count_players, name="CantidadEquipos"),
    path("get_young_player", fifa_endpoints.get_young_player, name="JugadorMasJoven"),
]
# urlpatterns = [
#     path("", include(router.urls)),
# ]
urlpatterns += router.urls
