from django.urls import path, include
from django.contrib import admin
from . import views


#ulrConf
urlpatterns = [
    path('', views.base),
    path('hello/', views.say_hello),
    path('register/', views.register),
    path('', include('django.contrib.auth.urls'))
]
