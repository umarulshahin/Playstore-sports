from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.cache import  never_cache,cache_control
from django.contrib.auth.decorators import login_required
from Admin_app.models import *
from user_app.models import *
from . models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
import re 
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import *
import uuid
import razorpay
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors     
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from datetime import datetime
import environ

env = environ.Env()


# Create your views here.

             # ................. Dashbord......................
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Dashbord(request):
    try:
        if 'phone' in request.session:
            return redirect("signup_otp")  
    
        pro=Product.objects.all()
    
        sub = Sub_Category.objects.filter(name__icontains="adidas").prefetch_related("product_set")
        out_of_stock =True
        context={
                'pro' : pro,
                'sub' : sub,
                'out_of_stock':out_of_stock
        }
        
        return render(request,'dashbord/dashbord.html',context)   
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
              

               # .................End Dashbord......................


               # ................. All Product......................
               
def All_Product(request):
    
    try:
        
        search=request.GET.get('search')     
        sub=request.GET.get('sub')   
        sort=request.GET.get('sorting',"")
        filter=request.GET.get('filter',"")
        page=request.GET.get('page',"")
        
        
        if not (sub and sort and filter):
            
            value=Product.objects.all()
            
        
       
            
        else:
            value=Product.objects.all()
        
        if search:
            value=Product.objects.filter(name__icontains=search)
            
        if filter and filter != "all":   
            
            value=value.filter(sub_category=int(filter))
            
        elif filter and filter == "all":
            
            value=Product.objects.all()
            
        if sort:
            
            value=value.order_by(sort)
        
        sub=Sub_Category.objects.all()     
        
        paginator=Paginator(value,2)
        pro=paginator.get_page(page)
            
        context={
                'pro' : pro,
                'sub' : sub
            }
            
        return render(request,'dashbord/all_product.html',context)
            
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)


        # ................. End All Product......................
               
         # .................SEARCH SUGGESTIONS......................
         
@require_GET   
@never_cache
def Suggestions(request):
    
    try:
        prefix = request.GET.get('prefix', '')
        suggestions = []
        products = Product.objects.filter(name__icontains=prefix)
        for product in products:
            suggestions.append(product.name)
        return JsonResponse({'suggestions': suggestions})
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)

               
               # ................. END SEARCH SUGGESTIONS......................
               
               #.................. VIEW PRODUCT..........................
               
@never_cache           
def View_Product(request,id):
    
    try:
        
        pro=get_object_or_404(Product,id=id)
        out_of_stock=Product_size.objects.filter(stock__gte=1,product=id)
        
        if not out_of_stock:
            stock=False
        else:
            stock=True
        relate=Product.objects.exclude(id=id)[:4]

        context={
            
            'pro' : pro,
            'relate' : relate,
            'stock' : stock,
        
        }
        
        return render(request,'dashbord/view_product.html',context)
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
               
               # ................. End View Product......................
               
                  # ................. USER PROFILE......................

@login_required(login_url='/user_app/Login/')
@never_cache
def User_Profile(request):
    
    try:
        
        if request.user.is_authenticated:
            
            user=CustomUser.objects.get(email=request.user)
            user_details = CustomUser.objects.get(id=user)
            
            context = {
                'user' : user_details,
            }
            
            return render(request,'dashbord/profile.html',context)
        
        return redirect("login")
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
                  
                     # .................END USER PROFILE......................
                     
                     # .................EDIT PROFILE......................
 
@login_required(login_url='/user_app/Login/')
@never_cache                    
def Edit_Profile(request,id):
    
    try:
        if request.method == "POST":
            
            username=request.POST.get("editFirstName")
            phone=request.POST.get("editphone")
            
            pattern = r'^[a-zA-Z0-9].*'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^(?!0{10}$)\d{10}$'
            
            if not (username  or phone ):
                messages.error(request, "please Fill Required Field")
                return redirect("user_profile")
            
            if not re.match(pattern,username):
                messages.error(request,"Please Enter Valid User Name")
                return redirect("user_profile")
            
            
            elif not re.match(pattern_Phone,phone):
                messages.error(request,"Please enter valid Phone number")
                return redirect("user_profile")
                    
            
            CustomUser.objects.filter(id=id).update(username=username,ph_no=phone)
            
            return redirect("user_profile")
            
        return redirect('user_profile')   
            
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
    
                     # .................END EDIT PROFILE......................
                     
                     
                      # .................ADDRESS AND ADD ADDRESS......................
                     
@login_required(login_url='/user_app/Login/')
@never_cache                
def Addresses(request):    
    
    try:
        
        if request.user.is_authenticated:
            
            try:
                user=CustomUser.objects.get(email=request.user)
                
                value=User_Address.objects.filter(customuser=user.id)
                
                context={
                    
                    'value' : value
                }
            
            
                return render(request,'dashbord/address.html',context)
            
            except Exception as e:
                
                return render(request,'dashbord/address.html')
                
        return redirect('user_profile')
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)

         # .................END ADDRESS AND ADD ADDRESS......................
         
          # ................. ADD ADDRESS......................
 
@login_required(login_url='/user_app/Login/')
@never_cache          
def Add_Address(request):
    
    try:
        
            if request.user.is_authenticated:
            
                user=CustomUser.objects.get(email=request.user)
                
                if request.method == "POST":
                
                        name=request.POST.get("name")
                        email=request.POST.get("email")
                        phone=request.POST.get("phone")
                        house=request.POST.get("house")
                        street=request.POST.get("street")
                        city=request.POST.get("city")
                        state=request.POST.get("state")
                        country=request.POST.get("country")
                        pin_code=request.POST.get("pin_code")
                        location=request.POST.get("location")
                        
                        
                        pattern = r'^[a-zA-Z0-9].*'
                        pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        pattern_Phone= r'^(?!0{10}$)\d{10}$'
                            
                        if not (name or email or phone or house or street or city or country or pin_code or location):
                                messages.error(request, "please Fill Required Field")
                                return redirect("addresses")
                            
                        if not all(re.match(pattern, value) and value.strip() for value in [name, email, phone, house, street, city,country, state, pin_code, location,]):
                                messages.error(request, "Please Enter Valid values")
                                return redirect("addresses")
                            
                        elif not re.match(pattern_email,email):
                                messages.error(request,"Please enter valid email address")
                                return redirect("addresses")
                            
                            
                        elif not re.match(pattern_Phone,phone):
                                messages.error(request,"Please enter valid Phone number")
                                return redirect("addresses")
                            
                        
                        value=CustomUser.objects.get(id=user.id)
                        
                        
                        User_Address.objects.create(
                            
                            name=name,
                            email=email,
                            phone=phone,
                            house=house,
                            street=street,
                            city=city,
                            state=state,
                            country=country,
                            pin_code=pin_code,
                            location=location,
                            customuser= value,            
                                                    )
                
                
                        return redirect("addresses")
                
                
                return redirect("addresses")
            return redirect('login')
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
           # .................END ADD ADDRESS......................
         
         # .................DELETE ADDRESS......................
         
         
