from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from coinbase_commerce.error import WebhookInvalidPayload, SignatureVerificationError
from coinbase_commerce.webhook import Webhook
from coinbase_commerce.client import Client
import stripe

from .models import Order, STATUS_CHOICES

client = Client(api_key=settings.COINBASE_API_KEY)


def payment_success(request, pk):
    try:
        payment_ref = request.GET.get("payment_ref")
        db_info = Order.objects.get(order_id=payment_ref)
        if payment_ref:
            intent = stripe.checkout.Session.retrieve(payment_ref)
            if intent.payment_status == "paid":
                db_info.status = STATUS_CHOICES.COMPLETED
                db_info.save()
            context = {
                "db_info": db_info,
                "payment_details": intent,
            }
            return render(request, "main/webhook-stripe.html", context)
        else:
            charge = client.charge.retrieve(db_info.code)
            context = {
                "db_info": db_info,
                "payment_details": charge,
            }
            return render(request, "main/webhook.html", context)
    except:
        return HttpResponse(status=404)


def payment_status(request, pk):
    if request.method == "GET":
        order = Order.objects.get(order_id=pk)
        status = order.get_status_display()
        metadata = {
            "quantity": order.quantity,
            "payment_ID": order.order_id,
        }
        return JsonResponse({"status": status, "metadata": metadata})

    else:
        return HttpResponseNotFound("<h1>Page not found</h1>")


@csrf_exempt
def coinbase_webhook(request):
    if request.method == "POST":
        secret_key = settings.COINBASE_SECRET_KEY
        # event payload
        request_data = request.body.decode("utf-8")
        # webhook signature
        request_sig = request.headers.get("X-CC-Webhook-Signature")

        try:
            # signature verification and event object construction
            event = Webhook.construct_event(request_data, request_sig, secret_key)

            obj = Order.objects.get_or_create(
                order_id=event.data.code,
            )
            if event.type == "charge:confirmed":
                obj.status = STATUS_CHOICES.COMPLETED

            elif event.type == "charge:failed":
                obj.status = STATUS_CHOICES.FAILED

            obj.save()
        except (WebhookInvalidPayload, SignatureVerificationError) as e:
            return str(e), 400

    return HttpResponse()
