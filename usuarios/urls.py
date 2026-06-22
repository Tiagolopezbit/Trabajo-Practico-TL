from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro),
    path('login/', views.login),
]