from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import Cart, CartItem, Area, District
from products.models import Product 
from orders.models import Coupon
from products.dict_key import dict_key
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

# First of checks if any cart is already created or not.
# The logic is, every cart is associated with session.
# If cart is not created/ seasion is over, new cart will be created.
def viewCart(request):
    print("view Cart")
    cart = None

    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    
    if the_id:                
        cart = Cart.objects.get(id=the_id)  ##If cart is already created, get the cart.

        if (cart.total < 0):   #This condition is to avoid to make the cart total negative
                cart.total = 0 # Everytime when the cart will be shown, this condition should e checked
        amount = cart.total
    
        if(amount==0):              ## If the cart is empty, push a empty message 
            cart.coupon_discount = 0
            massege = "Your cart is empty"
            context = {'cart':cart, 'empty': massege}         
            template = "cart/view.html"
            return render(request, template, context)
## The block below calculates the discounts per product and total percentage of discount
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
        print(District)        
        context = {'cart':cart,
                    'discount': discount,
                    'districts': District.objects.all()}
## The below else statement executes only if the cart is empty
    else:
        massege = "Your cart is empty"
        context = {'cart':cart, 'empty': massege}
             
    template = "cart/view.html"
    return render(request, template, context)



def update_cart(request, slug):
    request.session.set_expiry(120000)
    ##Check if the method
    try:
        qty = request.GET.get('qty')
        print("Quantity Got: ", qty)
        print("Slug Got: ", slug)
        update_qty = True
    except:
        qty = None
        update_qty = False

    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
        cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        print ("yeah")
    
    if update_qty and qty:

        if int(qty) == 0:
            cart_item.delete()

            if (cart.total < 0):
                cart.total = 0                    

        elif (qty == "102" and cart_item.product.stock > 0):
            cart_item.quantity += 1
            cart_item.save()

        elif (qty == "101" and cart_item.product.stock > 0):
            cart_item.quantity -=1

            if(cart_item.quantity==0):
                print("item", cart_item.quantity)
                cart_item.delete()
                request.session['item_count']=0
            else:
                cart_item.save()    

        else:
            if(cart_item.product.stock >= int(qty)):
                print("stk: ", cart_item.product.stock)
                cart_item.quantity = int(qty)
                cart_item.save()
            else:
                print("Out of stock");    
                response = JsonResponse({'out_of_stock': True,
                                'cart_item': request.session['item_count'],
                                'cart_total': cart.total,
                                'coupon_discount': cart.coupon_discount})
                return response

    else:
        pass
    

    new_total = 0.00
    for item in cart.cartitem_set.all():
        if (item.product.sale != item.product.price):
            line_total = float(item.product.sale)*item.quantity
            item.line_total = line_total
            item.save()
            new_total = new_total+ line_total
        else:
            line_total = float(item.product.price)*item.quantity
            item.line_total = line_total
            print(line_total)
            item.save()
            new_total = new_total+ line_total
    request.session['item_count'] = cart.cartitem_set.count()
    cart.total = float(new_total)
    cart.total = new_total - float(cart.coupon_discount)
    cart.save()

    if request.is_ajax():
        print(":ajax")
        response = JsonResponse({'cart_item': request.session['item_count'],
                                'cart_total': cart.total,
                                'coupon_discount': cart.coupon_discount})
        return response

    return HttpResponseRedirect(reverse("viewCart"))               


def coupon(request):
    print("Method name: Coupon")
    message = ""
    try:
        coupon_code = request.GET.get('cpn')
        print(coupon_code)
    except:
        coupon_code = None
        message = 'No Coupon Found'

    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        HttpResponseRedirect(reverse('viewCart'))

    if coupon_code:
        try:
            coupon_object = Coupon.objects.get(coupon_code=coupon_code)
            if(coupon_object.active):    
                cpn_discount = coupon_object.coupon_discount
                if(cart.total > 500):
                    if cart.coupon_discount == 0:
                        cart.coupon_discount = cpn_discount
                        cart.total = (cart.total) - (cart.coupon_discount)
                        cart.save()
                        message = 'Coupon applied'
                    else:
                        message = 'Coupon is already applied'        
                else:
                    message = 'You have to shop more than 500 taka to apply this coupon'
            else:
                message = 'No Coupon Found'        
        except:
            message = 'No Coupon Found'  
    response = JsonResponse({'message': message,
                            'cart_total': cart.total,
                            'coupon_discount': cart.coupon_discount})
    
    return response

        
##returns delivery charge and area name corresponding to each district
def getDeliveryCharge(request):
    if(request.is_ajax):
        district_name = request.GET.get('dst')
        district_id = District.objects.get(district_name=district_name).id
        areas = Area.objects.filter(district_name=district_id)
        area_charge = {}
        for item in range(0,len(areas)):
            area_charge[areas[item].area] = int(areas[item].charge)
        print(area_charge)                    
        response = JsonResponse(area_charge)
        return response



# def confirmOrder(request):
#     if(request.is_ajax):
#         try:
#             the_id = request.session['cart_id']
#             cart = Cart.objects.get(id=the_id)
#         except:
#             new_cart = Cart()
#             new_cart.save()
#             request.session['cart_id'] = new_cart.id
#             the_id = new_cart.id
#             cart = Cart.objects.get(id=the_id)


