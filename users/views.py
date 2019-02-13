from django.contrib.auth import logout
from .forms import SignUpForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/home')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})


def home(request):
    return render(request, 'users/home.html')


def logut(request):
    logout(request)
