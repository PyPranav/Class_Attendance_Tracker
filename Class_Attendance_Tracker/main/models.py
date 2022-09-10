from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClassName(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=5)
    def __str__(self):
        return self.name

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjectName = models.CharField(max_length=50)

    def __str__(self):
        return self.subjectName

class Student(models.Model):
    classname = models.ForeignKey(ClassName, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rollno = models.CharField(max_length=10)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    netAttendance = models.IntegerField(default=0)
    
    def __str__(self):
        return self.firstname+" "+self.lastname

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    ispresent = models.BooleanField()

    def __str__(self):
        return self.ispresent