from django.contrib import admin
from .models import BplTable, BplMatchesAll

# Register your models here.
admin.site.register(BplTable)
admin.site.register(BplMatchesAll)