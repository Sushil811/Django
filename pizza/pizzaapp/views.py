from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import PizzModel, CustomerModel, OrderModel

# Create your views here.
def adminloginview(request):
    return render(request,'pizzaapp/adminlogin.html')

def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    #user exist
    if user is not None and user.username == "admin":
    #or if user is not None:
        login(request, user)
        return redirect('adminhomepage')


    #user doesn't exist
    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Username or Password") # Error message
        return redirect('adminloginpage')

def adminhomepageview(request):
    pizzas = PizzModel.objects.all()
    context = {'pizzas': pizzas}
    return render(request,'pizzaapp/adminhomepage.html', context)

def logoutadmin(request):
    logout(request)
    return redirect('adminloginpage')

def addpizza(request):
    #adding pizza into the database
    name = request.POST['pizza']
    price = request.POST['price']
    PizzModel(name=name, price=price).save()
    return redirect('adminhomepage')

def deletepizza(request, pizzapk):
    PizzModel.objects.filter(id = pizzapk).delete()
    return redirect('adminhomepage')


def homepageview(request):
    return render(request, "pizzaapp/homepage.html")

def signupuser(request):
    username = request.POST['username']
    password = request.POST['password']
    phoneno = request.POST['phoneno']

    #if username already exist
    if User.objects.filter(username = username).exists():
        messages.add_message(request, messages.ERROR, 'User Already Exists')
        return redirect('homepage')


    #if username doesn't exist
    User.objects.create_user(username = username, password = password).save()
    lastobject = len(User.objects.all())-1
    CustomerModel(userid = User.objects.all() [int(lastobject)].id, phoneno = phoneno).save()
    messages.add_message(request,messages.ERROR, 'User Successfully registered')
    return redirect('homepage')


def userloginview(request):
    return render (request, 'pizzaapp/userlogin.html')

def userauthenticate(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    if user is not None:
        login(request, user)
        return redirect('customerpage')

    if user is None:
        messages.add_message(request,messages.ERROR,"Invalid Credentials")
        return redirect('userloginpage')

def customerwelcomeview(request):
    username = request.user.username
    context = {'username': username,'pizzas': PizzModel.objects.all()}
    return render(request, 'pizzaapp/customerwelcome.html', context)

def userlogout(request):
    logout(request)
    return redirect ('userloginpage')

def placeorder(request):
    username = request.user.username
    phoneno = CustomerModel.objects.filter(userid = request.user.id)[1].phoneno
    address = request.POST['address']
    ordereditems = ""
    for pizza in PizzModel.objects.all():
        pizzaid = pizza.id
        name = pizza.name
        price = pizza.price
        quantity = request.POST.get(str(pizzaid), " ")

        print(name)
        print(price)
        print(quantity)
        if str(quantity) != "0" and str(quantity) == " ":
            ordereditems = ordereditems + name + " " + price + "quantity : " + quantity + " "



    OrderModel(username=username, phoneno=phoneno, address=address, ordereditems=ordereditems).save()
    messages.add_message(request, messages.SUCCESS, "Order Successfully placed")
    return redirect('customerpage')


