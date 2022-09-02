from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("<h1>heyya</h1>"+str(request.user))

def loginPage(request):
    pass

def registerPage(request):
    pass

def logoutPage(request):
    return redirect('login')