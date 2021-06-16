from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from api.models import *
from .forms import *
from django.contrib.auth import get_user_model
User = get_user_model()

def Signup(request):
    if request.method == "POST":
        form =AddTrainerForm(request.POST)
        if form.is_valid():
            form.create()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = AddTrainerForm()
    return render(request, 'registration/signup.html', {'form': form})
