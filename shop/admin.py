from django.contrib import admin
from .models import Service, Item, Account

# Register your models here.
admin.site.register((Service, Item, Account))
