from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path("", views.sell_wow, name="sell_wow_tbc"),
    path("sell-gold/", views.sell_wow_token, name="sell_wow_token"),
    path(
        "sell-gold/<str:slug>/",
        views.sell_wow_token_step2,
        name="sell_wow_token_step2",
    ),
]
