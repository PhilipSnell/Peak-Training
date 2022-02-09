from collections import defaultdict
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from api.models import ExerciseType
from .form import *

import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from bootstrap_modal_forms.generic import BSModalCreateView
from datetime import date
from django.utils.dateparse import parse_date

User = get_user_model()


def processDate(request):
    newdate = parse_date(json.loads(request.POST.get('date', None))["date"])
    request.session["date"] = json.dumps(
        newdate, indent=4, sort_keys=True, default=str)


def processForm(request):

    # Get the posted form
    ClientSelect = UserForm(request.POST, request=request)
    if ClientSelect.is_valid():
        selected_client = ClientSelect.cleaned_data["selected_client"]
        print(selected_client.email)
        request.session["selected_client"] = selected_client.email


def getUserform(request):
    if "selected_client" in request.session:
        form = UserForm(initial={'selected_client': User.objects.get(
            email=request.session['selected_client'])}, request=request)
        form.fields["selected_client"].empty_label = None
    else:
        form = UserForm(request=request)
    return form


def home(request):
    if request.method == "POST":
        processForm(request)

    form = getUserform(request)
    return render(request, 'trainerInterface/home.html', {'form': form})


@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def dashboard(request):
    if request.method == "POST":
        processForm(request)

    form = getUserform(request)
    if request.is_ajax():
        return render(request, 'trainerInterface/dashboard-ajax.html', {'form': form})
    else:
        return render(request, 'trainerInterface/dashboard.html', {'form': form})


def clients(request):
    if request.method == "POST":
        processForm(request)

    form = getUserform(request)
    trainer = Trainer.objects.get(trainer=request.user)

    return render(request, 'trainerInterface/clients.html', {'form': form, 'clients': trainer.clients.all()})


def cloneWeek(request):
    user = User.objects.get(email=request.session['selected_client'])
    if request.is_ajax():
        phaseFromNum = request.POST.get('phaseFrom', None)
        weekFromNum = request.POST.get('weekFrom', None)
        phaseToNum = request.POST.get('phaseTo', None)
        weekToNum = request.POST.get('weekTo', None)
        # try:
        phaseFrom = Phase.objects.get(user=user,
                                      phase=phaseFromNum)
        weekFrom = phaseFrom.weeks.get(week=weekFromNum, user=user)

        phaseTo = Phase.objects.get(user=User.objects.get(email=request.session['selected_client']),
                                    phase=phaseToNum)
        weekTo = phaseTo.weeks.get(week=weekToNum, user=user)

        # Clear all current days
        for day in weekTo.days.all():
            for entry in day.entrys.all():
                entry.delete()
            day.delete()
        copiedDays = []
        for day in weekFrom.days.all():
            copiedEntrys = []
            for entry in day.entrys.all():
                copiedEntry = TrainingEntry(
                    user=User.objects.get(
                        email=request.session['selected_client']),
                    phase=weekTo.phase,
                    week=weekTo.week,
                    day=day.day,
                    reps=entry.reps,
                    weight=entry.weight,
                    sets=entry.sets,
                    comment=entry.comment,
                    exercise=entry.exercise
                )
                copiedEntry.save()
                copiedEntrys.append(copiedEntry)
            copiedDay = Day(
                phase=weekTo.phase,
                week=weekTo.week,
                day=day.day,
                user=user
            )
            copiedDay.save()
            copiedDay.entrys.add(*copiedEntrys)
            copiedDay.save()
            copiedDays.append(copiedDay)
        weekTo.days.add(*copiedDays)
        weekTo.save()
        # except:

    return redirect('trainplan')


@user_passes_test(lambda user: user.is_trainer, login_url='/login/')
def dataTracking(request):
    if request.method == "POST":
        processForm(request)

    if "selected_client" in request.session:
        currUserID = request.user.id
        groups = TrackingGroup.objects.filter(trainer__id__in=[1, currUserID])
    else:
        groups = None
    # TrackingGroup.objects.all().delete()
    form = getUserform(request)
    addGroupForm = GroupAddForm()
    addFieldForm = GroupFieldForm()
    return render(request, 'trainerInterface/dataTracking.html', {'form': form, 'groups': groups, 'addGroupForm':
                                                                  addGroupForm, 'addFieldForm': addFieldForm, 'selected_client': request.session['selected_client']})


def editGroup(request):

    if request.is_ajax():
        groupId = request.POST.get('groupId', None)
        name = request.POST.get('name', None)
        fieldIds = json.loads(request.POST.get('fieldIds', None))['fieldIds']
        fieldnames = json.loads(request.POST.get(
            'fieldnames', None))["fieldnames"]
        fieldSelects = json.loads(request.POST.get(
            'classifications', None))["classifications"]
        toggles = json.loads(request.POST.get('toggles', None))["toggles"]

        editGroup = TrackingGroup.objects.get(id=groupId)
        editGroup.name = name
        editGroup.save()

        for id, fieldname, fieldselect, toggle in zip(fieldIds, fieldnames, fieldSelects, toggles):
            print(id)
            if not id:

                if fieldselect == 'text':
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=False,
                    )
                else:
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=True,
                    )

                if toggle == 'True':
                    new_field.save()
                    new_field.clientToggle.add(User.objects.get(
                        email=request.session['selected_client']))

                new_field.save()
                editGroup.textfields.add(new_field)
                editGroup.save()
            elif 'delete' in id:
                TrackingTextField.objects.get(id=id[0]).delete()

            else:
                editField = TrackingTextField.objects.get(id=id)
                editField.name = fieldname
                if toggle == 'True':
                    editField.clientToggle.add(User.objects.get(
                        email=request.session['selected_client']))
                else:
                    editField.clientToggle.remove(User.objects.get(
                        email=request.session['selected_client']))
                if fieldselect == 'text':
                    editField.type = False
                else:
                    editField.type = True
                editField.save()
                editGroup.textfields.add(editField)
                editGroup.save()

    return redirect('trainprog')


def addGroup(request):

    if request.is_ajax():
        name = request.POST.get('name', None)
        fieldnames = json.loads(request.POST.get(
            'fieldnames', None))["fieldnames"]
        fieldSelects = json.loads(request.POST.get(
            'classifications', None))["classifications"]
        toggles = json.loads(request.POST.get('toggles', None))["toggles"]
        print(fieldSelects)
        try:

            new_group = TrackingGroup(
                name=name,
                trainer=request.user,
            )
            new_group.save()
            for fieldSelect, fieldname, toggle in zip(fieldSelects, fieldnames, toggles):
                if fieldSelect == "text":
                    new_field = TrackingTextField(
                        name=fieldname,
                        type=False,
                    )

                    if toggle == 'True':
                        new_field.save()
                        new_field.clientToggle.add(User.objects.get(
                            email=request.session['selected_client']))

                    new_field.save()
                else:

                    new_field = TrackingTextField(
                        name=fieldname,
                        type=True,
                    )

                    if toggle == 'True':
                        new_field.save()
                        new_field.clientToggle.add(User.objects.get(
                            email=request.session['selected_client']))
                    new_field.save()
                new_group.textfields.add(new_field)
                new_group.save()

            print("saved")
            response = {
                'msg': 'Your form has been submitted successfully'  # response message
            }

        except:
            print("not saved")
            response = {
                'msg': 'Your form has not been saved'  # response message
            }
    return redirect('dataTracking')
