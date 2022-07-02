from django.db import models
from datetime import datetime

from django.db.models import F


class CountryManager(models.Manager):
    def filter_country_by_name(self, country):
        return self.filter(name_country=country.upper())

    def create_country(self, country):
        return self.create(name_country=country)


class PlayerManager(models.Manager):
    def all_player(self):
        return self.all().values(
            "player_photo",
            "name",
            "last_name",
            "birth_date",
            "team__name_team",
            "titular",
            "shirt_number",
            "position",
        )

    def create_player(self, data):
        #     data["player_photo"]
        # and data["name"]
        # and data["last_name"]
        # and data["birth_date"]
        # and data["team_id"]
        # and data["titular"]
        # and data["shirt_number"]
        # and data["position"]
        return self.create(
            player_photo=data["player_photo"],
            name=data["name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"],
            team_id=data["team_id"],
            titular=data["titular"],
            shirt_number=data["shirt_number"],
            position=data["position"],
        )

    def count_titular_by_team(self, team_id):
        return self.filter(team_id=team_id, titular=True).count()

    def count_shirt_by_team(self, team_id, shirt_number):
        return self.filter(team_id=team_id, shirt_number=shirt_number).count()


class TeamManager(models.Manager):
    def filter_team_by_name(self, team):
        return self.filter(name_team=team)

    def filter_team_by_country(self, country_id):
        return self.filter(country_id=country_id)

    def filter_team_by_country_name(self, country_name):
        return self.filter(country__name_country=country_name)

    def all_teams(self):
        return self.all().values(
            "id",
            "name_team",
            "flag_photo",
            "shield_photo",
            "country__name_country",
        )

    def create_team(self, data, id_country):
        return self.create(
            name_team=data["name_team"],
            flag_photo=data["flag_photo"],
            shield_photo=data["shield_photo"],
            country_id=id_country,
        )

    def get_team_by_id(self, id_team):
        return self.filter(id=id_team)

    def detroy_team_by_id(self, id):
        pass
