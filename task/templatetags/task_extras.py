from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from task.models import Task


user_model = get_user_model()
register = template.Library()

# @register.filter
# def auth_user(user):
#     if user