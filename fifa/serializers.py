from django.db.models import fields
from rest_framework import serializers
from .models import Team, Country, Player, CoachingStaff


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name_team", "flag_photo", "shield_photo", "country")


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            "player_photo",
            "name",
            "last_name",
            "birth_date",
            "team_id",
            "titular",
            "shirt_number",
            "position",
        )


class CoachingStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachingStaff
        fields = ("name", "last_name", "birth_date", "nacionality_id", "rol", "team")
