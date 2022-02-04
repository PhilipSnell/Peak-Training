from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
from datetime import date


def graphTracking(request):
    if request.method == "POST":
        processForm(request)
        if request.is_ajax():
            processDate(request)

    if "selected_client" in request.session:
        newdate = date.today()
    newdate = date.today()
    form = getUserform(request)

    return render(request, 'trainerInterface/graph.html', {'form': form, 'date': newdate})
