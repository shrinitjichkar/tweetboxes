from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Tweet

@login_required
def create_tweet(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image', None)
        if content or image:
            if len(content) <= 280:
                tweet = Tweet.objects.create(user=request.user, content=content)
                if image:
                    tweet.image = image
                    tweet.save()
                messages.success(request, 'Tweet posted successfully!')
                return redirect('core:feed')
            else:
                messages.error(request, 'Tweet cannot exceed 280 characters')
        else:
            messages.error(request, 'Tweet content or image is required')
    return redirect('core:feed')

@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image', None)
        remove_image = request.POST.get('remove_image', False)
        if content or tweet.image or image:
            if len(content) <= 280:
                tweet.content = content
                if remove_image:
                    tweet.image.delete()
                    tweet.image = None
                if image:
                    if tweet.image:
                        tweet.image.delete()
                    tweet.image = image
                tweet.save()
                messages.success(request, 'Tweet updated successfully!')
                return redirect('tweets:my_tweets')
            else:
                messages.error(request, 'Tweet cannot exceed 280 characters')
        else:
            messages.error(request, 'Tweet content or image is required')
    return render(request, 'tweets/edit_tweet.html', {'tweet': tweet})

@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, 'Tweet deleted successfully!')
        return redirect('tweets:my_tweets')
    return render(request, 'tweets/delete_tweet.html', {'tweet': tweet})

@login_required
def my_tweets(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tweets/my_tweets.html', {'page_obj': page_obj})

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        messages.info(request, 'Tweet unliked')
    else:
        tweet.likes.add(request.user)
        messages.info(request, 'Tweet liked')
    return redirect('core:feed')

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    paginator = Paginator(tweets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'is_own_profile': request.user == user
    }
    return render(request, 'tweets/user_profile.html', context)
