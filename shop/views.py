import stripe
from django_filters.views import FilterView

from django.views.generic import DetailView, ListView, View
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from wowtbc.models import Game
from wowtbc.forms import ServiceAccountForm
from payment.models import Order, PAYMENT_CHOICES, STATUS_CHOICES
from .models import Service, Item, Account
from .filters import ServiceFilter, ItemFilter, AccountFilter

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class BestSellerDetailView(DetailView):
    template_name = "main/buy_games/best-seller.html"
    model = Game
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        game = self.get_object()
        context = super(BestSellerDetailView, self).get_context_data(**kwargs)
        context["services"] = Service.objects.filter(game=game, featured=True)
        context["items"] = Item.objects.filter(game=game, featured=True)
        context["accounts"] = Account.objects.filter(game=game, featured=True)
        context["game"] = game
        return context


class ServiceListView(FilterView):
    template_name = "main/buy_games/services.html"
    model = Service
    context_object_name = "services"
    filterset_class = ServiceFilter

    def get_queryset(self):
        game_slug = self.kwargs.get("slug")
        game = Game.objects.get(slug=game_slug)
        return Service.objects.filter(game=game)

    def get_context_data(self, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        game_slug = self.kwargs.get("slug")
        game = Game.objects.get(slug=game_slug)
        context["game"] = game
        return context


class CreateCheckoutSessionView(View):
    def post(self, request):
        item_type = request.POST["item_type"]
        item_id = request.POST["item_id"]
        quantity = int(request.POST.get("quantity", 1))
        protocol = "https://" if request.is_secure() else "http://"
        domain = request.get_host()
        domain_name = protocol + domain
        if item_type == "service":
            item = get_object_or_404(Service, id=item_id)
        elif item_type == "item":
            item = get_object_or_404(Item, id=item_id)
        elif item_type == "account":
            item = get_object_or_404(Account, id=item_id)

        # Create the Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=request.user.email
            if request.user.is_authenticated
            else None,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": int(item.price * 100),  # Price in cents
                    },
                    "quantity": quantity,
                },
            ],
            metadata={
                "game": item.game,
                "item_type": item_type,
                "item_id": item.id,
                "quantity": quantity,
            },
            mode="payment",
            # get the domain name from the request
            success_url=f"{domain_name}/shop/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_name}",
        )

        Order.objects.create(
            order_id=session.id,
            user=request.user if request.user.is_authenticated else None,
            item=item,
            payment_method=PAYMENT_CHOICES.STRIPE,
            amount=int(session.amount_total) / 100,
            quantity=session.metadata.get("quantity"),
            currency="USD",
        )

        return render(
            request,
            "shop/checkout.html",
            {"session_id": session.id, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY},
        )


class ItemListView(FilterView):
    template_name = "main/buy_games/items.html"
    model = Item
    context_object_name = "items"
    filterset_class = ItemFilter

    def get_queryset(self):
        game_slug = self.kwargs.get("slug")
        game = Game.objects.get(slug=game_slug)
        return Item.objects.filter(game=game)

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        game_slug = self.kwargs.get("slug")
        game = Game.objects.get(slug=game_slug)
        context["game"] = game
        return context


class AccountListView(FilterView):
    template_name = "main/buy_games/accounts.html"
    model = Service
    context_object_name = "accounts"
    filterset_class = ServiceFilter

    def get_queryset(self):
        game_slug = self.kwargs.get("slug")
        game = Game.objects.get(slug=game_slug)
        return Account.objects.filter(game=game)

    def get_context_data(self, **kwargs):
        context = super(AccountListView, self).get_context_data(**kwargs)
        game_slug = self.kwargs.get("slug")
        game = Game.objects.get(slug=game_slug)
        context["game"] = game
        return context


class CheckoutSuccessView(View):
    form = ServiceAccountForm
    template_name = "shop/success.html"

    def get(self, request):
        session_id = request.GET.get("session_id")
        session = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(Order, order_id=session_id)
        order.status = (
            STATUS_CHOICES.COMPLETED
            if session.payment_status == "paid"
            else STATUS_CHOICES.FAILED
        )
        order.save()
        # Confirm the payment and update your database
        return render(
            request,
            self.template_name,
            {
                "intent": session,
                "order": order,
                "form": self.form(initial={"order_id": session_id}),
            },
        )

    def post(self, request):
        form = ServiceAccountForm(request.POST)
        session_id = request.POST.get("order_id")
        session = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(Order, order_id=session_id)
        if form.is_valid():
            form.save()
        return render(
            request,
            self.template_name,
            {"intent": session, "order": order},
        )


class CheckoutCancelView(View):
    def get(self, request):
        return render(request, "shop/cancel.html")
