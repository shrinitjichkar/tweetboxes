from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from tweets.models import Tweet

def home_view(request):
    if request.user.is_authenticated:
        return redirect('core:feed')
    return redirect('accounts:login')

@login_required
def feed_view(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    paginator = Paginator(tweets, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'core/feed.html', context)
