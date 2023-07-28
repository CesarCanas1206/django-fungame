from django.urls import path
from . import views

urlpatterns = [
    path(
        "create-checkout-session/",
        views.CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("success/", views.CheckoutSuccessView.as_view(), name="checkout_success"),
    path("cancel/", views.CheckoutCancelView.as_view(), name="checkout_cancel"),
    path(
        "<slug:slug>/best-seller/",
        views.BestSellerDetailView.as_view(),
        name="best_seller_detail_view",
    ),
    path(
        "<slug:slug>/services/",
        views.ServiceListView.as_view(),
        name="services_list_view",
    ),
    path(
        "<slug:slug>/items/",
        views.ItemListView.as_view(),
        name="items_list_view",
    ),
    path(
        "<slug:slug>/accounts/",
        views.AccountListView.as_view(),
        name="accounts_list_view",
    ),
]
