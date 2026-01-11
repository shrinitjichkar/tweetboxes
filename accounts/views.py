from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('accounts:login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:feed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            login(request, user)
            return redirect('core:feed')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:feed')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('core:feed')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')