@login_required(login_url='/user_app/Login/')
@never_cache
def Delete_Address(request,id):
    
    try:
        
        if id:
           
           User_Address.objects.filter(id=id).delete()
           
           
           return redirect("addresses")
        
        return redirect("addresses")
        
        
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)  
    
         # .................END DELETE ADDRESS......................
         
         # .................EDIT ADDRESS......................
         
@login_required(login_url='/user_app/Login/')
@never_cache
def Edit_Address(request):
    
    try:
            
        if request.method == "POST" :
            
                E_name=request.POST.get("editName")
                E_email=request.POST.get("editEmail")
                E_phone=request.POST.get("editphone")
                E_house=request.POST.get("editHouse")
                E_street=request.POST.get("editStreet")
                E_city=request.POST.get("editcity")
                E_state=request.POST.get("editstate")
                E_country=request.POST.get("editcountry")
                E_pin_code=request.POST.get("editpin_code")
                E_location=request.POST.get("editlocation")
                address_id = request.POST.get('editid')
                
                pattern = r'^[a-zA-Z0-9].*'
                pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                pattern_Phone= r'^(?!0{10}$)\d{10}$'
                    
                if not (E_name or E_email or E_phone or E_house or E_street or E_city or E_country or E_pin_code or E_location):
                        messages.error(request, "please Fill Required Field")
                        return redirect("addresses")
                    
                if not all(re.match(pattern, value) and value.strip() for value in [E_name, E_house, E_street, E_city, E_country, E_pin_code, E_location]):
                        messages.error(request,"Please Enter Valid values")
                        return redirect("addresses") 
                    
                elif not re.match(pattern_email,E_email):
                        messages.error(request,"Please enter valid email address")
                        return redirect("addresses")
                    
                    # elif CustomUser.objects.filter(email=email).exists():
                    #     messages.error(request,"Email already exists")
                    #     return render(request,'dashbord/profile.html')
                    
                elif not re.match(pattern_Phone,E_phone):
                        messages.error(request,"Please enter valid Phone number")
                        return redirect("addresses")
                    
                
            
                User_Address.objects.filter(id=address_id).update(name=E_name,
                                                    email=E_email,
                                                    phone=E_phone,
                                                    house=E_house,
                                                    street=E_street,
                                                    city=E_city,
                                                    state=E_state,
                                                    country=E_country,
                                                    pin_code=E_pin_code,
                                                    location=E_location
                                                    )
            

        return redirect("addresses")
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
         
         # .................END EDIT ADDRESS......................
         
         # .................ADD TO CART......................

@never_cache   
def Add_to_Cart(request):
    
    try:
        
        if request.user.is_authenticated:
        
            if request.method == "POST":
            
            
                pro_id=request.POST.get('product_id')
                pro_size=request.POST.get('product_size')
                product = Product.objects.get(id=pro_id)
                
                product_check = Product.objects.get(id=pro_id)
                
              
                if (pro_size):
                        if(product_check):
                            
                            if Cart.objects.filter(customuser=request.user,product=pro_id,size=pro_size).exists():
                                
                                return JsonResponse({'status' :"Product already in  Cart"})
                            else:
                                
                                pro_qty=request.POST.get('product_qty')
                            
                                s_dis=0
                                if not product_check.offer_price or product_check.offer_price<=0:
                                    
                               
                                    total= int(product_check.price) * int(pro_qty)
                                    offer_price=int(product_check.offer_price)
                                    
                                     #  SUB CATEGORY OFFER ADDING........................
                                     
                                    today = datetime.today().date()
                                    sub=Sub_Category.objects.filter(offer__isnull=False,offer__end_date__gte=today,).prefetch_related('offer')
                                    sub=sub.filter(is_deleted=True)
                                       
                                    if product_check.sub_category in sub:
                                        
                                        sub_id=product_check.sub_category.id
                                        sub_data=Sub_Category.objects.filter(id=sub_id).prefetch_related('offer')
                                        for off in sub_data:
                                            dis=0
                                            sub_off=Offer.objects.get(id=off.offer.id)
                                            dis = (product_check.price * sub_off.discount)/100
                                            dis = (dis * int(pro_qty))
                                            s_dis += dis
                                    
                                            offer_price = int(product_check.price) - s_dis
                                            total= int(offer_price) * int(pro_qty)
                                            
                                    #  END SUB CATEGORY OFFER ADDING........................
                                   
                                else:
                                    
                                    total= int(product_check.offer_price) * int(pro_qty)
                                    offer_price=int(product_check.offer_price)
                                   
                                Cart.objects.create(customuser=request.user,
                                                    product=product,
                                                    size=pro_size,
                                                    qty=pro_qty,
                                                    price=int(product_check.price),
                                                    offer_price=offer_price,
                                                    total_price=total)
                                
                                if Wishlist.objects.filter(product=pro_id,customuser=request.user).exists():
                                    
                                    Wishlist.objects.get(product=pro_id,customuser=request.user).delete()
                              
                                return JsonResponse({'status' :"Product added successfully"})

                            
                        else:
                            return JsonResponse({'status' :"No such product found"})
                else:
                    
                    return JsonResponse({'status' :"Please select Your Size"})
                    
                            
        else:
                    
            return JsonResponse({'status' :"Login to Continue"})
           
                
            
        
        return redirect("view_product") 
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)

         # .................END ADD TO CART......................
         
         
          # .................User CART......................
          
