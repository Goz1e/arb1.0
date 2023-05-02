from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
import email
from django.shortcuts import render, redirect
from .forms import UserCreationForm, LoginForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.account.forms import ResetPasswordForm, AddEmailForm
from allauth.socialaccount.forms import DisconnectForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect('arb:dashboard')
    
    template_name = 'accounts/index.html'
    context = {'title':'arby'}
    return render(request,template_name,context)


def signup(request):
    print('initiated....................')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:completed')
    return render(request, 'accounts/signup.html', {'signup_form': form,'title':'dashboard'})


def login_view(request,backend = 'django.contrib.auth.backends.ModelBackend'):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.info(request, "login successful!")                
                return redirect('arb:dashboard')    
            else:
                messages.info(request, "login failed!")
            return redirect('accounts:index')
        
    return render(request, 'accounts/login.html', context={'form': LoginForm,'title':'login'})


# def completed(request):
#     return render(request, 'accounts/completed.html', context={'title':'Completed!'})


def about(request):
    template_name = 'accounts/about.html'
    context = {'title':'about',}
    return render(request,template_name,context)

def test(request):
    template_name = 'accounts/test.html'
    context = {'title':'test',}
    return render(request,template_name,context)


@login_required(login_url='accounts:index')         
def logout_view(request):
    logout(request)
    return redirect('accounts:index')


@login_required(login_url='accounts:index')
def delete_account(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()
        messages.info(request,'account deleted successfully!')
        return redirect('accounts:index')