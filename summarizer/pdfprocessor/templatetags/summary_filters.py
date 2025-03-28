from django import template

register = template.Library()

@register.filter(name='count_entities')
def count_entities(value, entity):
    """Count occurrences of specific entities in summary"""
    if not value:
        return 0
    return value.count(str(entity))