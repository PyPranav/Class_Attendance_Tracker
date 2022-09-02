from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

#_________________________________________Login Logout and Regitering User___________________________________________
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {}
    if request.method=='POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account was created for "+form.cleaned_data.get("username"))
            return redirect('login')
    context = {'form':form}
    print(form.errors)
    return render(request, 'register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')
#______________________________________________________________________________________________________

@login_required(login_url='login')
def home(request):
    return HttpResponse("<h1>heyya</h1>"+str(request.user))
