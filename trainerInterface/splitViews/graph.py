from cmath import inf
import json
from urllib import response
from django.http import HttpResponse, JsonResponse
from trainerInterface.views import processForm, processDate, getUserform
from api.models import *
from trainerInterface.form import *
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
import numpy as np
import myfitnesspal as mfp

def graphTracking(request):
    request.session["href"] = '/dashboard/graph/'
    newdate = date.today()

    return render(request, 'trainerInterface/graph.html', {'date': newdate})


def getData(request):
    if request.is_ajax():

        if "selected_client" in request.session:
            client = User.objects.get(email=request.session['selected_client'])
            groups = TrackingGroup.objects.filter(clientToggle=client)
            try: 
                myfitnesspal = MyFitnessPal.objects.get(user=client)
                if myfitnesspal.connected:
                    admin = User.objects.get(email="admin@admin.com")
                    mfp_group = TrackingGroup.objects.filter(trainer=admin, name= "My Fitness Pal")
                    groups = groups.union(mfp_group)
            except MyFitnessPal.DoesNotExist:
                pass


            html_response = '<select>'
            for group in groups:
                html_response = html_response+'<option value="' + \
                    group.name+'">'+group.name+'</option>'
            html_response = html_response+'</select>'
            # print(html_response)
        return HttpResponse(html_response)


def getFields(request):
    if request.is_ajax():

        if "selected_client" in request.session:

            client = User.objects.get(email=request.session['selected_client'])

            selected_group = request.GET.get('group', None)
            group = TrackingGroup.objects.get(name=selected_group)

            fields = group.textfields.filter(clientToggle__in=[client]).order_by('id')
        return HttpResponse(render(request, 'trainerInterface/segments/graphgroupfields.html', {'fields': fields}))
        # html_response = ''
        #     for field in group.textfields.all():
        #         html_response = html_response+'<div class="group-field">'+field.name+'</div>'

        # return HttpResponse(html_response)


def getGraphData(request):
    if request.is_ajax():
        # try:
        field_ids = json.loads(request.POST.get('fields', None))["fields"]
        date = request.POST.get('date', None)
        date_time = datetime.strptime(date, '%d/%m/%Y')
        days = []
        days = [date_time]
        for i in range(1, 7):
            days.append(date_time+timedelta(days=i))
        response = {}
        client = User.objects.get(email=request.session['selected_client'])
        fields = TrackingTextField.objects.filter(id__in=field_ids).order_by('id')
        print(datetime.now())
        if fields[0] in MyFitnessPalFields.objects.get(id=1).fields.all():
            try:
                mfp_details = MyFitnessPal.objects.get(user=client)
            except MyFitnessPal.DoesNotExist:
                response['error'] = "My Fitness Pal log in for " +client.first_name + " " +client.last_name + " not found!"
                JsonResponse(response)
            try:
                mfpclient = mfp.Client(mfp_details.username)
            except Exception as e:
                response['error'] = str(e)
                JsonResponse(response)
            for day in days:
                values = fields[0].values.filter(date=day)
                if len(values)==0 and day < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                    
                    mfp_fields = MyFitnessPalFields.objects.get(id=1).fields.all().order_by('id')
                    

                    data=mfpclient.get_date(day.year,day.month,day.day)
                    print(data)
                    try:
                        calories = TrackingTextValue(
                            value=data.totals['calories'],
                            client=client,
                            field_id=mfp_fields[0].id,
                            date=day
                        )
                        calories.save()
                        fields[0].values.add(calories)
                    except KeyError:
                        print(KeyError)
                        pass
                    try:
                        protein = TrackingTextValue(
                            value=data.totals['protein'],
                            client=client,
                            field_id=mfp_fields[1].id,
                            date=day
                        )
                        protein.save()
                        fields[1].values.add(protein)
                    except KeyError:
                        print(KeyError)
                        pass
                    try:
                        carbs = TrackingTextValue(
                            value=data.totals['carbohydrates'],
                            client=client,
                            field_id=mfp_fields[2].id,
                            date=day
                        )
                        carbs.save()
                        fields[2].values.add(carbs)
                    except KeyError:
                        print(KeyError)
                        pass
                    try:
                        fat = TrackingTextValue(
                            value=data.totals['fat'],
                            client=client,
                            field_id=mfp_fields[3].id,
                            date=day
                        )
                        fat.save()
                        fields[3].values.add(fat)
                    except KeyError:
                        print(KeyError)
                        pass
                    try:
                        sodium = TrackingTextValue(
                            value=data.totals['sodium'],
                            client=client,
                            field_id=mfp_fields[4].id,
                            date=day
                        )
                        sodium.save()
                        fields[4].values.add(sodium)
                    except KeyError:
                        print(KeyError)
                        pass
                    try:
                        sugar = TrackingTextValue(
                            value=data.totals['sugar'],
                            client=client,
                            field_id=mfp_fields[5].id,
                            date=day
                        )
                        sugar.save()
                        fields[5].values.add(sugar)
                    except KeyError:
                        print(KeyError)
                        pass

        # print(fields)
        # for group in groups:
        #     for field in group.textfields.filter(clientToggle=client):
        # if field.name == option:
        
        data = []
        y_axis = []
        data_y_pos = []
        for field in fields:


            data_values = []
            for date in days:
                try:
                    data_values.append(field.values.get(
                        client=client, date=date).value)
                except:
                    data_values.append('')
            data.append(data_values)

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
            if minVal != maxVal:
                display_vals = np.linspace(
                    minVal, display_max, 9, endpoint=False)
                display_vals = np.round(display_vals, 1).tolist()
            else:
                display_vals = [np.round(minVal-minVal/10, 1), "", "", "",
                                minVal, "", "", "", np.round(minVal+minVal/10, 1)]
            display_vals.reverse()
            if display_vals[0] != display_vals[0]:
                display_vals = ["", "", "", "", "", "", "", "", "", ""]

            y_axis.append(display_vals)

            value_pos = []
            for value in data_values:
                if value != '':
                    value = float(value)
                    if range_100 == 0:
                        value_pos.append("50%")
                    else:
                        value_pos.append(
                            str((value-display_min)*100/range_100)+"%")
                else:
                    value_pos.append('0')
            data_y_pos.append(value_pos)

        

        response['datavals']= data
        response['y_axis'] = y_axis
        response['data_y_pos'] = data_y_pos
        
        # except:
        #     response = {
        #         'error': 'Could not load data'
        #     }
        print(response)
        return JsonResponse(response)


def linkValues(request):

    calories = TrackingTextField.objects.get(name='Calories')
    print(calories.id)
    # values = TrackingTextValue.objects.all()
    # for value in values:
    #     field = TrackingTextField.objects.get(id=value.field_id)
    #     field.values.add(value)
    #     field.save()

    return redirect('home')
