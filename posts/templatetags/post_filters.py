from django import template

register = template.Library()


@register.filter(name='shorten')
def shorten(content, rows: int):
    split_content = content.split('\n')
    new_content = ""
    for fragment in split_content[:rows]:
        new_content += fragment + "\n"
    return new_content
