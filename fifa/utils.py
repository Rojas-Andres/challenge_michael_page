from .models import Country, Team


def validate_country(country):
    get_country = Country.own_manager.filter_country_by_name(country.upper())
    if get_country:
        return get_country
    else:
        return None


def validate_team(team):
    get_team = Team.own_manager.filter_team_by_name(team.upper())
    if get_team:
        return get_team
    else:
        return None
