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

    def __str__(self):
        return f"{self.position} - {self.team}"
    

class LaLigaGamesAll(models.Model):
    season = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    away_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.season} / {self.round_number}"