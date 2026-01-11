from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
     path('feed/', views.feed_view, name='feed'),
]
