
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import user_passes_test
from .form import *

import json
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date

User = get_user_model()

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def processDate(request):
    newdate = parse_date(json.loads(request.POST.get('date', None))["date"])
    request.session["date"] = json.dumps(
        newdate, indent=4, sort_keys=True, default=str)


def processForm(request):

    # Get the posted form
    ClientSelect = UserForm(request.POST, request=request)
    if ClientSelect.is_valid():
        selected_client = ClientSelect.cleaned_data["selected_client"]
        session_id = ClientSelect.cleaned_data["session_id"]

        client = User.objects.get(email=selected_client.email)
        
        request.session[session_id+"_selected_client"] = selected_client.email
        request.session[session_id+"_clone_client"] = client.first_name + " " + client.last_name

        form = UserForm(initial={'selected_client': User.objects.get(email=request.session[session_id+'_selected_client'])}, request=request)
        form.fields["selected_client"].empty_label = None
        return form

def home(request):
    if request.method == "POST":
        form = processForm(request)
    else:
        form = UserForm(request=request)
    return render(request, 'trainerInterface/home.html', {'form': form})

def privacy(request):
    return render(request, 'registration/privacy.html')

def appHelp(request):
    return render(request, 'registration/help.html')

def dashboard(request):
    if request.session["href"] is None:
        request.session["href"] = '/dashboard/'
    if request.method == "POST":
        form = processForm(request)
    else:
        form = UserForm(request=request)
    if is_ajax(request):
        return render(request, 'trainerInterface/dashboard-ajax.html', {'form': form})
    else:
        return render(request, 'trainerInterface/dashboard.html', {'form': form})


def clients(request):
    if request.method == "POST":
        form = processForm(request)
    else:
        form = UserForm(request=request)
    trainer = Trainer.objects.get(trainer=request.user)

    return render(request, 'trainerInterface/clients.html', {'form': form, 'clients': trainer.clients.all()})