@login_required(login_url='/user_app/Login/')
@never_cache          
def User_Cart(request):
    
    try:
        
        if request.user.is_authenticated:
        
                cart=Cart.objects.filter(customuser=request.user)
                
                sub=request.session.get("sub_total")
                
                if not sub :
                    sub_total=0
                    for i in cart:
                    
                        sub_total += int(i.total_price)
                    request.session["sub_total"]=sub_total
                    sub=request.session.get("sub_total")
                else:
                    sub_total=0
                    for i in cart:
                    
                        sub_total += int(i.total_price)
                    request.session["sub_total"]=sub_total
                    sub=request.session.get("sub_total")
                    
                    
                
                context={
                    
                    'cart':cart,
                    'sub_totel' : sub,
                }
                
                
                
                return render(request,'dashbord/cart.html',context)
        return redirect('login')
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
           # .................END USER CART......................
           
           
           # .................UPDATE AND STOCK MANAGE, TOTAL PRICE, SUB_TOTAL  CART......................
           
@never_cache
@require_POST
@login_required(login_url='/user_app/Login/')
@never_cache
def update_quantity_view(request):
    
    try:
        
        if request.method == 'POST':
        
            cart_item_id = request.POST.get('cartItemId')
            new_quantity = int(request.POST.get('newQuantity'))
            
            if "sub_total" in request.session:
                
                del request.session["sub_total"]
            
            cart_item = get_object_or_404(Cart, id=cart_item_id)
            
            stock=Product_size.objects.get(size=cart_item.size,product=cart_item.product)
            
            if stock is not None and new_quantity > stock.stock and stock.stock == 0:
            
                return JsonResponse({'error': f'Not enough stock available. Current stock: {stock.stock}'}, status=400)
        
            if not cart_item.offer_price or cart_item.offer_price <= 0:
            
                total=int(cart_item.price) * int(new_quantity)
               
            else:
                
                total=int(cart_item.offer_price) * int(new_quantity)
        
            
            if stock.stock >= new_quantity :
                
                
                    request.session['qty']={new_quantity:cart_item_id}
                    cart_item.qty = new_quantity
                    cart_item.total_price = total
                    cart_item.save()
                    
                    total_item=Cart.objects.filter(customuser=request.user)
                    sub_total = 0
                    
                    for i in total_item:
                        
                        sub_total += int(i.total_price)
                    
                    
                    cart_subtotal=request.session["sub_total"]=sub_total
                    
                    current_stock=stock.stock
                    
                    return JsonResponse({'success': True,'total_price': total,'cart_subtotal2w': cart_subtotal,'current_stock': current_stock})
                
            
            # elif  new_quantity <= request.session.get('qty'):    
                
                    
            #         request.session['qty']=new_quantity
            #         cart_item.qty = new_quantity
            #         cart_item.total_price = total
            #         cart_item.save()
                    
            #         total_item=Cart.objects.filter(customuser=request.user)
            #         sub_total = 0
                    
            #         for i in total_item:
                        
            #             sub_total += int(i.total_price)
                    
                    
            #         cart_subtotal=request.session["sub_total"]=sub_total
                    
            #         current_stock=stock.stock
                    
            #         return JsonResponse({'success': True,'total_price': total,'cart_subtotal2w': cart_subtotal,'current_stock': current_stock})
                
            else:
                
                
                total_item=Cart.objects.filter(customuser=request.user)
                sub_total = 0
                    
                for i in total_item:
                        
                    sub_total += int(i.total_price) 
                cart_subtotal=request.session["sub_total"]=sub_total
                return JsonResponse({'error': f'Not enough stock available. Current stock: {stock.stock}'}, status=400)
            
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
        
         # ................. END UPDATE AND STOCK MANAGE, TOTAL PRICE, SUB_TOTAL  CART......................
         
          # .................DELETE PRODUCT FROM CART......................
        
    
@login_required(login_url='/user_app/Login/')
@never_cache
def Delete_Cart(request,product_id):
    
    try:
        
        value=Cart.objects.get(id=product_id)
        
        if "sub_total" in request.session:
        
            sub=request.session.get("sub_total")
            
            sub_total=  int(sub) - int(value.total_price)
            
            if "sub_total" in request.session:
                del request.session["sub_total"]
                

            request.session["sub_total"]=sub_total
            value.delete()
        
        return redirect('user_cart')
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
    
       # .................END DELETE PRODUCT FROM CART......................
       
        # .................CHECKOUT......................
        
@login_required(login_url='/user_app/Login/')
@never_cache       
def Checkout(request):
    
    
    try:
        
        if  request.user.is_authenticated:       
              
                value=Cart.objects.filter(customuser=request.user)
                for i in value:
                    
                    pro=Product_size.objects.filter(product=i.product,size=i.size)
                    
                    for j in pro:
                        
                        if j.stock < i.qty:
                            
                            messages.error(request,f"{i.product.name} stock not enough ")
                            return redirect("user_cart")
                        
                    
                user=request.user
                value=Cart.objects.filter(customuser=user)
                total=request.session.get("sub_total")
                address=User_Address.objects.filter( customuser=user)
              
                sub_total=0
                for j in value:
                    
                    sub_total += j.price * j.qty
                   
                discount=0            
                for i in value:
                    
                    if i.offer_price >= 1:
                        
                      dis=i.price - i.offer_price
                      discount += dis * i.qty
                cou=None      
                if request.method == "POST":
          
                    coupon_id=request.POST.get("coupon_id")
                    
                    if coupon_id:
                        
                        cou=Coupon.objects.get(id=coupon_id)
                        total-=cou.discount
                        request.session["coupon_id"]=coupon_id
                        
                    else:
                        request.session["coupon_id"]=None
                        
                coupon=Coupon.objects.filter(is_delete=True)
                valid=[]
                for i in coupon:
                    
                    if User_Coupon.objects.filter(customuser=request.user,coupon=i.id).exists():
                        pass
                    
                    elif i.offer_valid_amount <= sub_total:
                        
                        valid.append(i)
                
                key = env('RAZORPAY_KEY_ID')
                context={
                    
                    'value' :value,
                    'total':total,
                    'address' : address,
                    'discount' : discount,
                    'sub_total' : sub_total,
                    'coupon' : valid,
                    'coupon_amount' : cou,
                    'key' : key
                }
                
                
                return render(request,'dashbord/checkout.html',context)
        return redirect('login')
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
        # .................END CHECKOUT......................
        
        
        # ................. EDIT CHECKOUT ADDRESS......................
        
