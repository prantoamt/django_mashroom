from django.db import models
from products.models import Product

# Create your models here.
class Cart(models.Model):
    #items = models.ManyToManyField(CartItem, blank=True)
    coupon_name = models.CharField(max_length=120, default="", unique=True)
    coupon_discount = models.DecimalField(max_digits=100, decimal_places=2, default=0.00) 
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return "cart id %s" %(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    line_total = models.DecimalField(max_digits=1000, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.product_name    


class District(models.Model):
    district_name = models.CharField(max_length=120, default="", unique=True)

    def __str__(self):
        try:
            return str(self.district_name)
        except:
            print("Error")    

class Area(models.Model):
    district_name = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    area = models.CharField(max_length=120, default="", unique=True)
    charge = models.DecimalField(max_digits=10000, decimal_places=2, default=0.0)

    def __str__(self):
        try:
            return str(self.area)
        except:
            pass    