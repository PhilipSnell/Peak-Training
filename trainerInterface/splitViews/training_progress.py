from django.http import JsonResponse
from trainerInterface.views import is_ajax
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render


def trainprog(request):
    request.session["href"] = '/dashboard/trainprog/'
    if is_ajax(request):
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)
        if phase == None:
            phase = Phase.objects.filter(user=User.objects.get(
                email=request.session['selected_client'])).order_by('-phase')[0]
            week = Week.objects.filter(user=User.objects.get(
                email=request.session['selected_client']), phase=phase.phase).order_by('-week')[0]
        else:
            week = Week.objects.get(user=User.objects.get(
                email=request.session['selected_client']), phase=phase, week=week)

        return render(request, 'trainerInterface/trainProg.html', {'days': week.days.all().order_by('day')})


def getDayTableDataProg(request):

    if is_ajax(request):
        phase = request.POST.get('phase', None)
        week = request.POST.get('week', None)
        client = request.POST.get('client', None)
        if "selected_client" in request.session and client == None:
            week = Week.objects.get(user=User.objects.get(
                email=request.session['selected_client']), phase=phase, week=week)
            days = week.days.all()
        elif client != None:
            client = client.split()
            week = Week.objects.get(user=User.objects.get(
                first_name=client[0], last_name=client[1]), phase=phase, week=week)
            days = week.days.all()
        else:
            days = None
            response = {
                'error': 'Could not load days!'
            }
            return JsonResponse(response)

        return render(request, 'trainerInterface/segments/dayTableDataProg.html', {'days': days.order_by('day')})
