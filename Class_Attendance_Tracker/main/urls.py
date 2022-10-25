from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.loginPage, name='login'),
    path("register/", views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path("createclass/", views.createClass, name='createClass'),
    path("takeattendance/", views.takeAttendance, name="takeAttendance"),
    path("search/",views.search, name="search"),
    path("search/adv",views.adv_search, name="adv_search"),
]