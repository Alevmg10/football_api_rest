from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Table, Match
from .serializers import TableSerializer, MatchSerializer


class TableView(APIView):
    def get(self, request):
        table = Table.objects.all()
        serializer = TableSerializer(table, many=True)
        return Response(serializer.data)

class MatchList(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        round_number = self.request.query_params.get('round_number')

        if round_number is not None:
            queryset = queryset.filter(round_number=round_number)

        return queryset