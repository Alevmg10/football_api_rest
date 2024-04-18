from django.contrib import admin
from .models import LaligaMatch, LaligaTable

# Register your models here.
admin.site.register(LaligaTable)
admin.site.register(LaligaMatch)