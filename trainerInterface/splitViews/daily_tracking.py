from trainerInterface.views import processForm, processDate, getUserform, is_ajax
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
from datetime import date


def dailyTracking(request):
    if is_ajax(request):
        newdate = date.today()
        return render(request, 'trainerInterface/dailyTracking.html', {'date': newdate})


# OLD

# def dailyTracking(request):
#     if request.method == "POST":
#         processForm(request)
#         if is_ajax(request):
#             processDate(request)

#     if "selected_client" in request.session:
#         currUserID = request.user.id
#         groups = TrackingGroup.objects.filter(trainer__id__in=[1, currUserID])
#         if 'date' in request.session:
#             newdate = date(
#                 *map(int, json.loads(request.session['date']).split('-')))

#         else:
#             newdate = date.today()
#         trackingVals = TrackingTextValue.objects.filter(client=User.objects.get(
#             email=request.session['selected_client']), date=newdate)
#     else:
#         groups = None
#         trackingVals = None

#     form = getUserform(request)

#     return render(request, 'trainerInterface/dailyTracking.html',
#                   {'form': form, 'groups': groups, 'selected_client': request.session['selected_client'],
#                    'trackingVals': trackingVals, 'date': newdate})
