from django import template

register = template.Library()

@register.filter
def format_school(value):
    if "-am-" in value or value.endswith("-am"):
        value = value.replace("-am", "-a&m")
    if "-at-" in value or value.endswith("-at"):
        value = value.replace("-at", "-a&t")
    return value.replace("-", " ").title()