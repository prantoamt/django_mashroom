from django.db import models
from carts.models import Cart
from django.contrib.auth import get_user_model



# Create your models here.

User = get_user_model()

STATUS_CHOICES = (
    ("Started", "Started"),
    ("Confirmed", "Confirmed"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
)

PAYMENT_CHOICES = (
    ("Cash in delivery", "Cash in delivery"),
    ("Bkash", "Bkash"),
    ("Rocket", "Rocket"),
)

class Order(models.Model):
    #add user
    user = models.ForeignKey(User, blank=True, null=True, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    #address
    order_id = models.CharField(max_length=120, default="ABC", unique=True)
    sub_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    delivery_charge = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    coupon_discount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=120, choices=PAYMENT_CHOICES, default="Cash in delivery")
    final_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

class Coupon(models.Model):
    coupon_code = models.CharField(max_length = 10, default="", unique = True)
    coupon_discount = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    coupon_count = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code
