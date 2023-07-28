from django.db.models import fields
import django_filters

from .models import *


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ["tags"]
