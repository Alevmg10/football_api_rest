from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BrasilATable
from django.db.models import Q
from .serializers import BrasilATableSerializer


class BrasilATableView(APIView):
    def get(self, request):
        # Get the last 20 updates for the Table model in ascending order by id
        last_20_updates = BrasilATable.objects.order_by('position')[:20]
        serializer = BrasilATableSerializer(last_20_updates, many=True)
        return Response(serializer.data)
