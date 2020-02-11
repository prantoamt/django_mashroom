from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse, Http404
from django.urls import reverse
from carts.models import Cart
from .models import Order
from .utils import id_generator
from django.contrib.auth.decorators import login_required
from products.dict_key import dict_key

# Create your views here.

@login_required(login_url='login')
def checkout(request):
    if request.is_ajax: 
        if(request.GET):
            delivery_charge = request.GET.get('dlvry')
            sub_total = request.GET.get('sbtotal')
            district = request.GET.get('dst')
            area = request.GET.get('area')
            print(area)

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
        new_order.sub_total = float(sub_total)
        new_order.delivery_charge = float(delivery_charge)
        new_subtotal = float(new_order.sub_total)
        new_delivery = float(delivery_charge)
        new_coupon = float(new_order.coupon_discount)
        raw_total = (new_subtotal + new_delivery) - new_coupon
        new_order.final_total = float(raw_total)
        new_order.area = area
        new_order.district = district
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
    else:
        context = locals()        
    template = "order/order.html"
    return render(request, template, context)


@login_required(login_url='login')    
def confirmOrder(request):
    if(request.is_ajax):
        template = 'order/successfull_order.html'
        msg = "Something Went wrong. Please try again"
        context = {'msg': msg}
        if(request.GET):
            address = request.GET.get('adrs')
            phone = request.GET.get('phn')
            zipcode = request.GET.get('zip')
            payment_method = request.GET.get('paymnt')
            print(address)
            try:
                the_id = request.session['cart_id']
                cart = Cart.objects.get(id=the_id)
            except:
                the_id = None
                msg = "Something went wrong. Please logout and login then try again"
                return render(request, template, context)

            try:
                order = Order.objects.get(cart=cart)
                order.address = address
                order.zipcode = zipcode
                order.payment_method = payment_method
                order.phone_no = phone
                order.status = "Confirmed"
                for item in (order.cart.cartitem_set.all()):
                    item.product.stock = item.product.stock - item.quantity
                    item.product.save()
                order.save()
                del request.session['cart_id']
                del request.session['item_count']
            except:
                msg = "Something went wrong. Please logout and login then try again"
                return render(request, template, context)
            msg = 'Order has been placed successfully! Our customer care will contact with you soon' 
            context = {'msg': msg}        
            return render(request, template, context)    
    return JsonResponse({'sd':3})            

def viewOrdersAdminInterface(request):
    orders = Order.objects.all()
    for order in orders:
        cart = order.cart
        for item in cart.cartitem_set.all():
            print ("cart item:", item.quantity)
    template = 'order/order_admin.html'
    context = {'orders': orders}
    return render(request, template, context)    