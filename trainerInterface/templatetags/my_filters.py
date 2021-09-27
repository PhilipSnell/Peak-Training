from django import template
from api.models import TrackingGroup

register = template.Library()


def is_in(case, accounts):
    for element in accounts:
        if element.email == case:
            return True
    return False

def get_group(id):
    group = TrackingGroup.objects.get(id=id)
    print(group.name)
    return group.name
register.filter(get_group)
register.filter(is_in)

