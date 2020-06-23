"""MyAPI URL Configuration"""

from django.urls import path
from . import views
urlpatterns = [
    path('', views.mySite, name='mySite'),
	path('form/', views.myForm, name='myForm'),
    path('status/', views.status, name='status'), 
] 
