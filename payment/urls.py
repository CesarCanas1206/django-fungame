from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path("verification/", views.coinbase_webhook, name="payment_verification"),
    path("status/<str:pk>/", views.payment_status, name="payment_status"),
    path("<str:pk>/", views.payment_success, name="payment_success"),
]
