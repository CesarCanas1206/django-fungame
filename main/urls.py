from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("buy-games/", views.BuyGamesListView.as_view(), name="buy_games_list_view"),
    path(
        "buy-games/<slug:slug>/",
        views.BuyGamesDetailView.as_view(),
        name="buy_games_detail_view",
    ),
    path("sell-games/", views.SellGamesListView.as_view(), name="sell_games_list_view"),
    path(
        "sell-games/<slug:slug>/",
        views.SellGamesDetailView.as_view(),
        name="sell_games_detail_view",
    ),
    # discord links here
    path("ffxiv/", RedirectView.as_view(url="https://discord.gg/ruQjC3Mkq7")),
    path("RS/", RedirectView.as_view(url="https://discord.gg/fjuRFVMufj")),
    path("rs/", RedirectView.as_view(url="https://discord.gg/fjuRFVMufj")),
    path("dofus/", RedirectView.as_view(url="https://discord.gg/ruQjC3Mkq7")),
    path("GIL/", RedirectView.as_view(url="https://discord.gg/ruQjC3Mkq7")),
    path("gil/", RedirectView.as_view(url="https://discord.gg/ruQjC3Mkq7")),
    path("wow/", RedirectView.as_view(url="https://discord.gg/KgMBtDuUX5")),
    path("WOW/", RedirectView.as_view(url="https://discord.gg/KgMBtDuUX5")),
    # page
    path("page/<str:slug>/", views.PageDetailView.as_view(), name="page"),
]
