from django import forms
import django_filters
from .models import Service, Item, Account


class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search", "class": "form-control"}
        ),
    )

    class Meta:
        model = Service
        fields = ["name"]


class ItemFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search", "class": "form-control"}
        ),
    )

    class Meta:
        model = Item
        fields = ["name"]


class AccountFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search", "class": "form-control"}
        ),
    )

    class Meta:
        model = Account
        fields = ["name"]
