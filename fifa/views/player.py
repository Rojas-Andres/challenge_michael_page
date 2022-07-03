from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response

# from rest_framework.views import viewsets
from rest_framework import viewsets, status, generics

from rest_framework.decorators import api_view
from fifa.serializers import PlayerSerializer
from fifa.models import Team
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
)
from fifa.models import Player
from django.http import HttpResponse


class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.own_manager.all_player()

    def list(self, request):
        id_player = request.GET.get("id")
        if id_player:
            print("adasddsads")
            get_player = Player.own_manager.get_player_by_id(id_player)
            if get_player:

                serializer_context = {
                    "request": request,
                }
                serializer = PlayerSerializer(
                    get_player.get(), many=False, context=serializer_context
                )
                if serializer:
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "response": f"No existe el jugador {id_player} en la base de datos"
                    }
                )
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
                data["player_photo"]
                and data["name"]
                and data["last_name"]
                and data["birth_date"]
                and data["team_id"]
                and data["titular"]
                and data["shirt_number"]
                and data["position"]
            ):
                player = validate_player_create(data)
                if "respuesta" in player:
                    return Response(player, status=status.HTTP_400_BAD_REQUEST)
                new_player = Player.own_manager.create_player(data)
                new_player.save()
                return Response({"respuesta": "Jugador creado correctamente!"})

        except KeyError as e:
            res[str(e)] = "Este campo es requerido"

        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        player = Player.own_manager.get_player_by_id(kwargs["pk"]).first()
        res = {}
        if player:
            data = request.data
            new_dict = {}
            # Validamos que al equipo que quiera actualizar exista
            if "team_id" in data:
                team = Team.own_manager.get_team_by_id(data["team_id"]).first()
                if team:
                    new_dict["team_id"] = data["team_id"]
                else:
                    res[
                        "respuesta"
                    ] = f"No existe el equipo con el id {data['team_id']} en la bd!"
                    return res
            else:
                new_dict["team_id"] = player.team_id

            # Validar fecha
            if "birth_date" in data:
                date = convert_date(data["birth_date"])
                if not date:
                    res[
                        "respuesta"
                    ] = "Recuerde el formato fecha YYYY-MM-DD (AÑO-MES-DIA)"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                date = player.birth_date.strftime("%Y-%m-%d")
            new_dict["birth_date"] = date

            # Validar titular
            if "titular" in data:
                new_dict["titular"] = to_bool(data["titular"])
                if new_dict["titular"] != player.titular:
                    count_player_titular = Player.own_manager.count_titular_by_team(
                        new_dict["team_id"]
                    )
                    if count_player_titular >= 11 and data["titular"] == True:
                        res[
                            "respuesta"
                        ] = "Ya tiene 11 jugadores titulares no puede colocar otro mas como titular"
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_dict["titular"] = player.titular
            # Validar shirt number
            if "shirt_number" in data:
                new_dict["shirt_number"] = data["shirt_number"]
                if new_dict["shirt_number"] != player.shirt_number:
                    count_player_shirt = Player.own_manager.count_shirt_by_team(
                        new_dict["team_id"], new_dict["shirt_number"]
                    )
                    if count_player_shirt != 0:
                        res[
                            "respuesta"
                        ] = "No puede registrar a otro jugador con la misma camiseta en ese equipo"
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_dict["shirt_number"] = player.shirt_number
            # Validate position
            if "position" in data:
                position = validate_position_exist(data["position"])
                if not position:
                    res[
                        "respuesta"
                    ] = f"No existe la posicion {data['position']} recuerde que solo estan estas {get_positions()}"
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
                new_dict["position"] = position
            else:
                new_dict["position"] = player.position
            player.name = data.get("name", player.name)
            player.last_name = data.get("last_name", player.last_name)
            player.birth_date = new_dict["birth_date"]
            player.team_id = new_dict["team_id"]
            player.birth_date = new_dict["birth_date"]
            player.team_id = new_dict["team_id"]
            player.titular = new_dict["titular"]
            player.shirt_number = new_dict["shirt_number"]
            player.position = new_dict["position"]
            player.save()
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
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
