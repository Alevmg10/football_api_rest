from rest_framework import serializers
from .models import BrasilATable

class BrasilATableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrasilATable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses', 'goal_diff']

