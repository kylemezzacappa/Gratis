from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here. These connect to the templates/html, but must be accessed from the sister urls dir.
# This is where I store my methods.
# the client gets information with GET, but when it submits a form it will use POST. 
# Refreshing the browser will yield the same GET or POST method previously used.
# Render will go to the HTML, but Request will go to the method in views

def index(request):
    return render(request, 'Gratis/index.html')

def home(request):
    return render(request, 'Gratis/home.html')

def liveStocks(request):
    return render(request, 'Gratis/liveStocks.html')

def create(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name= first_name, last_name= last_name, email= email, password= password)
    user.save()
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name

    return redirect("/home")

def validate_login(request):
    errors = User.objects.log_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])  
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    request.session['first_name'] = user.first_name
    request.session['last_name'] = user.last_name
    return redirect("/home")

def success(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    messages.success(request, "Sucessfully registered or (logged in)!")
    return render(request,'Gratis/home.html', context)

def logout(request):
    request.session.clear()
    return redirect("/")

