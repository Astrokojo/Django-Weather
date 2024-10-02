from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #the path for our index view
    path('delete/<city_name>/', views.delete_city, name='delete_city')
]