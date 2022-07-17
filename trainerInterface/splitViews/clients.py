from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect


def clients(request):

    trainer = Trainer.objects.get(trainer=request.user)
    return render(request, 'trainerInterface/clients.html', {'clients': trainer.clients.all()})
