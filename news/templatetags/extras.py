from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='get_val')
def get_val(datet):
    date = [int(d) for d in datet.replace("-"," ").replace("T"," ").replace("Z","").replace(":"," ").split(" ")]
    return datetime(year=date[0],month=date[1],day=date[2],hour=date[3],minute=date[4],second=date[5])

@register.filter(name='toStr')
def toStr(number):
    print(number)
    if number==0:
        return ''
    if number >= 1000000000:  # Billion
        return str(number // 1000000000) + "B"
    elif number >= 1000000:  # Million
        return str(number // 1000000) + "M"
    elif number >= 1000:     # Thousand
        return str(number // 1000) + "K"
    else:
        return str(number)