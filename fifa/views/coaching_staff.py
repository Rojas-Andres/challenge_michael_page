from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response

# from rest_framework.views import viewsets
from rest_framework import viewsets, status, generics

from rest_framework.decorators import api_view
from fifa.serializers import CoachingStaffSerializer
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
    validate_nacionality_exist,
    calculate_age,
)
from fifa.models import Player
from django.http import HttpResponse


class CoachingStaffViewSet(viewsets.ModelViewSet):
    serializer_class = CoachingStaffSerializer
    queryset = CoachingStaff.own_manager.get_all_coaching()

    def list(self, request):
        id_coaching = request.GET.get("id")
        if id_coaching:
            get_coaching = CoachingStaff.own_manager.get_coaching_by_id(id_coaching)
            if get_coaching:
                serializer_context = {
                    "request": request,
                }
                serializer = CoachingStaffSerializer(
                    get_coaching.get(), many=False, context=serializer_context
                )
                if serializer:
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "response": f"No existe el coaching {id_coaching} en la base de datos"
                    }
                )

        else:
            all_coaching = CoachingStaff.own_manager.get_all_coaching()
            if not all_coaching:
                return Response(
                    {"respuesta": "No hay cuerpo tecnico en la base de datos!"}
                )
            return Response(all_coaching)

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
                country = validate_nacionality_exist(data["nacionality_id"])
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

                age = calculate_age(date)
                if age < 15:
                    res[
                        "respuesta"
                    ] = "El coach que desea inscribir no puede tener menos de 15 años"
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
        coaching = CoachingStaff.own_manager.get_coaching_by_id(kwargs["pk"]).first()
        res = {}
        if coaching:
            data = request.data

            # Validamos birth_date
            if "birth_date" in data:
                date = convert_date(data["birth_date"])
                if not date:
                    res[
                        "respuesta"
                    ] = "Recuerde el formato fecha YYYY-MM-DD (AÑO-MES-DIA)"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                age = calculate_age(date)

                if age < 15:
                    res[
                        "respuesta"
                    ] = "El coach que desea inscribir no puede tener menos de 15 años"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)

                if date != coaching.birth_date:
                    coaching.birth_date = date

            if "nacionality_id" in data:
                if data["nacionality_id"] != coaching.nacionality_id:
                    # Validar si la nacionalidad existe
                    country = validate_nacionality_exist(data["nacionality_id"])
                    if not country:
                        res[
                            "respuesta"
                        ] = f"El pais con el id {data['nacionality_id']} no existe en la base de datos"
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)
                    coaching.nacionality_id = country.get().id
                else:
                    pass
            # Validamos el rol
            if "rol" in data:
                rol = validate_rol_exist(data["rol"])
                if not rol:
                    res[
                        "respuesta"
                    ] = f"Recuerde que los roles permitidos son {get_rol()}"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                coaching.rol = rol

            # Validamos si el equipo existe
            if "team_id" in data:
                team = Team.own_manager.get_team_by_id(data["team_id"])
                if not team:
                    res[
                        "respuesta"
                    ] = f"El equipo con el id {data['team_id']} no existe en la base de datos"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                coaching.team_id = team.get().id
            coaching.name = data.get("name", coaching.name)
            coaching.last_name = data.get("last_name", coaching.last_name)
            coaching.save()
            serializer = CoachingStaffSerializer(coaching)
            return Response(serializer.data)
        return Response(
            {"respuesta": f"No se encuentra el coaching con el id {kwargs['pk']}"}
        )

    def destroy(self, request, *args, **kwargs):
        coaching = CoachingStaff.own_manager.get_coaching_by_id(kwargs["pk"]).first()
        if coaching:
            coaching.delete()
            return Response({"respuesta": "Cuerpo tecnico eliminado correctamente"})
        return Response(
            {"respuesta": f"No se encuentra el cuerpo tecnico con el id {kwargs['pk']}"}
        )
