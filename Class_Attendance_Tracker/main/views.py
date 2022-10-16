from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime

#_________________________________________Login Logout and Registering User___________________________________________

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
    latest=request.user.attendance_set.last()
    context["clsName"]=latest.student.classname.name
    context['dt']=latest.datetime.strftime("%d-%m-%Y, %H:%M")
    context['subj']=latest.subject
    # print(clsName,dt,subj)
    return render(request, "home.html", context)

@login_required(login_url="login")
def createClass(request):
    context={"takeNewStudentDetails":False}

    if request.method=="GET" and request.GET:
        req = request.GET
        if request.user.classname_set.filter(name = req.get('year')+'_'+req.get('className')):
            messages.info(request,"Class already exists!")
            return render(request, 'createClass.html', context )
        if req.get('strength').isdigit() and int(req.get('strength'))<=999 and int(req.get('strength'))>=1:
            context["className"] = req.get('year')+'_'+req.get('className')
            context['rnge'] = map(lambda x: (3-len(str(x)))*"0"+str(x) ,range(1,int(req.get('strength'))+1))
            context["takeNewStudentDetails"] = True
        else:
            messages.info(request,"Please enter a valid strength of class!")

    if request.method=="POST":
        reqP = request.POST
        reqG = request.GET
        clsName = request.user.classname_set.create(name=reqG.get('year')+'_'+reqG.get('className'))
        request.user.save()
        strength = int(reqG.get("strength"))
        for i in range(1,strength+1):
            i = str(i)
            i = (3-len(i))*"0"+i
            fname = reqP.get('firstName_'+i)
            lname = reqP.get('lastName_'+i)
            rollno = clsName.name+i
            clsName.student_set.create(user=request.user, rollno=rollno, firstname=fname, lastname=lname)
        clsName.save()
        messages.success(request, f"New class {clsName.name} was created")
        return redirect("home")
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
        

    if request.method == "GET" and request.GET and "className" in request.GET and "subName" in request.GET:
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
    now = datetime.now()
    context['curdate'], context['curtime'] = now.strftime("%Y-%m-%d"), now.strftime("%H:%M")

    return render(request, 'takeAttendance.html', context )