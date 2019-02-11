from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/home')
    else:
        form = UserCreationForm()
    form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def home(request):
    return render(request, 'users/home.html')


def logut(request):
    logout(request)
