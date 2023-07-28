from django import template
from currencies.models import Currency

register = template.Library()


@register.filter
def to_string(value):
    return str(value)


@register.filter
def currency_symbol(currency_code):
    try:
        currency = Currency.objects.get(code=currency_code)
        return currency.symbol
    except Currency.DoesNotExist:
        return ""
