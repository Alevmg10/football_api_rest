from django.db import models


class Table(models.Model):
    season = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    points = models.CharField(max_length=100)
    played = models.CharField(max_length=100)
    wins = models.CharField(max_length=100)
    draw = models.CharField(max_length=100)
    losses = models.CharField(max_length=100)


# class Team(models.Model):
#     name = models.CharField(max_length=100)
#     team = models.ForeignKey(Table, on_delete=models.CASCADE)


class Match(models.Model):
    temporada = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    score = models.CharField(max_length=10)
    away_team = models.CharField(max_length=100)


# class Player(models.Model):
#     name = models.CharField(max_length=100)
#     team = models.ForeignKey(Table, on_delete=models.CASCADE)
    

# class GoalScorer(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     goals = models.IntegerField()
