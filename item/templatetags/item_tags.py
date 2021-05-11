from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def rounded_timesince(value, delimiter=None):
    """
    .
    """
    if value.split()[0] in ['1', '0'] and value.split()[1] in ['minutes', 'minute']:
        return 'just now' 
    return f"{value.split(delimiter)[0]} ago"

@register.filter(is_safe=True)
@stringfilter
def rounded_timesince_min(value, delimiter=None):
    """
    .
    """
    time_chunk = value.split(delimiter)
    x = time_chunk[0]
    try:
        y = time_chunk[1]
        digit_date = x.split()[0]
        letter_date = x.split()[1][0]
        if x.split()[1] in ['years', 'year']:
            if y.split()[1]:
                digit_date = int(x.split()[0]) * 48 + int(y.split()[0]) * 4
            else:
                digit_date = int(x.split()[0]) * 48 
            return f'{digit_date}w'    

        if x.split()[1] in ['months', 'month']:
            if y.split()[1]:
                digit_date = int(x.split()[0]) * 4 + int(y.split()[0])
            else:
                digit_date = int(x.split()[0]) * 4 
            return f'{digit_date}w'    
    except:
        y = None
        digit_date = value.split()[0]
        letter_date = value.split()[1][0]  

    if value.split()[0] in ['1', '0'] and value.split()[1] in ['minutes', 'minute']:
        return 'just now'       
    return f'{digit_date}{letter_date}'
