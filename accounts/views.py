from django.shortcuts import render
from django.views import View
from payment.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return render(request, "account/profile.html", {"orders": orders})
