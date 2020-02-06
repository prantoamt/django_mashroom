from django.contrib import admin
from .models import Cart, CartItem, Area, District




class AreaAdmin(admin.ModelAdmin):
	list_display = ['area', 'district_name', 'charge']
	list_editable = ['district_name','charge']
	class Meta:
		model = Area

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Area, AreaAdmin)
admin.site.register(District)
