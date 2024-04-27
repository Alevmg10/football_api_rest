from django.contrib import admin
from .models import BplTable, BplGames, BplTeamsGoalsData, BplMatches

# Register your models here.
admin.site.register(BplTable)
admin.site.register(BplGames)
admin.site.register(BplTeamsGoalsData)
admin.site.register(BplMatches)