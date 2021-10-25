from django import template
from api.models import *

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

def get_sets(entry):
    entryId = entry.id
    exerciseId = entry.exercise.id
    sets = Set_Entry.objects.filter(t_id=entryId, e_id=exerciseId)

    return sets


register.filter(get_sets)
register.filter(get_group)
register.filter(is_in)
register.filter(id_in)

