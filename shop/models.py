from django.db import models
from wowtbc.models import Game

# Create your models here.


class Shop(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField(help_text="Price in USD")
    image = models.ImageField(upload_to="shop", max_length=200)
    description = models.TextField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ["name"]


class Service(Shop):
    pass


class Item(Shop):
    pass


class Account(Shop):
    pass
