from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response

# from rest_framework.views import viewsets
from rest_framework import viewsets, status, generics

from rest_framework.decorators import api_view
from fifa.serializers import PlayerSerializer
from fifa.models import Team, Country, CoachingStaff
from rest_framework.decorators import action
from fifa.utils import (
    validate_country,
    validate_team,
    validate_team_by_id,
    to_bool,
    validate_player_create,
    validate_position_exist,
    convert_date,
    get_positions,
    validate_rol_exist,
    get_rol,
)
from fifa.models import Player
from django.http import HttpResponse


class CoachingStaffViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.own_manager.all_player()

    def list(self, request):
        id_player = request.GET.get("id")
        if id_player:
            pass
            # get_country = Country.own_manager.filter_country_by_name(country.upper())
            # if get_country:
            #     # Obtener el equipo referente a ese pais
            #     team = Team.own_manager.filter_team_by_country(
            #         get_country.get().id
            #     ).get()
            #     serializer_context = {
            #         "request": request,
            #     }
            #     serializer = TeamSerializer(
            #         team, many=False, context=serializer_context
            #     )
            #     if serializer:
            #         return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response(
            #         {"response": f"No existe el pais {country} en la base de datos"}
            #     )
        else:
            all_players = Player.own_manager.all_player()
            if not all_players:
                return Response({"respuesta": "No hay jugadores en la base de datos!"})
            return Response(all_players)

    def create(self, request, *args, **kwargs):
        data = request.data
        res = {}
        try:
            if (
                data["name"]
                and data["last_name"]
                and data["birth_date"]
                and data["nacionality_id"]
                and data["rol"]
                and data["team_id"]
            ):
                # Validar si el pais existe
                country = Country.own_manager.filter_country_by_id(
                    data["nacionality_id"]
                )
                if not country:
                    res[
                        "respuesta"
                    ] = f"El pais con el id {data['nacionality_id']} no existe en la base de datos"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                # Validate team_id

                team = Team.own_manager.get_team_by_id(data["team_id"])
                if not team:
                    res[
                        "respuesta"
                    ] = f"El equipo con el id {data['team_id']} no existe en la base de datos"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                # Validate birth date
                date = convert_date(data["birth_date"])
                if not date:
                    res[
                        "respuesta"
                    ] = "Recuerde el formato fecha YYYY-MM-DD (AÑO-MES-DIA)"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                rol = validate_rol_exist(data["rol"])
                if not rol:
                    res[
                        "respuesta"
                    ] = f"Recuerde que los roles permitidos son {get_rol()}"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                new_coach = CoachingStaff.own_manager.create_coach(
                    data, country.get().id, rol, team.get().id
                )
                new_coach.save()
                return Response({"respuesta": "Cuerpo tecnico creado correctamente!"})
        except KeyError as e:
            res[str(e)] = "Este campo es requerido"
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        player = Player.own_manager.get_player_by_id(kwargs["pk"]).first()
        res = {}
        if player:
            data = request.data

        return Response(
            {"respuesta": f"No se encuentra el equipo con el id {kwargs['pk']}"}
        )

    def destroy(self, request, *args, **kwargs):
        player = Player.own_manager.get_player_by_id(kwargs["pk"]).first()
        if player:
            player.delete()
            return Response({"respuesta": "Jugador eliminado correctamente"})
        return Response(
            {"respuesta": f"No se encuentra el jugador con el id {kwargs['pk']}"}
        )
