from datetime import datetime
from django import template
register = template.Library()
@register.filter(is_safe=True)
def date_filter(value):
    if not value:return ''
    return datetime.strptime(str(value).split('T')[0],'%Y-%m-%d')
