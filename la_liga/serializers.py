import pytz
from rest_framework import serializers
from .models import LaligaTable, LaLigaGamesAll

class LigaTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaligaTable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses', 'goal_diff']

class LigaMatchSerializer(serializers.ModelSerializer):
    date_time = serializers.SerializerMethodField()


    class Meta:
        model = LaLigaGamesAll
        fields = ['season', 'date_time', 'round_number', 'home_team', 'home_score','away_score', 'away_team']

    def get_date_time(self, obj):
        # Convert the datetime to the desired timezone
        venezuela_tz = pytz.timezone('America/Caracas')
        local_time = obj.date_time.astimezone(venezuela_tz)
        # Format the datetime to exclude timezone information
        return local_time.strftime('%Y-%m-%d %H:%M:%S')