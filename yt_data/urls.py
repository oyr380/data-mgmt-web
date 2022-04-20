from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('channel/<chname>/', views.channel, name='channel'),
    path('channel/', views.channel, name='yt_data_channel'),
]
