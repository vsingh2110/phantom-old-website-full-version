from django.db import models
from rest_framework.response import Response 

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