@login_required(login_url='/user_app/Login/')
@never_cache
def Checkout_Edit_Address(request):
    
    
    try:
        
          if request.method == "POST" :
        
            E_name=request.POST.get("editName")
            E_email=request.POST.get("editEmail")
            E_phone=request.POST.get("editphone")
            E_house=request.POST.get("editHouse")
            E_street=request.POST.get("editStreet")
            E_city=request.POST.get("editcity")
            E_state=request.POST.get("editstate")
            E_country=request.POST.get("editcountry")
            E_pin_code=request.POST.get("editpin_code")
            E_location=request.POST.get("editlocation")
            address_id = request.POST.get('editid')
            
 
            pattern = r'^[a-zA-Z0-9].*'
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            pattern_Phone= r'^(?!0{10}$)\d{10}$'
                
            if not (E_name or E_email or E_phone or E_house or E_street or E_city or E_country or E_pin_code or E_location):
                    messages.error(request, "please Fill Required Field")
                    return redirect("checkout")
                
            if not all(re.match(pattern, value) and value.strip() for value in [E_name, E_house, E_street, E_city, E_country, E_pin_code, E_location]):
                    messages.error(request,"Please Enter Valid values")
                    return redirect("checkout") 
                
            elif not re.match(pattern_email,E_email):
                    messages.error(request,"Please enter valid email address")
                    return redirect("checkout")
                
                # elif CustomUser.objects.filter(email=email).exists():
                #     messages.error(request,"Email already exists")
                #     return render(request,'dashbord/profile.html')
                
            elif not re.match(pattern_Phone,E_phone):
                    messages.error(request,"Please enter valid Phone number")
                    return redirect("checkout")
                
            
        
            User_Address.objects.filter(id=address_id).update(name=E_name,
                                                  email=E_email,
                                                  phone=E_phone,
                                                  house=E_house,
                                                  street=E_street,
                                                  city=E_city,
                                                  state=E_state,
                                                  country=E_country,
                                                  pin_code=E_pin_code,
                                                  location=E_location
                                                  )
        

            return redirect("checkout")
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
    
        # .................END EDIT CHECKOUT ADDRESS......................
        
        
        # .................ADD CHECKOUT ADDRESS......................
        
@login_required(login_url='/user_app/Login/')
@never_cache   
def Checkout_Add_Address(request):
    
    try:
                
            if request.user.is_authenticated:
            
            
                user=CustomUser.objects.get(email=request.user)
                
                if request.method == "POST":
                
                        name=request.POST.get("name")
                        email=request.POST.get("email")
                        phone=request.POST.get("phone")
                        house=request.POST.get("house")
                        street=request.POST.get("street")
                        city=request.POST.get("city")
                        state=request.POST.get("state")
                        country=request.POST.get("country")
                        pin_code=request.POST.get("pin_code")
                        location=request.POST.get("location")
                        
                        pattern = r'^[a-zA-Z0-9].*'
                        pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        pattern_Phone= r'^(?!0{10}$)\d{10}$'
                            
                        if not (name or email or phone or house or street or city or country or pin_code or location):
                                messages.error(request, "please Fill Required Field")
                                return redirect("checkout")
                            
                        if not all(re.match(pattern, value) and value.strip() for value in [name, email, phone, house, country, state, street , city, pin_code, location]):
                                messages.error(request,"Please Enter Valid values")
                                return redirect("checkout") 
                            
                        elif not re.match(pattern_email,email):
                                messages.error(request,"Please enter valid email address")
                                return redirect("checkout")
                            
                            # elif CustomUser.objects.filter(email=email).exists():
                            #     messages.error(request,"Email already exists")
                            #     return render(request,'dashbord/profile.html')
                            
                        elif not re.match(pattern_Phone,phone):
                                messages.error(request,"Please enter valid Phone number")
                                return redirect("checkout")
                            
                        
                        value=CustomUser.objects.get(id=user.id)
                        
                        
                        User_Address.objects.create(
                            
                            name=name,
                            email=email,
                            phone=phone,
                            house=house,
                            street=street,
                            city=city,
                            state=state,
                            country=country,
                            pin_code=pin_code,
                            location=location,
                            customuser= value,
                                                    
                                                    
                                                    )
                
                
                        return redirect("checkout")
                
                
                return redirect("checkout")
            return redirect("login")
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
        # .................END ADD CHECKOUT ADDRESS......................
        
        
        # .................USER ORDER......................
        
