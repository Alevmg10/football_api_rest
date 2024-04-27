from django.contrib import admin
from .models import BplTable, BplGames, BplMatches

# Register your models here.
admin.site.register(BplTable)
admin.site.register(BplGames)
admin.site.register(BplMatches)