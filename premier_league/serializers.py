import pytz
from rest_framework import serializers
from .models import BplTable, BplMatchesAll

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BplTable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses']


class MatchSerializer(serializers.ModelSerializer):
    date_time = serializers.SerializerMethodField()


    class Meta:
        model = BplMatchesAll
        fields = ['season', 'date_time', 'round_number', 'home_team', 'home_score','away_score', 'away_team']

    def get_date_time(self, obj):
        # Convert the datetime to the desired timezone
        venezuela_tz = pytz.timezone('America/Caracas')
        local_time = obj.date_time.astimezone(venezuela_tz)
        # Format the datetime to exclude timezone information
        return local_time.strftime('%Y-%m-%d %H:%M:%S')