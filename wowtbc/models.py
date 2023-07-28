from django.db import models
from django_extensions.db.fields import AutoSlugField

from ckeditor_uploader.fields import RichTextUploadingField


class CoinTypeImage(models.Model):
    image = models.ImageField(upload_to="CoinType", null=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = "Coin Type Image"
        verbose_name_plural = "Coin Type Images"


class ServersList(models.Model):
    name = models.CharField(max_length=100)
    servers_list = models.TextField(
        blank=True, null=True, help_text="Comma separated list of servers"
    )

    def __str__(self):
        return self.name

    def get_servers_list(self):
        return [item.strip() for item in self.servers_list.split(",")]


class Game(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from=["title"])
    image = models.ImageField(upload_to="games", verbose_name="Thumbnail")
    header_image = models.ForeignKey(CoinTypeImage, on_delete=models.CASCADE, null=True)
    buy_price = models.FloatField(help_text="Price per 1 Unit coins")
    sell_price = models.FloatField(help_text="Price per 1 Unit coins")
    min_sale = models.FloatField()
    unit = models.CharField(max_length=1, choices=(("K", "K"), ("M", "M")), default="K")
    gold_type = models.CharField(max_length=100)
    servers_list = models.ForeignKey(
        ServersList, on_delete=models.SET_NULL, null=True, blank=True
    )
    stock = models.CharField(max_length=10, default="0M", help_text="e.g 100K or 100M")
    show_rg = models.BooleanField(verbose_name="Show Region & Server", default=False)
    show_faction = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    body = RichTextUploadingField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]


class ServiceAccount(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    vpn = models.CharField(max_length=100)
    other_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.order_id