@login_required(login_url='/user_app/Login/')
@never_cache     
def User_Order(request):
    
    try:

        
        if  request.user.is_authenticated:
            
            if request.method == 'POST':
                
                user=int(CustomUser.objects.get(email=request.user))
                user_id=CustomUser.objects.get(id=user)
            
                address=request.POST.get('address')
                payment_method=request.POST.get('paymentMethod')
                total=Cart.objects.filter(customuser=user_id).aggregate(total=Sum('total_price'))
                

                address=User_Address.objects.filter(id=address)
                for j in address:
                    user_add={'name' :j.name , 'email' : j.email, 'phone' : j.phone, 
                            'house' :j.house, 'street': j.street, 'city': j.city, 
                            'state':j.state, 'country':j.country, 'pin_code':j.pin_code,
                            'location': j.location} 
                    
                    
                # ..................stock rechecking.................
                
                
            
                value=Cart.objects.filter(customuser=request.user)
                for i in value:
                        
                        pro=Product_size.objects.filter(product=i.product,size=i.size)
                        
                        for j in pro:
                            if j.stock < i.qty:
                                
                                messages.error(request,f"{i.product.name} out stock please choose any another product")
                                return redirect("user_cart")
                            
                            # ........... CASH ON DELIVERY ............
                            
                coupon_id=request.session.get("coupon_id")
                
              
                if  payment_method == 'cashOnDelivery' and address:    
                    
                    valid_amount=0
                    discount=0
                    # for i in value:
                                                        
                    #         for j in pro:
                                                    
                    #             if j.stock >= i.qty:
                                                            
                    #                 new_stock=j.stock-i.qty
                    #                 Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                                    
                                    # ..................... Coupen Cheking......................
                    print(user_id)    
                    if coupon_id:
                                      
                        coupon=Coupon.objects.filter(id=coupon_id)
                        for coupon in coupon:
                            
                            total['total']-=coupon.discount      
                            valid_amount=coupon.offer_valid_amount
                            discount=coupon.discount
                            
                            User_Coupon.objects.create(customuser=user_id,
                                                        coupon=coupon)
                                                
                                    
                        #    ...............order_id genarating.............                
                                        
                    unique_id = uuid.uuid4()
                    order_id = str(unique_id)[:8]
                                
                     # ..................order creating.................
                                        
                    print(user_id) 
                    Order.objects.create(user = user_id,
                                         user_address =user_add,
                                         total_amount = total['total'],
                                         payment_type = payment_method,
                                         order_id = order_id ,
                                         coupon_valid_amount = valid_amount,
                                         coupon_discount=discount
                                                            )
                                    
                    id=Order.objects.get(order_id=order_id)
                    value=Cart.objects.filter(customuser=user_id)
                    request.session['order_id']=id.id
                                        
                    for i in value:                
                                                                    
                        Order_Items.objects.create(order=id,
                                                product=i.product,
                                                Sub_Category=i.product.sub_category,
                                                qty=i.qty,
                                                size=i.size,
                                                price=i.price,
                                                offer_price=i.offer_price,
                                                total_price=i.total_price)
                        
                        #.............. stock updating...............
                        
                    for i in value:
                                                            
                        for j in pro:
                                                        
                          if j.stock >= i.qty:
                                                                
                                new_stock=j.stock-i.qty
                                Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                                            
                                        
                    Cart.objects.filter(customuser=user_id).delete()
                    request.session['coupon_id']=None
            
                    return redirect('confirmation')
                
                # ..................... Wallet Payment .........................
                
                                
                elif  payment_method == "wallet" and address:
                        
                                
                            id=int(CustomUser.objects.get(email=request.user))
                            user=CustomUser.objects.get(id=id)
                            total=Cart.objects.filter(customuser=user).aggregate(total=Sum('total_price'))
                            
                            total=int(total['total'])
                            
                            
                                     # ...................Wallet Balance cheking....................
                            if int(user.wallet_bal) > total:
                                    
                                    
                                    #........................ coupon cheking...........
                            
                                valid_amount=0
                                discount=0
                                if coupon_id:
                                    
                                    coupon=Coupon.objects.filter(id=coupon_id)
                                    for coupon in coupon:
                                
                                        total-=coupon.discount      
                                        valid_amount=coupon.offer_valid_amount
                                        discount=coupon.discount
                                        
                                        User_Coupon.objects.create(customuser=user,
                                                                    coupon=coupon)
                    #    ...............order_id genarating.............                
                                            
                                unique_id = uuid.uuid4()
                                order_id = str(unique_id)[:8]    
                                
                    # ..................order creating.................
                                            
                                print(user_id) 
                                Order.objects.create(user = user,
                                                    user_address =user_add,
                                                    total_amount = total,
                                                    payment_type = payment_method,
                                                    order_id = order_id ,
                                                    coupon_valid_amount = valid_amount,
                                                    coupon_discount=discount
                                                                        )  
                                id=Order.objects.get(order_id=order_id)
                                value=Cart.objects.filter(customuser=user_id)
                                request.session['order_id']=id.id
                                
                                for i in value:               
                                        
                                    Order_Items.objects.create(order=id,
                                                            product=i.product,
                                                            Sub_Category=i.product.sub_category,
                                                            qty=i.qty,
                                                            size=i.size,
                                                            price=i.price,
                                                            offer_price=i.offer_price,
                                                            total_price=i.total_price)
                                
                                #................... wallet amount reduct.................
                                
                                user.wallet_bal -= int(total)
                                user.save()
                                Wallet_Transactions.objects.create(customuser = user,
                                                                   amount = total,
                                                                   resons = 'shopping',
                                                                   add_or_pay = 'pay'
                                                                     
                                                                   )
                                
                                #............................ stock update ...............
                                
                                for i in value:
                                                                        
                                    for j in pro:
                                                                    
                                        if j.stock >= i.qty:
                                                                            
                                            new_stock=j.stock-i.qty
                                            Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                                                       
                                                    
                                Cart.objects.filter(customuser=user_id).delete()
                                request.session['coupon_id']=None
                        
                                return redirect('confirmation')                  
                                        
                            
                            else:
                                
                                messages.error(request,f" Your Wallet is insufficient Please choose any another Payment method")
                                return redirect("checkout")
                              
                              
                 
                 
                 
                              #..........................Upi Payment ...........................
                              
                if request.method == "POST":    
                        
                        payment_method=request.POST.get("payment_mode")
                        address_id=request.POST.get("address_id")
                       
                        if payment_method == "paid by Razorpay":
                    
                            address=User_Address.objects.filter(id=address_id)
                            for j in address:
                                user_add={'name' :j.name , 'email' : j.email, 'phone' : j.phone, 
                                        'house' :j.house, 'street': j.street, 'city': j.city, 
                                        'state':j.state, 'country':j.country, 'pin_code':j.pin_code,
                                        'location': j.location} 
                                
                                # .................stock checking ............
                  
                            value=Cart.objects.filter(customuser=request.user)
                            for i in value:
                                    
                                    pro=Product_size.objects.filter(product=i.product,size=i.size)
                                    
                                    for j in pro:
                                        
                                        if j.stock < i.qty:
                                            
                                            messages.error(request,f"{i.product.name} out stock please choose any another product")
                                            return redirect("user_cart")
                        
                                        # .................stock Updatin ............
                                        
                            # value=Cart.objects.filter(customuser=request.user)
                            # for i in value:
                                
                            #     pro=Product_size.objects.filter(product=i.product,size=i.size)
                                                        
                            #     for j in pro:
                                                            
                            #         if j.stock >= i.qty:
                                                                    
                            #                 new_stock=j.stock-i.qty
                            #                 Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                   
                            valid_amount=0
                            discount=0                                       
                            if coupon_id:
                                      
                                coupon=Coupon.objects.filter(id=coupon_id)
                                for coupon in coupon:
                                    
                                    total['total']-=coupon.discount
                                                        
                                    valid_amount=coupon.offer_valid_amount
                                    discount=coupon.discount
                            
                                    
                                    User_Coupon.objects.create(customuser=user_id,
                                                coupon=coupon)
                             
                                                
                             #    ...............order_id genarating.............
                                                
                                                
                            unique_id = uuid.uuid4()
                            order_id = str(unique_id)[:8]
                                   
                            # ..................order creating.................
                                                
                                                
                            Order.objects.create(user = user_id,
                                                user_address =user_add,
                                                total_amount = total['total'],
                                                payment_type = payment_method,
                                                order_id = order_id ,
                                                coupon_valid_amount = valid_amount,
                                                coupon_discount=discount
                                                                
                                                                    )
                                     
                            id=Order.objects.get(order_id=order_id)
                            value=Cart.objects.filter(customuser=user_id)
                                            
                            request.session['order_id']=id.id
                                            
                                           
                       
                            for i in value:
                                                
                                Order_Items.objects.create(order=id,
                                                        product=i.product,
                                                        Sub_Category=i.product.sub_category,
                                                        qty=i.qty,
                                                        size=i.size,
                                                        price=i.price,
                                                        offer_price=i.offer_price,
                                                        total_price=i.total_price)
                                                
                                    # .................stock Updatin ............
                                
                            value=Cart.objects.filter(customuser=request.user)
                            for i in value:
                                
                                pro=Product_size.objects.filter(product=i.product,size=i.size)
                                                        
                                for j in pro:
                                                            
                                    if j.stock >= i.qty:
                                                                    
                                            new_stock=j.stock-i.qty
                                            Product_size.objects.filter(product=i.product,size=i.size).update(stock=new_stock)
                                                
                                            
                                            Cart.objects.filter(customuser=user_id).delete()
                                            request.session['coupon_id']=None
                                    
                                            return redirect('confirmation')
                                            
                                    else:
                                        
                                        messages.error(request,f"{i.product.name} out stock please choose any another product")
                                        return redirect("user_cart")
                        else:
                            
                            messages.error(request,f"Select any Address ")
                            return redirect("checkout")      
                    
                
                else:
                            
                            return redirect("checkout")
                        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)                       
        
        # ................. END USER ORDER ......................
        
        
        # ................. ORDER CONFIRMATION ..................
        
