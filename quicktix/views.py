import json
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage(request):
    return render(request, "quicktix/index.html")

def features(request):
   return render(request, "quicktix/features.html")

def login(request):
    print (request.POST.get('email'))
    return render(request, "quicktix/login.html")

def dashboard(request):
   return render(request, "quicktix/dashboard.html")
