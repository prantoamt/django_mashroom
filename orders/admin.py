from django.contrib import admin
from .models import Order, Coupon

class orderAdmin(admin.ModelAdmin):
        date_hierarchy = 'timestamp'
        search_fields = ['status']
        list_display = ['order_id', 'user', 'cart', 'sub_total', 'delivery_charge', 'coupon_discount', 'final_total', 'status']
        # list_editable = ['price', 'sale', 'stock', 'active']
        # list_filter = ['active', 'stock', 'price']
        readonly_fields = ['timestamp', 'updated']
        class meta:
            model = Order

    
# Register your models here.
admin.site.register(Order, orderAdmin)
admin.site.register(Coupon)