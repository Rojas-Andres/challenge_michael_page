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
                        # Validar que ya no exista un equipo con ese pais
                        team_c = Team.own_manager.filter_team_by_country_name(
                            data["country"]
                        )
                        if not team_c:
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
                            ] = "Ya se encuentra un equipo creado con ese pais"
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
            if (
                "name_team" in data
                or "flag_photo" in data
                or "shield_photo" in data
                or "country" in data
            ):

                if "name_team" in data and team.name_team != data["name_team"]:
                    team.name_team = data["title"]
                if "flag_photo" in data and team.name_team != data["flag_photo"]:
                    team.flag_photo = data["flag_photo"]
                if "shield_photo" in data and team.name_team != data["shield_photo"]:
                    team.shield_photo = data["shield_photo"]
                if "country" in data and team.name_team != data["country"]:
                    team.country = data["country"]
                team.save()
                return Response({"respuesta": "Equipo actualizado satisfactoriamente!"})
            else:
                return Response(
                    {
                        "respuesta": "Recuerde que debe de enviar al menos uno de estos [name_team,flag_photo,shield_photo,country] "
                    }
                )
        return Response(
            {"respuesta": f"No se encuentra el equipo con el id {kwargs['pk']}"}
        )

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
