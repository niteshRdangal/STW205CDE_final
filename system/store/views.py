from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']


    products = Product.objects.all()
    context= {'products':products,'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context= {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context= {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action',action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)




    else:
        customer,order =guestOrder(request, data)


    order.transaction_id = transaction_id

    order.complete = True
    order.save()

    if order.delivery == True:
        DeliveryAddress.objects.create(
            customer=customer,
            order=order,
            address=data['delivery']['address'],
            city=data['delivery']['city'],
            state=data['delivery']['state'],
            zipcode=data['delivery']['zipcode'],
        )
    return JsonResponse('Payment complete!', safe=False)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was craeted for: ' + user)

            return redirect('login')

    context = {'form':form}
    return render(request, 'store/register.html',context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)

        return redirect('store')
    context = {}
    return render(request, 'store/login.html', context)


