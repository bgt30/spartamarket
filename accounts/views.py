from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, ProfileUpdateForm

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products:product_list')
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    is_following = request.user.is_following(profile_user) if request.user.is_authenticated else False
    
    context = {
        'profile_user': profile_user,
        'is_following': is_following,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if request.user != target_user:  # 자기 자신을 팔로우할 수 없도록
        if request.user.following.filter(id=target_user.id).exists():
            request.user.following.remove(target_user)
        else:
            request.user.following.add(target_user)
    
    return redirect('accounts:profile', user_id=user_id)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', user_id=request.user.id)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile_update.html', {'form': form})

