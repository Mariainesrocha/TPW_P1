from django import template
from django.contrib.auth.models import Group
from TechSekai.views import *

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def addstr(arg1=None, arg2=None):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter(name='split')
def split(value, key):
    return value.split(key)

