from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LaligaTable, LaligaGames
from django.db.models import Q
from .serializers import LigaTableSerializer, LigaMatchSerializer


class LaligaTableView(APIView):
    def get(self, request):
        # Get the last 20 updates for the Table model in ascending order by id
        last_20_updates = LaligaTable.objects.order_by('position')[:20]
        serializer = LigaTableSerializer(last_20_updates, many=True)
        return Response(serializer.data)
    

class LaligaMatchList(generics.ListAPIView):
    queryset = LaligaGames.objects.all()
    serializer_class = LigaMatchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the round_number and team from query parameters
        season = self.request.query_params.get('season')
        round_number = self.request.query_params.get('round_number')
        team = self.request.query_params.get('team')

        # Filter by season if provided, otherwise default to '2023/2024'
        if season:
            queryset = queryset.filter(season=season)
        else:
            queryset = queryset.filter(season='2023/2024')


        # If both round_number and team are provided, filter by both
        if round_number is not None and team is not None:
            queryset = queryset.filter(round_number=round_number)
            queryset = queryset.filter(Q(home_team=team) | Q(away_team=team))

        # If only round_number is provided, filter by it
        elif round_number is not None:
            queryset = queryset.filter(round_number=round_number)

        # If only team is provided, filter by it
        elif team is not None:
            queryset = queryset.filter(Q(home_team=team) | Q(away_team=team))           

        return queryset