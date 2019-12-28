from django import template
import sys
from Site.models import GameLine

register = template.Library()

@register.filter
def get_player_school(value):
    lines = list(GameLine.objects.filter(player_id=value))
    lines.sort(key=lambda x: x.date)
    return lines[-1].team_id