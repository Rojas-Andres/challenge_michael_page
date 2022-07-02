from django.db.models import fields
from rest_framework import serializers
from .models import Team, Country


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name_team", "flag_photo", "shield_photo", "country")
