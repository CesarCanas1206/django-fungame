import random, string


from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import render, redirect
from django.conf import settings

from coinbase_commerce.client import Client
from currencies.utils import calculate
import stripe

from blog.models import Post
from wowtbc.models import Game
from payment.models import Order, STATUS_CHOICES, PAYMENT_CHOICES
from .models import Page
from shop.models import Service, Item, Account

stripe.api_key = settings.STRIPE_SECRET_KEY


client = Client(api_key=settings.COINBASE_API_KEY)


def index(request):
    title = "VIRTGOLD | Buy & Sell Ingame Gold"
    description = "Virtgold is one of the best websites to Buy ingame virtual gold. With multiple payment options, you can either buy or sell osrs or rs3 gold."
    tags = [
        "virtgold",
        "virt gold",
        "buy gold",
        "buy ingame currencies",
        "sell currency",
    ]
    ogtype = "article"
    posts = Post.objects.filter(active=True, featured=True).order_by("-id")[0:3]
    featured_games = Game.objects.filter(featured=True)

    context = {
        "posts": posts,
        "title": title,
        "description": description,
        "tags": tags,
        "ogtype": ogtype,
        "featured_games": featured_games,
    }
    return render(request, "main/index.html", context)


# Game
class BuyGamesListView(ListView):
    model = Game
    template_name = "main/buy_games/list.html"
    context_object_name = "games"


class BuyGamesDetailView(DetailView):
    model = Game
    template_name = "main/buy_games/detail.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super(BuyGamesDetailView, self).get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(active=True, featured=True).order_by(
            "-id"
        )[0:3]
        return context

    def post(self, request, *args, **kwargs):
        game = self.get_object()
        user = request.user if request.user.is_authenticated else None
        up_id = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(7)
        )
        unique = False
        while unique == False:
            try:
                Order.objects.get(order_id=up_id)
                up_id = "".join(
                    random.choice(string.ascii_lowercase + string.digits)
                    for _ in range(7)
                )
            except:
                unique = True

        site = get_current_site(request).domain
        currency = request.POST.get("currency")
        region = None
        server = None
        faction = None

        if game.show_rg:
            region = request.POST.get("region", None)
            server = request.POST.get("server", None)
        if game.show_faction:
            faction = request.POST.get("faction", None)

        base_success_url = f"https://{site}/payment"
        if settings.DEBUG == True:
            base_success_url = f"http://{site}/payment"
        f_payment = request.POST.get("payment")
        f_ign = request.POST.get("ign")
        f_email = request.POST.get("email")
        f_quantity = float(request.POST.get("gold_amount"))
        f_total_usd = f_quantity * float(calculate(game.buy_price, currency))

        if f_payment == "Coinbase":
            payment_success = f"{base_success_url}/{up_id}"
            charge_info = {
                "name": f_ign,
                "description": f"Payment to buy {game.title}",
                "local_price": {"amount": f_total_usd, "currency": currency},
                "pricing_type": "fixed_price",
                "metadata": {
                    "ign": f_ign,
                    "email": f_email,
                    "quantity": int(f_quantity),
                    "region": region,
                    "faction": faction,
                    "server": server,
                    "game_title": game.title,
                },
                "redirect_url": payment_success,
            }
            charge = client.charge.create(**charge_info)

            Order.objects.create(
                order_id=charge.get("id"),
                user=user,
                item=game,
                payment_method=PAYMENT_CHOICES.COINBASE,
                amount=calculate(f_total_usd, currency),
                quantity=f_quantity,
                currency=currency,
            )
            return redirect(charge.get("hosted_url"))
        elif (
            f_payment == "Visa/Master Card"
            or f_payment == "Apple Pay"
            or f_payment == "Google Pay"
        ):
            payment_success = f"{base_success_url}/{up_id}"
            product = stripe.Product.create(name=f_ign)
            f_total = int(
                (
                    f_total_usd
                    + (
                        f_total_usd * 0.047
                        if currency == "USD"
                        else f_total_usd * 0.037
                    )
                )
                * 100
            )
            price = stripe.Price.create(
                unit_amount=f_total, currency=currency, product=product.id
            )
            ref_key = "{CHECKOUT_SESSION_ID}"
            session = stripe.checkout.Session.create(
                customer_email=f_email,
                success_url=f"{payment_success}?payment_ref={ref_key}",
                metadata={
                    "ign": f_ign,
                    "email": f_email,
                    "quantity": f_quantity,
                    "region": region,
                    "faction": faction,
                    "server": server,
                    "game_title": game.title,
                    "gold_type": game.gold_type,
                },
                line_items=[
                    {
                        "price": price.id,
                        "quantity": 1,
                    },
                ],
                mode="payment",
            )
            Order.objects.create(
                order_id=session.id,
                user=user,
                item=game,
                payment_method=PAYMENT_CHOICES.STRIPE,
                amount=calculate(f_total_usd, currency),
                quantity=f_quantity,
                currency=currency,
            )
            return redirect(session.url)

        return render(request, self.template_name)


# sell game
class SellGamesListView(ListView):
    model = Game
    template_name = "main/sell_games/list.html"
    context_object_name = "games"


class SellGamesDetailView(DetailView):
    model = Game
    template_name = "main/sell_games/detail.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super(SellGamesDetailView, self).get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(active=True, featured=True).order_by(
            "-id"
        )[0:3]
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = "main/page.html"
    context_object_name = "page"
    slug_field = "slug"
    slug_url_kwarg = "slug"
