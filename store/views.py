from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from .forms import *
from .authenticated import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


from django.utils.translation import activate

from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
# Create your views here.

def store(request):
    items, order, cartItems = get_cart_info(request)

    videos = Video.objects.all()


    context = {'items': items, 'order': order, 'cartItems': cartItems, 'videos': videos}
    return render (request, 'store/index.html', context)

def set_language(request):
    user_language = request.GET.get('language', settings.LANGUAGE_CODE)
    activate(user_language)
    response = redirect('/')
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return response


def searchProducts(request):
    if request.method == 'GET':
        items, order, cartItems = get_cart_info(request)
        searched = request.GET.get('searched')
        if searched:

            products = Product.objects.filter(name__contains = searched)
            context = {'products': products}
            
        else:
            products = Product.objects.all()
            customer = Customer.objects.get(name=request.user.username)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

        context = {'products': products,'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'store/Trgovina.html', context)



def kontakt(request):
    items, order, cartItems = get_cart_info(request)

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render (request, 'store/Kontakt.html', context)


def pecanje(request):
    items, order, cartItems = get_cart_info(request)


    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render (request, 'store/Pecanje.html', context)

def pesme(request):
    items, order, cartItems = get_cart_info(request)

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render (request, 'store/Pesme.html', context)

def zbirkaPesama(request):
    
    context = {}
    return render(request, 'store/pesme/zbirkaPesama.html', context)

def pricesaterena(request):
    items, order, cartItems = get_cart_info(request)
        

    context = {'items': items, 'order': order,'cartItems': cartItems, }
    return render (request, 'store/PričeSaTerena.html', context)

def prica1(request):

    items, order, cartItems = get_cart_info(request)
    cartItems = order.get_cart_items
    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render (request, 'store/prica1.html', context)

def trgovina(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = Customer.objects.get(name=request.user.username)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.info(request, 'You must be logged in to add to cart')
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        redirect('/')

    sort_by = request.GET.get('sort_by', 'name')  # Podrazumevano sortiranje po nazivu
    if sort_by == 'name':
        products = Product.objects.all().order_by('name')
    elif sort_by == 'price':
        products = Product.objects.all().order_by('price')
    else:
        products = Product.objects.all()
        
    context = {'items': items, 'order': order,'cartItems': cartItems, 'products': products, 'sort_by': sort_by}
    return render(request, 'store/Trgovina.html', context)

@login_required(login_url='/loginPage/')
def trgovinaDetaljnije(request, pk):
     product = get_object_or_404(Product, id=pk)
     items, order, cartItems = get_cart_info(request)
     cartItems = order.get_cart_items
     context = {'items': items, 'order': order,'cartItems': cartItems,'product': product,}
     return render(request, 'store/trgovinaDetaljnije.html', context)

def kurs(request):
    items, order, cartItems = get_cart_info(request)

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render (request, 'store/Kurs.html', context)

def kursTehnologije(request):
    return render(request, 'store/kursTehnologije.html')    

@login_required(login_url='/loginPage/')
def cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(name=request.user.username)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.info(request, 'You must be logged in to add to cart')
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']



    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render (request, 'store/cart.html', context)

def deleteOrder(request, pk):
    order = OrderItem.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('cart')

    context = {'item': order}
    return render(request, 'store/deleteOrder.html', context)

@login_required(login_url='/loginPage/')
def checkout(request):
    items, order, cartItems = get_cart_info(request)

    
    context = {'items': items, 'order': order, 'cartItems': cartItems,}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='/loginPage/')
def checkoutConfirm(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(name=request.user.username)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartList = order.get_cart_list
        cartItems = order.get_cart_items


        html_message = render_to_string('store/podaciokorisniku.html', {'user': request.user, 'email': request.user.email, 'grad': request.user.first_name, 'adresa': request.user.last_name, 'total': order.get_cart_total, 'ukupnoukorpi': order.get_cart_items, 'stvariukorpi': cartList})
       
             
        
#sending an email
        email = EmailMessage(
            'Podaci o korisniku',
            html_message,
            settings.EMAIL_HOST_USER,
            ['darko.spasojevic.django25@gmail.com'],
        )
        
        email.fail_silently = False
        email.send()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render (request, 'store/checkoutConfirm.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            customer = Customer(name=user)
            customer.save()
            messages.success(request, 'Account was created for user ' + user)
            return redirect('loginPage')

    context = {'form': form}
    return render(request, ('store/registerPage.html'),context)

def loginPage(request):
    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('trgovina')
            else:
                messages.info(request, 'Username or password is incorrect')


        context = {}
        return render(request, ('store/loginPage.html'), context)


def logoutPage(request):
    logout(request)
    
    return redirect('/')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productId:', productId)

    customer = Customer.objects.get(name=request.user.username) 
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created =  OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)
