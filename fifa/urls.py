from django.urls import path, include
from rest_framework import routers
from django.urls import path

# from . import views
from fifa.views import team, country, player, coaching_staff

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(r"team", team.TeamViewSet)
router.register(r"player", player.PlayerViewSet)
router.register(r"coaching", coaching_staff.CoachingStaffViewSet)
# router.register(r"accounts", AccountViewSet)
urlpatterns = [
    path("create_country", country.create_country, name="CrearPais"),
    path("get_all_country", country.get_all_country, name="GetAllCountry"),
]
# urlpatterns = [
#     path("", include(router.urls)),
# ]
urlpatterns += router.urls
