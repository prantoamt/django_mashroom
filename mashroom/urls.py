"""mashroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import products, home
from products.views import single
from carts.views import viewCart, update_cart, coupon, getDeliveryCharge
from orders.views import checkout
from account.views import loginView, logoutView, register
from orders.views import viewOrdersAdminInterface, confirmOrder
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

 
urlpatterns = [
    url(r'^$', home, name='home'),
    path('admin/', admin.site.urls),
    url(r'^products/$', products, name='products'),
    url(r'^products/(?P<slug>[\w-]+)/$', single, name='single_product'),
    url(r'^cart/$', viewCart, name='viewCart'),
    url(r'^cart/deliverycharge/$', getDeliveryCharge, name='delivery_charge'),
    url(r'^cart/(?P<slug>[\w-]+)/$', update_cart, name='update_cart'),
    url(r'^cart/coupon/code/$', coupon, name='coupon'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^accounts/login/$', loginView, name="login"),
    url(r'^accounts/logout/$', logoutView, name="logout"),
    url(r'^accounts/register/$', register, name="register"),
    url(r'^adminorder/$', viewOrdersAdminInterface, name="orders_admin"),
    url(r'^confirmorder/$', confirmOrder, name="confirm_order"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)