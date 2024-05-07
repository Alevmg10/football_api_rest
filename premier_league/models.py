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

    def __str__(self):
        return f"{self.position} - {self.team}"


class BplGames(models.Model):
    season = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    away_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.season} / {self.round_number}"


class BplMatches(models.Model):
    season = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    home_score = models.CharField(max_length=100)
    away_score = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.season} / {self.round_number}"
    

class BplMatchesTest(models.Model):
    season = models.CharField(max_length=100)
    round_number = models.IntegerField()
    home_team = models.CharField(max_length=100)
    home_score = models.CharField(max_length=100)
    away_score = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.season} / {self.round_number}"