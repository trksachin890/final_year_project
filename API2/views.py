from django.shortcuts import render,redirect
from app.models import Product,Category,FilterYear,Color,Brand,Contact_us,Order,OrderItem
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import khalti
import requests
import json









def BASE(request):
    return render(request,'main/base.html')

def HOME(request):
    product = Product.objects.filter(status = 'PUBLIC')

    context = {
        'product': product,
    }

    return render (request,'main/index.html', context)

def SIGNIN(request):
    return render (request, 'main/signin.html')

def PRODUCT(request):
    product = Product.objects.filter(status = 'PUBLIC')
    categories = Category.objects.all()
    filter_year = FilterYear.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()


    CATID = request.GET.get('categories')
    YEAR_FILTER_ID=request.GET.get('filter_year')
    COLORID=request.GET.get('color')
    BRANDID= request.GET.get('brand')
    ATOZID=request.GET.get("ATOZ")
    ZTOAID=request.GET.get("ZTOA")
    PRICE_LOWTOHIGHID=request.GET.get("PRICE_LOWTOHIGH")
    PRICE_HIGHTOLOWID=request.GET.get("PRICE_HIGHTOLOW")
    NEW_PRODUCTID=request.GET.get("NEW_PRODUCT")
    OLD_PRODUCTID=request.GET.get("OLD_PRODUCT")

    if CATID:
        product = Product.objects.filter(category = CATID, status="PUBLIC")
    elif YEAR_FILTER_ID:
        product=Product.objects.filter(filter_year=YEAR_FILTER_ID ,  status="PUBLIC")
    elif COLORID:
        product=Product.objects.filter(color=COLORID,status = 'PUBLIC')
    elif BRANDID:
        product=Product.objects.filter(brand=BRANDID,status = 'PUBLIC')
    elif ATOZID:
        product=Product.objects.filter(status = 'PUBLIC').order_by('-name')
    elif ZTOAID:
        product=Product.objects.filter(status = 'PUBLIC').order_by('name')
    elif PRICE_LOWTOHIGHID:
        product=Product.objects.filter(status = 'PUBLIC').order_by('price')
    elif PRICE_HIGHTOLOWID:
        product=Product.objects.filter(status = 'PUBLIC').order_by('-price')
    elif NEW_PRODUCTID:
        product=Product.objects.filter(status = 'PUBLIC',condition='NEW').order_by('-id')
    elif OLD_PRODUCTID:
        product=Product.objects.filter(status = 'PUBLIC',condition='OLD').order_by('-id')
    else:
        product = Product.objects.filter(status = 'PUBLIC').order_by('-id')


    context = {
        'product': product,
        'categories':categories,
        'filter_year':filter_year,
        'color': color,
        'brand':brand
    }
    return render(request,'main/product.html',context)

def SEARCH(request):
    query = request.GET.get('query')
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product': product
    }
    return render(request,'main/search.html',context)

def PRODUCT_DETAIL_PAGE(request,id):
    prod = Product.objects.filter(id=id).first()
    context = {
        'prod':prod,
    }
    return render(request,'main/product_single.html',context)

def Contact_Page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,message,email_from,['mrsachin2060@gmail.com'])
            contact.save()
            return redirect('home')
        except:
            return redirect('contact')
        
    return render(request,'main/contact.html')



def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        customer = User.objects.create_user(username,email,pass1)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.save()
        return redirect('register')

    return  render(request, 'registration/auth.html')

def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =  authenticate(username=username,password=password )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')

    return  render(request, 'registration/auth.html')

def HandleLogout(request):
    logout(request)
    
    return  redirect('home')




@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'cart/cart_details.html')

def CHECKOUT(request):
    return render(request,'cart/checkout.html')

def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id = uid)
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get("postcode")
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        
        
        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            amount = amount,

        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a*b

            item = OrderItem(
                user = user,
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()
    return render(request,'cart/placeorder.html')










def YOUR_ORDER(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id = uid)
    order = OrderItem.objects.filter(user = user)
    context = {
        'order':order
    }
    return render(request,'main/your_order.html',context)


def SUCCESS(request):
    return render(request,'cart/thank-you.html')


def ACCOUNT(request):
    return render(request,'main/account.html')