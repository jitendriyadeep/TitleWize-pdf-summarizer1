# pdfprocessor/templatetags/highlight.py
from django import template
from django.utils.html import escape, mark_safe

register = template.Library()

@register.filter
def highlight(text, query):
    text = escape(text)
    if query:
        query = escape(query)
        return mark_safe(text.replace(query, f'<mark>{query}</mark>'))
    return text