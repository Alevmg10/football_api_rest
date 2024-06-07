from django.contrib import admin
from .models import LaLigaGamesAll, LaligaTable

# Register your models here.
admin.site.register(LaligaTable)
admin.site.register(LaLigaGamesAll)