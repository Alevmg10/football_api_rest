from django.db import models

# Create your models here.
class BrasilATable(models.Model):
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


class BrasilANextMatches(models.Model):
    season = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    away_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.season} / {self.round_number}"