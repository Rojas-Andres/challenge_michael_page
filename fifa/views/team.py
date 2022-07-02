from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response

# from rest_framework.views import viewsets
from rest_framework import viewsets, status, generics

from rest_framework.decorators import api_view
from fifa.serializers import TeamSerializer
from fifa.models import Team
from rest_framework.decorators import action
from fifa.utils import validate_country, validate_team
from fifa.models import Country


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.own_manager.all_teams()

    def list(self, request):
        country = request.GET.get("country")
        if country:
            get_country = Country.own_manager.filter_country_by_name(country.upper())
            if get_country:
                # Obtener el equipo referente a ese pais
                team = Team.own_manager.filter_team_by_country(get_country.get().id)
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
            all_teams = Team.own_manager.all_teams()
            if not all_teams:
                return Response({"respuesta": "No hay equipos en la base de datos!"})
            return Response(all_teams)

    def create(self, request, *args, **kwargs):
        data = request.data
        res = {}
        try:
            if (
                data["name_team"]
                and data["flag_photo"]
                and data["shield_photo"]
                and data["country"]
            ):
                country = validate_country(data["country"])
                if country:
                    id_country = country.get().id
                    team_db = validate_team(data["name_team"])
                    if not team_db:
                        team = Team.own_manager.create_team(data, id_country)

                        team.save()
                        serializer_context = {
                            "request": request,
                        }
                        serializer = TeamSerializer(
                            team, many=False, context=serializer_context
                        )
                        if serializer:
                            return Response(
                                serializer.data, status=status.HTTP_201_CREATED
                            )
                    else:
                        res[
                            "respuesta"
                        ] = f"El equipo {data['name_team']} ya se encuentra creado en la base de datos"
                else:
                    res[
                        "response"
                    ] = f"El pais {data['country']} no se encuentra en la base de datos"
        except KeyError as e:
            res[str(e)] = "Este campo es requerido"

        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        team = Team.own_manager.get_team_by_id(kwargs["pk"]).first()
        if team:
            data = request.data
            if data["name_team"] and team.name_team != data["name_team"]:
                team.name_team = data["title"]
            if data["flag_photo"] and team.name_team != data["flag_photo"]:
                team.flag_photo = data["flag_photo"]
            if data["shield_photo"] and team.name_team != data["shield_photo"]:
                team.shield_photo = data["shield_photo"]
            if data["country"] and team.name_team != data["country"]:
                pass
            team.save()
            return Response({"respuesta": "Equipo actualizado satisfactoriamente!"})
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
