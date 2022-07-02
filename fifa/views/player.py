from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response

# from rest_framework.views import viewsets
from rest_framework import viewsets, status, generics

from rest_framework.decorators import api_view
from fifa.serializers import TeamSerializer
from fifa.models import Team
from rest_framework.decorators import action
from fifa.utils import (
    validate_country,
    validate_team,
    validate_team_by_id,
    to_bool,
    validate_player,
)
from fifa.models import Player


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.own_manager.all_teams()

    def list(self, request):
        id_player = request.GET.get("id")
        if id_player:
            get_country = Country.own_manager.filter_country_by_name(country.upper())
            if get_country:
                # Obtener el equipo referente a ese pais
                team = Team.own_manager.filter_team_by_country(
                    get_country.get().id
                ).get()
                serializer_context = {
                    "request": request,
                }
                serializer = TeamSerializer(
                    team, many=False, context=serializer_context
                )
                if serializer:
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"response": f"No existe el pais {country} en la base de datos"}
                )
        else:
            all_players = Player.own_manager.all_player()
            if not all_players:
                return Response({"respuesta": "No hay jugadores en la base de datos!"})
            return Response(all_teams)

    def create(self, request, *args, **kwargs):
        data = request.data
        res = {}
        try:
            #             return self.all().values(
            #     "player_photo",
            #     "name",
            #     "last_name",
            #     "birth_date",
            #     "team__name_team",
            #     "titular",
            #     "shirt_number",
            #     "position",
            # )
            if (
                data["player_photo"]
                and data["name"]
                and data["last_name"]
                and data["birth_date"]
                and data["team_id"]
                and data["titular"]
                and data["shirt_number"]
                and data["position"]
            ):
                player = validate_player(data)
                if "respuesta" in player:
                    return Response(player, status=status.HTTP_400_BAD_REQUEST)
                new_player = Player.own_manager.create_player(data)
                return Response("asdas")

        except KeyError as e:
            res[str(e)] = "Este campo es requerido"

        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        team = Team.own_manager.get_team_by_id(kwargs["pk"]).first()
        if team:
            data = request.data
            # Filtramos pais para saber si existe
            if "country" in data:
                country = Country.own_manager.filter_country_by_name(data["country"])
                if not country:
                    return Response(
                        {
                            "respuesta": f"No se encuentra el pais {data['country']} para actualizar "
                        }
                    )
                # Filtramos si ya hay algun equipo relacionado con ese pais , teniendo en cuenta que un solo equipo puede pertener a un pais
                get_team = Team.own_manager.filter_team_by_country(country.get().id)
                if get_team:

                    if (
                        get_team.get().id != team.id
                    ):  # Validamos que no haya ningun equipo creado
                        return Response(
                            {
                                "respuesta": f"Ya se encuentra un equipo relacionado con ese pais {data['country']}"
                            }
                        )
                else:
                    team.country_id = country.get().id
            team.name_team = data.get("name_team", team.name_team)
            team.flag_photo = data.get("flag_photo", team.flag_photo)
            team.shield_photo = data.get("shield_photo", team.shield_photo)

            team.save()

            serializer = TeamSerializer(team)
            return Response(serializer.data)

        return Response(
            {"respuesta": f"No se encuentra el equipo con el id {kwargs['pk']}"}
        )

    def destroy(self, request, *args, **kwargs):
        team = Team.own_manager.get_team_by_id(kwargs["pk"]).first()
        if team:
            team.delete()
            return Response({"respuesta": "Equipo eliminado correctamente"})
        return Response(
            {"respuesta": f"No se encuentra el equipo con el id {kwargs['pk']}"}
        )
