# from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.autocomplete, name='autocomplete'),
    path('by_name/', views.search_by_name, name='search_by_name'),
]
