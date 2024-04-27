"""
URL configuration for football_api_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from premier_league.views import MatchList, TableView, TodayMatches
from la_liga.views import LaligaTableView, LaligaMatchList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/premierleague/matches/', MatchList.as_view(), name='bpl-match-list'),
    path('api/premierleague/table', TableView.as_view(), name='bpl-table'),
    path('api/premierleague/current_matches', TodayMatches.as_view(), name='bpl-current_matches'),
    path('api/laliga/table', LaligaTableView.as_view(), name='laliga-table'),
    path('api/laliga/matches/', LaligaMatchList.as_view(), name='laliga-table'),
]
