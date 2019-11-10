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
    return render(request, 'Crossroads/index.html')

def create(request):
    errors = User.objects.regValidator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/Crossroads/')
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name= first_name, last_name= last_name, email= email, password= password)
    user.save()
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    return redirect("/Crossroads/bonuses")

def validate_login(request):
    errors = User.objects.log_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/Crossroads/')
    user = User.objects.get(email=request.POST['email'])  
    request.session['user_id'] = user.id
    request.session['user_name'] = user.first_name
    return redirect("/Crossroads/bonuses")

def success(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    messages.success(request, "Sucessfully registered or (logged in)!")
    return render(request,'Crossroads/bonuses.html', context)

def logout(request):
    request.session.clear()
    return redirect("/")

def bonuses(request):  
    context = {
        'allBonuses': Bonus.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    } 
    return render(request,'Crossroads/bonuses.html', context)

def process_bonus(request): 
    errors = Bonus.objects.bonusValidator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/index')
    bonus_name=request.POST['bonus_name'] 
    Message=request.POST['Message']
    creator = User.objects.get(id=request.session['user_id'])
    bonus = Bonus.objects.create(bonus_name=bonus_name,Message=Message, creator=creator) 
    return redirect('/')


def edit_bonus(request, bonus_id):
    context={
        'thisBonus': Bonus.objects.get(id=bonus_id),
        'allbonuses': Bonus.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'Crossroads/index.html', context)


def process_edit(request, id):
    errors = Bonus.objects.bonusValidator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect('/bonuses')
    bonusToUpdate=Bonus.objects.get(id=id)
    bonusToUpdate.bonus_name=request.POST['bonus_name'] 
    bonusToUpdate.Message=request.POST['Message']
    bonusToUpdate.save()
    return redirect(f'/index')

def delete_bonus(request, bonus_id):
    destroy= Bonus.objects.get(id=bonus_id)
    destroy.delete()
    return redirect('/index')

def user_bonuses(request, bonus_id):
    context={
        'thisBonus': Bonus.objects.get(id=bonus_id),
        'allBonuses': Bonus.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'Crossroads/index.html', context)

def myaccount(request, user_id):
    context={
        'allBonuses': Bonus.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'bonuses/myaccount.html', context)

# fix to redirect to current page correctly and prepopulate form data
def edit_account(request, id): 
    errors = User.objects.accountValidator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error)
        return redirect(f'/myaccount/5')
    accountToUpdate=User.objects.get(id=id)
    accountToUpdate.first_name=request.POST['first_name'] 
    accountToUpdate.Message=request.POST['last_name']
    accountToUpdate.email=request.POST['email']
    accountToUpdate.save()
    return redirect("/index")




