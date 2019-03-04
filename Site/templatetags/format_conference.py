from django import template

register = template.Library()

@register.filter
def format_conference(value):
    if value == "ivy":
        return "Ivy"
    elif value == "pac-12":
        return "Pac-12"
    if len(value) == 3 or len(value) == 4:
        return value.upper()    
    else:
        return value.replace("-", " ").title()