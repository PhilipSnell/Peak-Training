from django import template
from api.models import *
from django.db import models

register = template.Library()


def is_in(case, accounts):
    for element in accounts:
        if element.email == case:
            return True
    return False


def id_in(case, trackingVals):
    for trackingVal in trackingVals:
        if case == trackingVal.field_id:
            return trackingVal.value

    return ""


def get_group(id):
    group = TrackingGroup.objects.get(id=id)
    return group.name


class Set(models.Model):
    set = models.IntegerField()
    reps = models.CharField(max_length=300)
    weights = models.CharField(max_length=300)


def get_sets(entry):
    entryId = entry.id
    exerciseId = entry.exercise.id
    sets = []
    # try:
    set_entry = Set_Entry.objects.filter(t_id=entryId, e_id=exerciseId)
    if set_entry.count() > 0:

        reps = set_entry[0].reps.split(",")
        weights = set_entry[0].weights.split(",")

        for i in range(set_entry[0].sets):
            set = Set(
                set=i+1,
                reps=reps[i],
                weights=weights[i]
            )
            if reps[i] != '-1':
                sets.append(set)

    # except:
    #     print('no sets')
    return sets


def sliceVideo(video):

    return video[-11:]+"/0.jpg"


def get_feedback(id):
    try:
        feedback = SetFeedback.objects.get(t_id=id)
        if feedback.comment == "###":
            feedback.comment = ""
    except:
        feedback = None
    return feedback


def getActiveWeek(client):
    week = Week.objects.filter(user=client, isActive=True)
    if week:
        return week[0]
    return


def completed(week):

    days = week.days.all()
    completed_days = 0
    for day in days:
        exercises = day.entrys.all()
        for exercise in exercises:
            entrys = Set_Entry.objects.filter(t_id=exercise.id)
            if len(entrys) > 0:
                completed_days += 1
                break

    return completed_days


register.filter(completed)
register.filter(getActiveWeek)
register.filter(get_feedback)
register.filter(sliceVideo)
register.filter(get_sets)
register.filter(get_group)
register.filter(is_in)
register.filter(id_in)
