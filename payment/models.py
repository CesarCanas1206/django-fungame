from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class STATUS_CHOICES(models.TextChoices):
    INPROGRESS = "inprogress", "In Progress"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"


class PAYMENT_CHOICES(models.TextChoices):
    STRIPE = "stripe", "Stripe"
    COINBASE = "coinbase", "Coinbase"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")

    order_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES.choices, default=PAYMENT_CHOICES.STRIPE
    )
    amount = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    currency = models.CharField(max_length=10, default="USD")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.INPROGRESS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ["-id"]
