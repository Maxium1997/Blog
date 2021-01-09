from django import template

register = template.Library()


@register.filter(name='shorten')
def shorten(content, rows: int):
    split_content = content.split('\n')
    new_content = ""
    for fragment in split_content[:rows]:
        new_content += fragment + "\n"
    return new_content


@register.filter(name='hide_mail')
def hide_mail(email):
    split_mail = email.split('@')
    fragment1 = split_mail[0][:3] + "*****"
    fragment2 = split_mail[1]
    return fragment1 + '@' + fragment2
