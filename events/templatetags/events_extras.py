from django import template

register = template.Library()

@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='times')
def times(number):
    return range(number)


@register.filter
def list_item(l, i):
    try:
        return l[i]
    except:
        return None