@never_cache       
def Confirmation(request):
    
    try:
                
            id=str(request.session.get('order_id'))
            
            order=Order.objects.get(id=id)
            item=Order_Items.objects.filter(order=id)
            
            pairs = order.user_address.strip('{}').split(',')

            # Create a dictionary from the key-value pairs
            my_dict = {}
            for pair in pairs:
                key, value = pair.split(':')
                my_dict[key.strip(" '")] = value.strip(" '")
            
            context={
                'order' : order,
                'item' : item,
                'house' : my_dict['house'],
                'street' : my_dict['street'],
                'city' : my_dict['city'] ,
                'country' : my_dict['country'] 
            }
            
            
            return render(request,'dashbord/confirmation.html',context)
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)

       # .................END ORDER CONFIRMATION ......................
       
       
       # .................MY ORDER ......................
@login_required(login_url='/user_app/Login/')
@never_cache    
def My_Order(request):
    
    try:
            user=CustomUser.objects.get(email=request.user)
            order=Order.objects.filter(user_id=user.id)
            
            
            if order:
                addresses=[]
                for i in order:
                    
                    pairs = i.user_address.strip('{}').split(',')        
                    my_dict = {}
                    for pair in pairs:
                        key, value = pair.split(':')
                        my_dict[key.strip(" '")] = value.strip(" '")
                        
                        address = {'house': my_dict.get('house', ''),
                        'street': my_dict.get('street', ''),
                        'city': my_dict.get('city', ''),
                        'country': my_dict.get('country', ''),
                        'pin_code': my_dict.get('pin_code', ''),
                        'location': my_dict.get('location', ''),
                        'phone': my_dict.get('phone', ''),
                        'name': my_dict.get('name', ''),
                    }
                    
                    addresses.append({ 'address': address})
                    value=zip(order,addresses)
                    context={
                            
                        'value':value
                        
                        }
                
                return render(request,'dashbord/my_order.html',context)
            
            return render(request,'dashbord/my_order.html')
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
       
       # .................END MY ORDER ......................
       
       # ................. ORDER DETAILS......................
       
@login_required(login_url='/user_app/Login/')
@never_cache   
def Order_Details(request,id):
    
    try:
            order=Order.objects.get(id=id)
            item=Order_Items.objects.filter(order_id=id)
                
            context={
                'order' : order,
                'item' : item,
            }
            
            return render(request,'dashbord/order_details.html',context)
    except TypeError:
        return render(request,'dashbord/user_404.html')
       
       # .................END ORDER DETAILS......................
       
       # .................ORDER CANCELLATION......................
