import json
from django.template import Library
from django.utils.safestring import mark_safe
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
register = Library()
@register.filter
def tojson(obj):
    if isinstance(obj, QuerySet):
        return mark_safe(serialize('json', obj))
    return mark_safe(json.dumps(obj, cls=DjangoJSONEncoder))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def na_on_none(value):
    return value if value is not None else 'NA'
