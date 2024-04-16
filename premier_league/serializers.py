from rest_framework import serializers
from .models import Table, Match

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['temporada', 'round_number', 'home_team', 'score', 'away_team']