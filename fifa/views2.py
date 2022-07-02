from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response

# from rest_framework.views import viewsets
from rest_framework import viewsets, status, generics

from rest_framework.decorators import api_view
from .serializers import TeamSerializer
from .models import Team
from rest_framework.decorators import action
from .utils import validate_country, validate_team
from .models import Country


# @api_view(["GET"])
# def ApiOverview(request):
#     api_urls = {
#         "all_teams": "/",
#         "Search team by country": "/?country=country_name",
#         "Search by Subcategory": "/?subcategory=category_name",
#         "Add": "/create",
#         "Update": "/update/pk",
#         "Delete": "/item/pk/delete",
#     }

#     return Response(api_urls)

