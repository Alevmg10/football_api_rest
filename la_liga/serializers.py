from rest_framework import serializers
from .models import LaligaTable, LaligaGames

class LigaTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaligaTable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses', 'goal_diff']

class LigaMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaligaGames
        fields = ['season', 'round_number', 'home_team', 'home_score','away_score', 'away_team']