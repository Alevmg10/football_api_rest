import pytz
from rest_framework import serializers
from .models import BrasilATable, BrasilAMatchesAll, BrasilANextMatches
from utils.probabilidad import Probabilidades 

class BrasilATableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrasilATable
        fields = ['season', 'position', 'team', 'points', 'played', 'wins', 'draw', 'losses', 'goal_diff']


class BrasilAMatchesSerializer(serializers.ModelSerializer):
    date_time = serializers.SerializerMethodField()


    class Meta:
        model = BrasilAMatchesAll
        fields = ['season', 'date_time', 'round_number', 'home_team', 'home_score','away_score', 'away_team']

    def get_date_time(self, obj):
        # Convert the datetime to the desired timezone
        venezuela_tz = pytz.timezone('America/Caracas')
        local_time = obj.date_time.astimezone(venezuela_tz)
        # Format the datetime to exclude timezone information
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    

class BrasilANextMatchesSerializer(serializers.ModelSerializer):
    date_time = serializers.SerializerMethodField()


    class Meta:
        model = BrasilANextMatches
        fields = ['season', 'date_time', 'round_number', 'home_team', 'home_score','home_prob', 'away_score', 'away_prob', 'away_team']

    def get_date_time(self, obj):
        # Convert the datetime to the desired timezone
        venezuela_tz = pytz.timezone('America/Caracas')
        local_time = obj.date_time.astimezone(venezuela_tz)
        # Format the datetime to exclude timezone information
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_probabilities(self, obj):
        # Assuming `self.context['matches']` contains the list of matches for probabilities calculation
        matches = self.context.get('matches', [])
        upcoming_match = [obj]  # The match we are serializing is the upcoming match

        prob_calculator = Probabilidades(data=matches, data2=upcoming_match)
        return prob_calculator.probabilidad()