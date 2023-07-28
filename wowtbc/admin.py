from django.contrib import admin
from .models import Game, CoinTypeImage, ServersList, ServiceAccount

# Register your models here.

admin.site.register(
    (
        Game,
        CoinTypeImage,
        ServersList,
    )
)


@admin.register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = ("order_id", "username", "password", "vpn", "other_info")
    search_fields = ("order_id", "username", "password", "vpn", "other_info")
