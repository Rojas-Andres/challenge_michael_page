from .models import Country, Team, Player, CoachingStaff
from datetime import datetime, date


def validate_country(country: str):
    get_country = Country.own_manager.filter_country_by_name(country.upper())
    if get_country:
        return get_country
    else:
        return None


def validate_team(team: str):
    get_team = Team.own_manager.filter_team_by_name(team.upper())
    if get_team:
        return get_team
    else:
        return None


def to_bool(value) -> bool:
    if value == "true":
        return True
    elif value == "True":
        return True
    elif value == "false":
        return False
    elif value == "False":
        return False
    elif value == 0:
        return False
    elif value == 1:
        return True
    else:
        raise Exception("Value was not recognized as a valid Boolean.")


def validate_team_by_id(team_id: int):
    get_team = Team.own_manager.get_team_by_id(team_id)
    if get_team:
        return get_team
    else:
        return None


def validate_player_update(data):
    dict_data = {}
    if "birth_date" in data:
        data["birth_date"] = data.birth_date
    else:
        pass


def convert_date(date):
    try:
        birth_date_cast = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None
    return birth_date_cast


def validate_player_create(data: dict):
    res = {}
    try:
        birth_date_cast = datetime.strptime(data["birth_date"], "%Y-%m-%d")
    except ValueError:
        res["respuesta"] = "Recuerde el formato fecha YYYY-MM-DD (AÑO-MES-DIA)"
        return res
    # Validar que el jugador no tenga menos de 15 años
    age = calculate_age(birth_date_cast)
    if age < 15:
        res[
            "respuesta"
        ] = "El jugador que desea inscribir no puede tener menos de 15 años"
        return res
    # Validar que el equipo existe
    team = Team.own_manager.get_team_by_id(data["team_id"]).first()
    if team:
        try:

            titular_bool = to_bool(data["titular"])
            data["titular"] = titular_bool
        except Exception:
            res[
                "respuesta"
            ] = "Recuerde que en titular es un valor boolean (True,False)"
            return res
        # Validar que no hayan mas de 11 titulares
        count_player_titular = Player.own_manager.count_titular_by_team(data["team_id"])
        if count_player_titular >= 11 and titular_bool:
            res[
                "respuesta"
            ] = "Ya tiene 11 jugadores titulares no puede colocar otro mas como titular"
            return res
        count_player_shirt = Player.own_manager.count_shirt_by_team(
            data["team_id"], data["shirt_number"]
        )

        # Validar que no se repita la misma camisa por equipo
        if count_player_shirt != 0:
            res[
                "respuesta"
            ] = "No puede registrar a otro jugador con la misma camiseta en ese equipo"
            return res
        # Validar que se encuentre la posicion en las opciones
        position = validate_position_exist(data["position"])
        if not position:
            res[
                "respuesta"
            ] = f"No existe la posicion {data['position']} recuerde que solo estan estas {get_positions()}"
            return res
        data["position"] = position

        return data
    else:
        res["respuesta"] = f"No existe el equipo con el id {data['team_id']} en la bd!"
        return res


def validate_file(file: str):
    file_permission = ["PNG", "png", "jpg", "JPG"]
    fi = file.split(".")
    if fi[-1] in file_permission:
        return True
    return None


def get_positions():
    """
    Esta funcion me entrega todas las posiciones posibles
    """
    return [i[1] for i in Player.POSITION_OPTIONS]


def validate_position_exist(position: str):
    """
    Esta funcion valida si la posicion enviada existe
    """
    position = position.capitalize()
    result = list(filter(lambda x: x[1] == position, Player.POSITION_OPTIONS))
    if not result:
        return False
    return result[0][0]


def get_rol():
    """
    Esta funcion me entrega todos los posibles roles
    """
    return [i[1] for i in CoachingStaff.ROL_OPTIONS]


def validate_rol_exist(rol: str):
    """
    Esta funcion valida si el rol existe
    """
    rol = rol.capitalize()
    result = list(filter(lambda x: x[1] == rol, CoachingStaff.ROL_OPTIONS))
    if not result:
        return False
    return result[0][0]


def validate_nacionality_exist(nacionality_id: int):
    country = Country.own_manager.filter_country_by_id(nacionality_id)
    if not country:
        return None
    else:
        return country


def calculate_age(birth_date):
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def calculate_avg_age(data: list):
    ages = []
    for i in data:
        ages.append(calculate_age(i["birth_date"]))
    avg_age = sum(ages) / len(ages)
    return avg_age
