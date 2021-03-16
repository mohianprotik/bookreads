from django.contrib import admin
from django.urls import path
from .views import book_details

urlpatterns = [
    path('<int:book_id>/', book_details, name='book_details'),
    
]