@login_required(login_url='/user_app/Login/')
@never_cache
def Cancellation(request,id):
    
    try:
                
            order=Order.objects.get(id=id)
            date=timezone.now()
            if order:
            
                if order.payment_type == 'cashOnDelivery' :
                    user_order=Order_Items.objects.filter(order_id=id)
                    for i in user_order:
                        
                        
                        stock=Product_size.objects.get(product=i.product,size=i.size)
                        
                        stock.stock += i.qty
                        stock.save()
                    
                    if order.status == "delivered":
                        
                        user=CustomUser.objects.get(id=order.user)
                        user.wallet_bal = int(user.wallet_bal) + int(order.total_amount)
                        user.save()
                        Wallet_Transactions.objects.create(customuser = user,
                                                        amount= order.total_amount,
                                                        resons= 'order Cancellation',
                                                        add_or_pay = 'add',               
                                                        )
                        
                    order.status= 'cancelled'
                    order.status_date=date
                    order.save()
                    
                    
                    
                elif order.payment_type == 'paid by Razorpay' :
                    user_order=Order_Items.objects.filter(order_id=id)
                    for i in user_order:
                        
                        
                        stock=Product_size.objects.get(product=i.product,size=i.size)
                        
                        stock.stock += i.qty
                        stock.save()
                
                   
                    
                 #  .......................... Order Amount Add To Wallet....................
                 
                    user=CustomUser.objects.get(id=order.user)
                    user.wallet_bal = int(user.wallet_bal) + int(order.total_amount)
                    user.save()
                    Wallet_Transactions.objects.create(customuser = user,
                                                       amount= order.total_amount,
                                                       resons= 'order Cancellation',
                                                       add_or_pay = 'add',               
                                                       )
                    order.status= 'refunded'
                    order.status_date=date
                    order.save()
                    
                    
                elif order.payment_type == "wallet" :
                    
                    user_order=Order_Items.objects.filter(order_id=id)
                    for i in user_order:
                        
                        
                        stock=Product_size.objects.get(product=i.product,size=i.size)
                        
                        stock.stock += i.qty
                        stock.save()
                
                   
                    
                 #  .......................... Order Amount Add To Wallet....................
                 
                    user=CustomUser.objects.get(id=order.user)
                    user.wallet_bal += int(order.total_amount)
                    user.save()
                    Wallet_Transactions.objects.create(customuser = user,
                                                       amount= order.total_amount,
                                                       resons= 'order Cancellation',
                                                       add_or_pay = 'add',               
                                                       )
                    order.status= 'refunded'
                    order.status_date=date
                    order.save()
         
                    
            return redirect('my_order')
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
       # .................END ORDER CANCELLATION......................
       
       
       # .................RAZORPAY......................
       
@never_cache
def Pay_With_Upi(request):
       
        try:
       
            user=int(CustomUser.objects.get(email=request.user))
            user_id=CustomUser.objects.get(id=user)
          
          
            total=Cart.objects.filter(customuser=user_id).aggregate(total=Sum('total_price'))
            
            
            
            coupon_id=request.session.get("coupon_id")
            total=total['total']   
            if coupon_id:
                
                coupon=Coupon.objects.get(id=coupon_id)
                total-=coupon.discount
                
                
            # .........stock cheking ...........
            
            value=Cart.objects.filter(customuser=request.user)
            for i in value:
                    
                    pro=Product_size.objects.filter(product=i.product,size=i.size)
                    
                    for j in pro:
                        
                        if j.stock < i.qty:
                            
                            messages.error(request,f"{i.product.name} out stock please choose any another product")
                            return redirect("user_cart")
            
            client = razorpay.Client(auth=(env("RAZORPAY_KEY_ID"),env('RAZORPAY_KEY_SECRET')))

            return JsonResponse({
                    'total_amount' : total ,'username' :user_id.username,'email' : user_id.email,'phone':user_id.ph_no,
                    })
        except Exception as e: 

            error=type(e).__name__
            typee,code=status_codee(error)
                
            context={
                'type' :typee,
                'code' : code
            }
            return render(request, 'dashbord/user_404.html',context)
       # .................END RAZORPAY......................
       
       # .................NEW PASSWORD......................
@login_required(login_url='/user_app/Login/')
@never_cache      
def New_Password(request):
    
     try:   
                
            if  request.user.is_authenticated:
                
                    if request.method =='POST':
                        old_pass=request.POST.get("old_password")
                        new_pass=request.POST.get("new_password")
                        con_pass=request.POST.get("con_password")
                        
                        
                        pattern = r'^[a-zA-Z0-9].*'
                        pattern_pass = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
                        
                        if not (old_pass or new_pass or con_pass ):
                            messages.error(request, "please Fill Required Field")
                            return render(request,"dashbord/new_password.html")
                        
                        elif not re.match(pattern,new_pass or con_pass or old_pass ):
                            
                            messages.error(request,"Please enter valid input")
                            return render(request,"dashbord/new_password.html")
                        
                        elif not re.match(pattern_pass,new_pass):
                            messages.error(request,"The password is too weak")
                            return render(request,"dashbord/new_password.html")
                                
                        elif new_pass != con_pass:
                            
                            messages.error(request,"New Password and confirm password doesn't match ")
                            return render(request,"dashbord/new_password.html")
                        
                        else:
                                try:
                                    
                                    
                                    user= authenticate(request,email=request.user,password=old_pass)
                                    
                                except Exception as e:
                                    
                                    messages.error(request,"Old Password doesn't match ")
                                    return render(request,"dashbord/new_password.html")
                        
                                try:
                                        
                                    user=CustomUser.objects.get(email=request.user)
                                    hashed_password = make_password(new_pass)
                                    user.password = hashed_password
                                    user.save()
                                            
                                    messages.success(request,"New password updated")
                                    return redirect("login")
                                
                                except Exception as e:
                                    return render(request,"dashbord/404.html")
                                    
                                    
                                
                            
            
            return render(request,"dashbord/new_password.html")
        
     except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
       # .................END NEW PASSWORD......................
       
       # .................USER ORDERS BILL DOWNLOADING......................
       
@login_required(login_url='/user_app/Login/')
@never_cache 
def Orders_Bill(request,id):
    
    try:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_invoice.pdf"'

            # Set up PDF canvas
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Get order items and order details
            order_items = Order_Items.objects.filter(order=id)
            order = Order.objects.get(id=id)

            # Set up basic information on the PDF
            p.drawString(250, 750, "Sales Invoice")

            # Display order information
            y_coordinate = 700
            p.drawString(100, y_coordinate, f"Date: {order.created_date.strftime('%Y-%m-%d')}")
            y_coordinate -= 20
            p.drawString(100, y_coordinate, f"Order ID: {order.order_id}")
            y_coordinate -= 20
            p.drawString(100, y_coordinate, f"Customer: {order.user.username}")

            # Extract and display address information
            address = order.user_address.strip('{}').split(',')
            address_dict = {}
            for pair in address:
                key, value = pair.split(':')
                address_dict[key.strip(" '")] = value.strip(" '")

            y_coordinate -= 20
            p.drawString(100, y_coordinate, "Address:")
            for key, value in address_dict.items():
                if key in ['house', 'street', 'city', 'country', 'pin_code']:
                    y_coordinate -= 15
                    p.drawString(120, y_coordinate, value)

            # Create a table and set its style
            data = [['Item', 'Size', 'Quantity', 'Unit Price', 'Offer Price' ,'Total']]
            for item in order_items:
                data.append([item.product.name, item.size, item.qty, item.price, item.offer_price, item.total_price])

            table = Table(data, colWidths=[100, 80, 80, 80, 80, 80,])
            style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)

            # Calculate the height of the table
            table_height = len(data) * 15

            # Draw the table on the PDF
            y_coordinate -= max(table_height, 200)  # Ensure enough space for table even if address is large
            table.wrapOn(p, 0, 0)
            table.drawOn(p, 100, y_coordinate)

            # Display "Total Amount" below the table
            total_amount = sum(item.total_price for item in order_items)
            y_coordinate -= (table_height + 20)
            if order.coupon_discount:
                
                    total_amount-=order.coupon_discount
                    p.drawString(380, y_coordinate + 20, f"Coupon: - {order.coupon_discount}")
            
            p.drawString(360, y_coordinate, f"Total Amount: {total_amount}")

            # Close the PDF object cleanly
            p.showPage()
            p.save()

            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
       
       # .................END USER ORDERS BILL DOWNLOADING......................
 
     # ................. ADD WISHLIST......................

