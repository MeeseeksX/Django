from atexit import register
from django.template import Library


register = Library()


@register.filter
def mod(num):
    return num%2 == 0


@register.filter
def mod_val(num, val):
    return num%val == 0

