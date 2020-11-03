from django import template

register = template.Library()


@register.filter(name='concept')
def concept(content):
    return content[:30]
