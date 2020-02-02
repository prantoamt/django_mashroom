from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from carts.models import Cart
from .models import Order
from .utils import id_generator
from django.contrib.auth.decorators import login_required
from products.dict_key import dict_key
# Create your views here.

@login_required(login_url='login')
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('viewCart'))
        
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order(cart=cart)
        new_order.user = request.user
        new_order.order_id = id_generator()
    except:
        HttpResponseRedirect(reverse('viewCart'))

    if new_order.status == "Finished":
        del request.session['cart_id']
        del request.session['item_count']
    ##Update order DB
    new_order.coupon_discount = cart.coupon_discount
    new_order.sub_total = cart.total + cart.coupon_discount
    new_subtotal = float(new_order.sub_total)
    new_delivery = float(new_order.delivery_charge)
    new_coupon = float(new_order.coupon_discount)
    raw_total = (new_subtotal + new_delivery) - new_coupon
    new_order.final_total = float(raw_total)
    new_order.save()

    discount = {}
    total_price = 0
    total_discount = 0
    cart_items =  cart.cartitem_set.all()
    for i in range(len(cart_items)):
        item = cart_items[i].product.id
        price = cart_items[i].product.price
        total_price = total_price+price
        sale = cart_items[i].product.sale
        less = price - sale
        total_discount = total_discount+less
        if(price > 0):
            discount[item] = int((less/price)*100)
        else:
            discount[item] = 0    
    if(total_price > 0):
        percent_discount = int((total_discount/total_price)*100)
    else:
        percent_discount = 0        
    discount["total_discount"] = percent_discount
    context = {
        'cart': cart,
        'order': new_order,
        'discount': discount}
    template = "order/order.html"
    return render(request, template, context)

    