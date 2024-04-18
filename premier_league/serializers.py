from rest_framework import serializers
from .models import BplTable, BplMatch

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BplTable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BplMatch
        fields = ['temporada', 'round_number', 'home_team', 'score', 'away_team']