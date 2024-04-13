from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100)

class Match(models.Model):
    temporada = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    score = models.CharField(max_length=10)
    away_team = models.CharField(max_length=100)

# class Player(models.Model):
#     name = models.CharField(max_length=100)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)

class GoalScorer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    goals = models.IntegerField()
