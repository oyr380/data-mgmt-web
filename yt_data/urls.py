from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='yt_data_home'),
    path('about/', views.about, name='yt_data_about'),
]
