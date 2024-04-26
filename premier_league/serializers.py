from rest_framework import serializers
from .models import BplTable, BplGames

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BplTable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = BplGames
        fields = ['season', 'round_number', 'home_team', 'home_score','away_score', 'away_team']