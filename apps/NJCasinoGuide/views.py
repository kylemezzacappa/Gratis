from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def NJRanking(request):
    return render(request, 'NJCasinoGuide/NJRanking.html')