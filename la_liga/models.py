from django.db import models


class LaligaTable(models.Model):
    season = models.CharField(max_length=100)
    position = models.IntegerField()
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    played = models.IntegerField()
    wins = models.IntegerField()
    draw = models.IntegerField()
    losses = models.IntegerField()
    goal_diff = models.CharField(max_length=100)


class LaligaMatch(models.Model):
    temporada = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    score = models.CharField(max_length=10)
    away_team = models.CharField(max_length=100)