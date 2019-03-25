from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Profile
from .forms import UserCreationForm


def login(request):
    if request.user.is_authenticated:
        return redirect('posts:list')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', { # registration
        'form': form, 'next': request.GET.get('next', ''),
    })


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', { # registration
        'form': form,
    })
    

def post_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    posts = user.post_set.all()
    return render(request, 'accounts/post_list.html', {'page_user':user, 'posts':posts})


@require_POST
def follow(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if user == request.user:
        status = 422
        data={}
    else:
        if request.user in user.followers.all():
            user.followers.remove(request.user)
            status = 200
            data = {'followed': False}
        else:
            user.followers.add(request.user)
            status = 200
            data = {'followed': True}

    return JsonResponse(data, status=status)
