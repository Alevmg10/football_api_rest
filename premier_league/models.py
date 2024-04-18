from django.db import models


class BplTable(models.Model):
    season = models.CharField(max_length=100)
    position = models.IntegerField()
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    played = models.IntegerField()
    wins = models.IntegerField()
    draw = models.IntegerField()
    losses = models.IntegerField()
    goal_diff = models.CharField(max_length=100)


class BplMatch(models.Model):
    temporada = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    score = models.CharField(max_length=10)
    away_team = models.CharField(max_length=100)

# class TeamMatches(models.Model):
#     pass


# class Player(models.Model):
#     name = models.CharField(max_length=100)
#     team = models.ForeignKey(Table, on_delete=models.CASCADE)
    

# class GoalScorer(models.Model):
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     goals = models.IntegerField()
