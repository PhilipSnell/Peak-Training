from django import template

register = template.Library()

@register.filter(name='insert')
def insert(value, arg):
    print("entered")
    return value