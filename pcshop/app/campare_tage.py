from django import template

register = template.Library()

@register.filter
def is_selected(option, current):
    return option == current