@login_required(login_url='/user_app/Login/')
@never_cache 
def Add_Wishlist(request):
    
    try:
        if request.method== 'POST':
            pro_id =int(request.POST.get('product_id'))
            pro=Product.objects.get(id=pro_id)
            user = get_object_or_404(CustomUser, email=request.user)   
            
            if Wishlist.objects.filter(customuser=user,product=pro).exists():
            
                return JsonResponse({'success': 'already'})
            
            if Cart.objects.filter(customuser=user,product=pro).exists():
                    return JsonResponse({'success': 'cart already'})
            Wishlist.objects.create(customuser=user,product=pro) 
        
        
            return JsonResponse({'success': "added"})
        else:
            return JsonResponse({'success': False})
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
    
    # .................END WISHLIST......................
    
        # .................END WISHLIST......................

@login_required(login_url='/user_app/Login/')
@never_cache
def User_Wishlist(request):
    
    try:
        wish=Wishlist.objects.filter(customuser=request.user)

        context={
            
            'wish': wish
        }
        
        return render(request,'dashbord/wishlist.html',context)      
     
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
 
            # .................END WISHLIST......................
            
            # .................REMOVE WISHLIST......................
        
@login_required(login_url='/user_app/Login/')
@never_cache    
def Remove_Wishlist(request,id):
    try:
        Wishlist.objects.get(id=id).delete()
        return redirect("user_wishlist")
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
            
            # .................END REMOVE WISHLIST......................
            
             # ................. WALLET......................
             
@login_required(login_url='/user_app/Login/')
@never_cache
def My_Wallet(request):
    
    try:
        wallet=CustomUser.objects.get(email=request.user)
        transaction=Wallet_Transactions.objects.filter(customuser=wallet.id)
        public_key = env('RAZORPAY_KEY_ID')

        context={
            'wallet' : wallet,
            'transaction' : transaction,
             'key' : public_key
        }
        
        return render(request,'dashbord/wallet.html',context)
    
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
                    
        context={
            'type' :typee,
            'code' : code,
           
        }
        return render(request, 'dashbord/user_404.html',context)


            # .................END WALLET......................
            
            # ................. WALLET UPI......................

@never_cache   
def Wallet_upi(request):
    
    try:
    
        user_id=int(CustomUser.objects.get(email=request.user))
        user=CustomUser.objects.get(id=user_id)
        client = razorpay.Client(auth=(env("RAZORPAY_KEY_ID"),env('RAZORPAY_KEY_SECRET')))
        print("coming call")
            
        return JsonResponse({
                        'username' :user.username,'email' : user.email,'phone':user.ph_no,
                        })
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
       
       # .................END WALLET UPI......................
       
       # .................WALLET RECHARGE......................
       
@login_required(login_url='/user_app/Login/')
@never_cache
def wallet_Recharge(request):
    
    try:
        if request.method == "POST":

            amount=request.POST.get("amount")
            payment_type=request.POST.get("payment_mode")
            
            user=CustomUser.objects.get(email=request.user)
            new_balance = int(user.wallet_bal) + int(amount)
            user.wallet_bal=new_balance
            user.save()
            
            Wallet_Transactions.objects.create(customuser=request.user,
                                            amount=amount,
                                            resons=payment_type,
                                            add_or_pay = 'add'
                                            )
        return redirect("my_wallet")
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
       
       
       # .................END WALLET RECHARGE......................
       
#.......................... STATUS CODE CHEKING.................

never_cache
def status_codee(error):
    

    
    if error == 'ValidationError':
        type='Page not Found'
        code=404
        return type,code
    
    elif error == 'TypeError':
        
        type='Bad Request'
        code=400
        return type,code
    
    else:
        
        type='Page not Found'
        code=404
        return type,code

 #..........................END STATUS CODE CHEKING.................
 
  #..........................ORDER RETURN.................

 
@login_required(login_url='/user_app/Login/')
@never_cache
def Return(request,id):
        
    try:
                
            order=Order.objects.get(id=id)
            date=timezone.now()
            if order:
                                
                    user_order=Order_Items.objects.filter(order_id=id)
                    for i in user_order:
                        
                        
                        stock=Product_size.objects.get(product=i.product,size=i.size)
                        
                        stock.stock += i.qty
                        stock.save()
                
                   
                    
                 #  .......................... Order Amount Add To Wallet....................
                 
                    user=CustomUser.objects.get(id=order.user)
                    user.wallet_bal = int(user.wallet_bal) + int(order.total_amount)
                    user.save()
                    Wallet_Transactions.objects.create(customuser = user,
                                                       amount= order.total_amount,
                                                       resons= 'order Return',
                                                       add_or_pay = 'add',               
                                                       )
                    order.status= 'refunded'
                    order.status_date=date
                    order.save()
                    
            return redirect("my_order")    
               
        
    except Exception as e: 

        error=type(e).__name__
        typee,code=status_codee(error)
            
        context={
            'type' :typee,
            'code' : code
        }
        return render(request, 'dashbord/user_404.html',context)
    
    
      #..........................END ORDER RETURN.................


