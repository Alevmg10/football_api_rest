from django.contrib import admin
from .models import BrasilATable, BrasilANextMatches, BrasilAMatchesAll
# Register your models here.

admin.site.register(BrasilATable)
admin.site.register(BrasilANextMatches)
admin.site.register(BrasilAMatchesAll)