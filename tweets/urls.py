from django.urls import path
from . import views

app_name = 'tweets'

urlpatterns = [
    path('create/', views.create_tweet, name='create'),
       path('edit/<int:tweet_id>/', views.edit_tweet, name='edit'),
    path('delete/<int:tweet_id>/', views.delete_tweet, name='delete'),
        path('my-tweets/', views.my_tweets, name='my_tweets'),
    path('like/<int:tweet_id>/', views.like_tweet, name='like'),
     path('user/<str:username>/', views.user_profile, name='user_profile'),
]
