from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        # username = request.POST["username"]
        # password = request.POST["password"]
        # user = authenticate(request, username=username, password=password)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main_homepage')
        else:
            messages.success(request, "Error Logging In")
            return render(request, 'authentication/login_user.html', {"form":form})# Return an 'invalid login' error message

    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login_user.html', {"form":form})


def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('main_homepage')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration successful"))
            return redirect('main_homepage')
    else:
        form = UserCreationForm()

    return render(request, 'authentication/register_user.html', {
        'form':form,
    })


