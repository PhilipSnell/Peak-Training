from django import template
from api.models import *
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

register = template.Library()


def check_link(username):
    try:
        trainer = User.objects.get(username=username)
    except:
        return False
    try:
        trainer = Trainer.objects.get(trainer=trainer)
    except:
        return False
    return True


register.filter(check_link)
