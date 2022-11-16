import urllib, types, sys, copy

from django.db import models
from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from django.core.cache import cache
from django.urls import reverse
from django.core.exceptions import FieldError

from rest_framework import status
from rest_framework.response import Response 
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from itertools import chain
from operator import itemgetter
from collections import Hashable as H


def register_as_module(cls, mod_name):
    '''
    Create a dynamic module from public members of a given class
    and set it to sys modules
    '''
    _cls_module = types.ModuleType(mod_name)
    _defined_field = [attr for attr in dir(cls) if not attr.startswith("_")]
    for field in _defined_field:
        setattr(_cls_module,field, getattr(cls,field))
    sys.modules.setdefault('%s.%s'%(cls.__module__,mod_name),_cls_module)

def register_as_proxy_model(model, manager=models.Manager, module='common.models', app_label='cms', write=False):
    '''
    Return a ProxyModel of a given Model if it is not already proxy and attach new manager object
    otherwise return same  model and also keep default manager as '_objects' attribute
    '''
    if model._meta.proxy:
        return model
    manager_obj = manager() if isinstance(manager,models.Manager) else manager(model=model)
    app_label = model._meta.app_label if write else app_label
    _Meta = type('Meta',(),{'proxy':True,'app_label':app_label})
    attrs = {
            'Meta': _Meta,
            '__module__': module,
            'objects': manager_obj,
            '_default_manager': manager_obj,
    }
    Klass = type('Proxy%s'%model.__name__,(model,),attrs)
    Klass._objects = model.objects
    return Klass

class BasicModelManager(models.Manager):
    '''
    Model Manager designed for basic business filters
    applied in all models of the project
    '''
    def __init__(self,*args,**kwargs):
        self._model = kwargs.pop('model',self.__class__)
        self.fields = self._model._meta.get_all_field_names()

        self.filters = dict()
        self._set_filter(show_on_site = True)
        self._set_filter(site = settings.SITE_ID)
        self._set_filter(sites = settings.SITE_ID)

        return super(BasicModelManager, self).__init__(*args,**kwargs)

    def _set_filter(self,*args,**kwargs):
        field = kwargs.keys().pop()
        if field in self.fields:
            self.filters.update(kwargs)

    def get_queryset(self):
        queryset = super(BasicModelManager, self).get_queryset()
        try:
            return queryset.filter(**self.filters)
        except FieldError:
            return queryset

    def __repr__(self):
        return '<%s Manager object from %s.%s>' %(self._model.__name__,self.__module__,self.__class__.__name__)

def cstolist(value):
    """convert comma separated values to list identifying proper type.List object remains unchanged """
    if value in (None,'',u''):
        return []
    if isinstance(value,(str,unicode)):
        #do typecasting
        rawvalues=value.split(',')
        if rawvalues[0].isdigit():
            value = [int(v) for v in rawvalues]
        else:
            value = [v for v in rawvalues]
    elif isinstance(value,(int,)):
        value=[value]
    return value
# needs refactoring for more generic form
def choicestodict(data,keys=None):
    '''
    convert django choices to list of dict by default containing text and value key.Pass keys for customization.
    Usage:
        a=[[1,'a'],[2,'b']]
        x=choicestodict(a)
        x = [{'value':1,'text':'a'},{'value':2,'text':'b'}]

        a=[[1,'a'],[2,'b']]
        x=choicestodict(a,['id','name'])
        x = [{'id':1,'name':'a'},{'id':2,'name':'b'}]

    Possible Use Cases:
        convert model choices to list of text,value pairs
        convert lms api data to list of id,name value pairs
    '''
    if not keys:
        keys = ['value','text']
    return list(map((lambda x: dict(zip(keys,x))),data))


def get_client_ip(request):
    """
    Return client IP from request META
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

class NoPagination(object):
    """ 
    Wraps data wrapped in a dict with key name 'results'.Return Response object.
    Use with pagination_class=NoPagination as view attribute 
    """
    display_page_controls = False
    def paginate_queryset(self,queryset,request,view=None):
        if isinstance(queryset,models.Manager):
            queryset=queryset.all()
        return list(queryset)

    def get_paginated_response(self,data):
        return Response({'results':data})

    def get_results(self, data):
        return data['results']



def is_valid_email(email):
    """
    Uses django internal validator to ensure that email validation remains same throughout the app
    """
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

from qna.models.details import SpamWords
def is_spammed(content):
    spammed = False
    content = content.lower()
    content += " " + content + " "
    spamtrie = cache.get('spam_trie')
    if not spamtrie:
        all_words = SpamWords.objects.all()
        spamword_list = []
        for word_obj in all_words:
            spamword_list.append(str(word_obj.word.lower()))
        spamtrie = spamword_list
        if cache.has_key('spam_trie'):
            cache.delete('spam_trie')
        cache.set('spam_trie', spamtrie)
    for x in spamtrie:
        if " " + x + " " in content:
            spammed = True
            break
    if spammed:
        return True
    else:
        return False

def namify(slug):
    if not slug:
        return ''
    return urllib.unquote(slug).decode('utf8').replace('-',' ').title()

class Memoized(object):
    excluded_renderer = ('api','json')

    def __init__(self, func):
        self._func = func
        self._cache = {}

    def _create_cache_key(self,args,kwargs,initkwargs):
        kwargs.update(initkwargs)
        hashable_kwargs = filter(lambda x,H=H: isinstance(x[1],H),kwargs.items())
        return hash(tuple(sorted(hashable_kwargs+[self._func.__name__])))
    
    def _get_set_cache(self,args,kwargs,cache_key):
        value = self._func(*args,**kwargs)
        cache_duration = getattr(self._func._class,'cache_duration',settings.CACHE_DURATION)
        cache.set(cache_key,value,cache_duration)
        return value

    def _memoize_renderer(self,request):
        return request.accepted_renderer.format not in self.excluded_renderer

    def __call__(self, *args, **kwargs):
        cache_key = self._create_cache_key(args,kwargs,self._func._initkwargs)
        cache_data = self._memoize_renderer(args[0]) and cache.get(cache_key)
        return cache_data or self._get_set_cache(args,kwargs,cache_key)

def exception_handler(exc, context):
    if not settings.DEBUG:
        request = context.get('request')
        exception_handled = (Http404,)

        if isinstance(exc,exception_handled):
            status_code = status.HTTP_404_NOT_FOUND
        else:
            status_code = getattr(exc,'status_code',status.HTTP_500_INTERNAL_SERVER_ERROR)
        request_urlconf = getattr(request,'urlconf','desktop.urls')
        root_urlconf = __import__(request_urlconf,fromlist=1)
        handler = getattr(root_urlconf,'handler%s' %status_code,None)
        cls = getattr(handler,'cls',type('clsview',(),{'template_name':'404.html'}))
        if not isinstance(context.get('view'),cls) and callable(handler):
            response = handler(request)
        else:
            response = render(request,cls.template_name,locals(),status=status.HTTP_501_NOT_IMPLEMENTED)
        return response

def toolsuploadpath(instance, filename):
    """ Computes the logo image upload path """
    return "uploads/files/tools/%s" % ( filename.replace(' ', '-'),)

def is_ajax(request):
    return request.query_params.get('ajax',None) or request.is_ajax()

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
