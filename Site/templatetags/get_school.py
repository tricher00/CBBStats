from django import template
import sys
from Site.models import Team

register = template.Library()

@register.filter
def get_school(value):
    return Team.objects.get(id=value).name