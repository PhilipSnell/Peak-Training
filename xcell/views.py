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
        form = AddTrainerForm(request.POST)
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


def SignupClient(request, trainer=None):
    trainer_name = trainer.split('-')
    if request.method == "POST":
        form = AddClientForm(request.POST)
        try:
            trainer = User.objects.get(
                first_name=trainer_name[0], last_name=trainer_name[1])
            trainer = Trainer.objects.get(trainer=trainer)

        except:

            form.add_error('', 'trainer doesnt exist')

        if form.is_valid():

            print("form is valid")
            form.create()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=raw_password)
            trainer.clients.add(user)
            # // login(request, user)
            return redirect('home')
    else:
        form = AddClientForm()

    return render(request, 'registration/signup-client.html', {'form': form, 'firstName': trainer_name[0], 'lastName': trainer_name[1]})
