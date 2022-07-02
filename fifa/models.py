from django.db import models
from datetime import datetime

# Create your models here.
from . import managers


class Country(models.Model):
    name_country = models.CharField(max_length=255)
    own_manager = managers.CountryManager()

    class Meta:
        verbose_name = "Pais"
        verbose_name_plural = "Paises"

    @classmethod
    def get_by_id(cls, uid):
        return Country.objects.get(id=uid)


class Team(models.Model):
    name_team = models.CharField(verbose_name="Nombre del equipo", max_length=255)
    flag_photo = models.ImageField(
        verbose_name="Foto de la bandera", upload_to="uploads/flag"
    )
    shield_photo = models.ImageField(
        verbose_name="Foto del escudo", upload_to="uploads/shield"
    )
    country = models.OneToOneField(Country, on_delete=models.CASCADE)
    own_manager = managers.TeamManager()

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    @classmethod
    def get_by_id(cls, uid):
        return Team.objects.get(id=uid)


class Player(models.Model):
    GOALKEEPER = "GK"
    DEFENSE = "DF"
    Midfielder = "MD"
    FORWARD = "FW"
    POSITION_OPTIONS = [
        (GOALKEEPER, "Arquero"),
        (DEFENSE, "Defensa"),
        (Midfielder, "Centrocampista"),
        (FORWARD, "Delantero"),
    ]
    player_photo = models.ImageField(
        verbose_name="Foto del jugador", upload_to="uploads/shield"
    )
    name = models.CharField(verbose_name="Nombre(s)", max_length=255)
    last_name = models.CharField(verbose_name="Apellido(s)", max_length=255)
    birth_date = models.DateTimeField(verbose_name="Fecha de nacimiento")
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    titular = models.BooleanField(verbose_name="Titular", default=False)
    shirt_number = models.CharField(verbose_name="Numero de camiseta", max_length=255)
    position = models.CharField("Position", max_length=18, choices=POSITION_OPTIONS)
    own_manager = managers.PlayerManager()

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    @classmethod
    def get_by_id(cls, uid):
        return Player.objects.get(id=uid)

    def get_full_name(self):
        """
        Returns the first_name and the last_name
        """
        return self.name + " " + self.last_name


class CoachingStaff(models.Model):
    TECHNICAL = "TC"
    ASSISTANT = "AS"
    DOCTOR = "MD"
    TRAINER = "PR"
    ROL_OPTIONS = [
        (TECHNICAL, "Tecnico"),
        (ASSISTANT, "Asistente"),
        (DOCTOR, "Medico"),
        (TRAINER, "Preparador"),
    ]
    name = models.CharField(verbose_name="Nombre(s)", max_length=255)
    last_name = models.CharField(verbose_name="Apellido(s)", max_length=255)
    birth_date = models.DateTimeField(verbose_name="Fecha de nacimiento")
    nacionality = models.ForeignKey(Country, on_delete=models.CASCADE)
    rol = models.CharField("Rol", max_length=12, choices=ROL_OPTIONS)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    @classmethod
    def get_by_id(cls, uid):
        return CoachingStaff.objects.get(id=uid)
