from django.contrib import admin
from .models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "payment_method", "amount", "status")
    list_filter = ("user", "status")
    search_fields = ("user", "item", "payment_method", "amount", "status", "order_id")
