from django import forms
from .models import ServiceAccount


class ServiceAccountForm(forms.ModelForm):
    class Meta:
        model = ServiceAccount
        fields = ("order_id", "username", "password", "vpn", "other_info")
        widgets = {
            "order_id": forms.HiddenInput(),
        }
