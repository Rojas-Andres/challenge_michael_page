from django.urls import path, include
from rest_framework import routers
from django.urls import path

# from . import views
from fifa.views import team, country, player

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(
    r"team", team.TeamViewSet
)  # https://www.django-rest-framework.org/api-guide/routers/
router.register(r"player", player.PlayerViewSet)
# router.register(r"accounts", AccountViewSet)
urlpatterns = [path("create_country", country.create_country, name="CrearPais")]
# urlpatterns = [
#     path("", include(router.urls)),
# ]
urlpatterns += router.urls
