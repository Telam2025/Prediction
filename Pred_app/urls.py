from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='Home'),
    path('contact/', views.contact,name='Contact'),
    path('upload/', views.upload_view, name='upload'),
  
]
