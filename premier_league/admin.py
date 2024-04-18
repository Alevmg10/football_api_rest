from django.contrib import admin
from .models import BplTable, BplMatch

# Register your models here.
admin.site.register(BplTable)
admin.site.register(BplMatch)