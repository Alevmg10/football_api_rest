from rest_framework import serializers
from .models import LaligaTable, LaligaMatch

class LigaTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaligaTable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses']

class LigaMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaligaMatch
        fields = ['temporada', 'round_number', 'home_team', 'score', 'away_team']