from django.contrib.sitemaps import Sitemap

from django.urls import reverse

from datetime import datetime
from blog.models import Post
from wowtbc.models import Game
from main.models import Page


class HomeSiteMap(Sitemap):
    priority = 1

    def items(self):
        return ["main:index"]

    def location(self, item):
        return reverse(item)

    # def lastmod(self, obj):
    #     return datetime.strptime("2022-11-08", "%Y-%m-%d").date()


class PageSiteMap(Sitemap):
    priority = 0.8

    def items(self):
        return Page.objects.all()

    def location(self, obj):
        return reverse("main:page", args=[obj.slug])


class BlogSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Post.objects.filter(active=True)

    def lastmod(self, obj):
        return obj.created


class BuyGameSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Game.objects.all()

    def location(self, obj):
        return reverse("main:buy_games_detail_view", args=[obj.slug])


class SellGameSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Game.objects.all()

    def location(self, obj):
        return reverse("main:sell_games_detail_view", args=[obj.slug])
