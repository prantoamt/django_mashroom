from datetime import datetime
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from products.dict_key import dict_key
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.urls import reverse
from carts.models import Cart
from .models import Order
from .utils import id_generator, render_to_pdf


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
            # ##Send email
            # subject = 'Mushroom Firm: Order confirmed'
            # from_email = settings.EMAIL_HOST_USER
            # to_email = [order.user.email, settings.EMAIL_HOST_USER] 
            # text_content = 'Dear '+ order.user.first_name + '\nYour order (order id: '+ order.order_id+' has been confirmed. Our Delivery man will contact with you soon. Thanks for being with us!'
            # htmly_content = get_template('order/invoice_email_template.html')
            # order_name = order.user.first_name + " " + order.user.last_name
            # context['order_id'] = order.order_id
            # context['bill_to'] = order_name
            # context['phone_no'] = order.phone_no
            # context['email'] = order.user.email
            # context['district'] = order.district
            # context['area'] = order.area
            # context['address'] = order.address
            # context['zipcode'] = order.zipcode
            # context['sub_total'] = order.sub_total
            # context['delivery_charge'] = order.delivery_charge
            # context['coupon_discount'] = order.coupon_discount
            # context['final_total'] = order.final_total
            # context['date'] = order.updated
            # context['payment_method'] = order.payment_method
            # cart = order.cart
            # context['cart'] = cart
            # pdf = render_to_pdf('order/invoice.html', context)
            # html_content = htmly_content.render(context)
            # message = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            # message.attach_alternative(html_content, "text/html")
            # message.send()
            context['msg'] = msg        
            return render(request, template, context)    
    return JsonResponse({'sd':3})            

@staff_member_required
def viewOrdersAdminInterface(request):
    orders = Order.objects.order_by('viewed', '-updated')
    template = 'order/order_admin.html'
    context = {'orders': orders}
    return render(request, template, context)    

@staff_member_required
def orderDetails(request, order_id):
    order = Order.objects.get(order_id=order_id)
    order.viewed = True
    order.save()
    template = 'order/order_admin_details.html'
    context = {'order': order}
    context['order_status'] = order.status
    print(order.status)
    return render(request, template, context)    

@staff_member_required
def generateInvoice(request, order_id):
        order = Order.objects.get(order_id=order_id)
        context = {}
        order_name = order.user.first_name + " " + order.user.last_name
        context['order_id'] = order.order_id
        context['bill_to'] = order_name
        context['phone_no'] = order.phone_no
        context['email'] = order.user.email
        context['district'] = order.district
        context['area'] = order.area
        context['address'] = order.address
        context['zipcode'] = order.zipcode
        context['sub_total'] = order.sub_total
        context['delivery_charge'] = order.delivery_charge
        context['coupon_discount'] = order.coupon_discount
        context['final_total'] = order.final_total
        context['date'] = order.updated
        context['payment_method'] = order.payment_method
        cart = order.cart
        context['cart'] = cart
        pdf = render_to_pdf('order/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Order_%s.pdf" %(context['order_id'])
            content = "inline; filename='%s'" %(filename)
            # download = request.GET.get("download")
            # if download:
            #     content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
        return response

@staff_member_required
def changeOrderStatus(request, order_id):
    if(request.POST):
        value = request.POST.get('dropdown')
        order = Order.objects.get(order_id=order_id)
        order.status = value
        order.save()
        template = 'order/order_admin_details.html'
        context = {'order': order}
        context['order_status'] = order.status
    return render(request, template, context)   