from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from fifa.utils import validate_country
from fifa.models import Country
from fifa.serializers import CountrySerializer


@api_view(["POST"])
def create_country(request):
    """
    Esta api se encarga de crear el pais
    """
    data = request.data
    res = {}
    try:
        if data["country"]:
            get_country = validate_country(data["country"])
            if not get_country:
                country = Country.own_manager.create_country(data["country"].upper())
                country.save()
                res[
                    "respuesta"
                ] = f"Pais {data['country'].upper()} creado satisfactoriamente"
            else:
                res[
                    "respuesta"
                ] = f"El pais {data['country'].upper()} ya existe en la base de datos."
            pass
    except KeyError as e:
        res[str(e)] = "Este campo es requerido"

    return Response(res, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_all_country(request):
    get_all_countrys = Country.own_manager.get_all_country()

    serializer_context = {
        "request": request,
    }
    serializer = CountrySerializer(
        get_all_countrys, many=True, context=serializer_context
    )
    if serializer:
        return Response(serializer.data, status=status.HTTP_201_CREATED)
