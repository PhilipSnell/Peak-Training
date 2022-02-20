from cmath import inf
from urllib import response
from django.http import HttpResponse, JsonResponse
from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
import numpy as np


def graphTracking(request):
    request.session["href"] = '/dashboard/graph/'
    newdate = date.today()

    return render(request, 'trainerInterface/graph.html', {'date': newdate})


def getData(request):
    if request.is_ajax():

        if "selected_client" in request.session:
            client = User.objects.get(email=request.session['selected_client'])
            groups = TrackingGroup.objects.filter(
                clientToggle=client)
            html_response = '<select>'
            for group in groups:
                for field in group.textfields.filter(clientToggle=client):

                    html_response = html_response+'<option value="' + \
                        field.name+'">'+field.name+'</option>'
            html_response = html_response+'</select>'
            # print(html_response)
        return HttpResponse(html_response)


def getGraphData(request):
    if request.is_ajax():
        option = request.POST.get('option', None)
        date = request.POST.get('date', None)
        date_time = datetime.strptime(date, '%d/%m/%Y')
        days = [date_time]
        for i in range(1, 7):
            days.append(date_time+timedelta(days=i))

        print(days)
        client = User.objects.get(email=request.session['selected_client'])
        groups = TrackingGroup.objects.filter(
            clientToggle=client)
        values = None
        for group in groups:
            for field in group.textfields.filter(clientToggle=client):
                if field.name == option:
                    print('ID')
                    print(field.id)
                    for value in field.values.all():
                        print(value.date)
                    print(date_time)
                    data_values = []
                    for date in days:
                        try:
                            data_values.append(field.values.get(
                                client=client, date=date).value)
                        except:
                            data_values.append('')
        maxVal = -inf
        minVal = inf

        for value in data_values:
            if value != '':
                value = float(value)
                if value < minVal:
                    minVal = value
                if value > maxVal:
                    maxVal = value

        # max to min is 80% of the displayed range
        range_80 = maxVal-minVal
        # calculate 10% so we can add to max and subtract from min
        range_10 = (range_80/10)*1.25
        display_max = maxVal+range_10
        display_min = minVal-range_10
        range_100 = display_max-display_min
        display_vals = np.linspace(
            minVal, display_max, 9, endpoint=False)
        display_vals = np.round(display_vals, 1).tolist()

        value_pos = []
        for value in data_values:
            if value != '':
                value = float(value)
                value_pos.append(str((value-display_min)*100/range_100)+"%")
            else:
                value_pos.append('0')

        response = {
            'data': data_values,
            'display': display_vals,
            'positions': value_pos
        }
        return JsonResponse(response)
