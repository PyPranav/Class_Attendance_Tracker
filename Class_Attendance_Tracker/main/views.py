from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *

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
    context={}
    return render(request, "home.html", context)

@login_required(login_url="login")
def createClass(request):
    context={}
    return render(request, 'createClass.html', context )

@login_required(login_url="login")
def takeAttendance(request):
    context = {"takeAttendanceDetails":True}
    if request.method == "POST":
        print(request.POST)
        print(request.GET)
        curClass = request.user.classname_set.filter(name=request.GET.get('className'))[0]
        students = curClass.student_set.all()
        sub = request.user.subject_set.filter(subjectName=request.GET.get('subName'))[0]
        for student in students:
            student.attendance_set.create(user = request.user, subject = sub, datetime=request.GET.get('curdate')+" "+request.GET.get('curtime')+":00", ispresent=student.rollno in request.POST)
            student.netAttendance += 1 if student.rollno in request.POST else 0
            student.save()
        messages.success(request, f"Attendance of class {curClass.name} was recorded")
        return redirect('home')
        

    if request.method == "GET" and request.GET and "className" in request.GET:
        print(request.GET)
        context["takeAttendanceDetails"]=False
        context["className"] = request.GET.get('className')
        context["subName"] = request.GET.get('subName')
        context["curdate"] = request.GET.get('curdate')
        context["curtime"] = request.GET.get('curtime')
        context['allStudents'] = request.user.classname_set.filter(name = context['className'])[0].student_set.all()
        totalAttendanceToDate = len(context['allStudents'][0].attendance_set.all())
        context['allStudents'] = [[z, int(z.netAttendance*100/totalAttendanceToDate) if totalAttendanceToDate>0 else 100] for z in context['allStudents']]
        return render(request, 'takeAttendance.html', context )

    context['subjects'] = request.user.subject_set.all()
    context['classnames'] = request.user.classname_set.all()
    return render(request, 'takeAttendance.html', context )