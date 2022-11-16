import re
import json
from django.utils import timezone,six
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from rest_framework import serializers

class TZDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        tz = timezone.get_default_timezone()
        value = timezone.localtime(value, timezone=tz)
        return super(TZDateTimeField, self).to_representation(value)

class ChoiceTextField(serializers.ChoiceField):
    def __init__(self,choices,**kwargs):
        kwargs['read_only']=True
        super(ChoiceTextField,self).__init__(choices,**kwargs)

    def to_internal_value(self,data):
        raise ValueError('Cannot set value of ChoiceTextField')

    def to_representation(self,value):
        if value in ('', None):
            return ''
        return self.grouped_choices.get(value,'')

#Multi Choice field serializer
class SelectListSerializer(serializers.ListSerializer):
    def to_representation(self,data):
        if not isinstance(data, models.Manager):
            if data and data[0] != '':
                queryset = self.get_qset(data)
            else:                     
                queryset = [] 
        else:
            queryset = data
        return super(SelectListSerializer,self).to_representation(queryset)         
         
    def get_qset(self,data):                                      
        meta = self.child.__class__.Meta                            
        qset = getattr(meta,'qset',None)                            
        if qset is None:
            qset = meta.model.objects                               
        data = filter(lambda x: x.isdigit(),data)
        return qset.filter(id__in = data)

class KeyListSerializer(serializers.ListSerializer):
    def to_representation(self,data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        meta = self.child.__class__.Meta
        listkey = getattr(meta,'list_by_key','id')
        listkeyval = [getattr(item,listkey,None) for item in iterable]
        result = []
        for item in iterable:
            setattr(item,listkey+'_s',listkeyval)
            result.append(self.child.to_representation(item))
        return result

class UrlField(serializers.Field):
    def __init__(self,urlname,*args,**kwargs):
        self.urlname = urlname
        return super(UrlField,self).__init__(*args,**kwargs)
    def to_representation(self,value):
        if value.slug:
            return '%s' % reverse(self.urlname,args=[value.slug])
        return ""

class MobileField(serializers.CharField):
    default_error_messages = {
        'invalid': 'Enter Valid Mobile Number'
    }
    def __init__(self,**kwargs):
        super(MobileField,self).__init__(**kwargs)
        mregex = re.compile('^[789]\d{9}$')
        validator = RegexValidator(mregex,message=self.error_messages['invalid'])
        self.validators.append(validator)

class SerializerSet(serializers.Serializer):
    """
    @TODO: Move it to utils on multiple use case
    Validates and saves multiple serializer.On calling is_valid it validates against all child_serializer_classes
    Use Case:

    from common.api.leadapi import CreateLeadForm
    class RegisterSerializerSet(SerializerSet):
        course_category=serializers.ChoiceField(required=True,choices=CATEGORY_CHOICES)
        current_city = serializers.ChoiceField(required=True,allow_blank=True,choices=CITY_CHOICES)
        class Meta:
            fields = ('course_category','current_city')
            #these serializer instance can be accessed through self.createuserform,self.userleadmapform,self.createleadform
            child_serializer_classes = (CreateUserForm,UserLeadMapForm,CreateLeadForm,)
    """
    def __getattr__(self,name):
        data = self._childcache.get(name,None)
        if data is not None:
            return data
        return self.__getattribute__(name)
        
    def is_valid(self,raise_exception=False):
        errors={}
        self._childcache={}
        valid = super(SerializerSet,self).is_valid(raise_exception=False)
        #loop in reverse so that the errors of first gets preference
        #each child can be accessed through lowercased serializer name i.e. self.createuserform
        for child in reversed(self.Meta.child_serializer_classes):
            child_serializer=child(data=self.initial_data)
            if not child_serializer.is_valid():
                valid = False
                errors.update(child_serializer.errors)
            self._childcache[child.__name__.lower()]=child_serializer
        if valid:
            validated_data={}
            for child in reversed(self.Meta.child_serializer_classes):
                validated_data.update(self._childcache[child.__name__.lower()]._validated_data)
            validated_data.update(self._validated_data)
            self._validated_data = validated_data
            
        errors.update(self._errors)
        self._errors = errors
        if not valid and raise_exception:
            raise ValidationError(self.errors)
        return valid


    def save(self,**kwargs):
        """
        saves all the child serializer class
        """
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )
        for name,child in self._childcache.iteritems():
            child.save(**kwargs)
        return True

class JSONField(serializers.Field):
    default_error_messages = {
        'invalid': ('Value must be valid JSON.')
    }

    def __init__(self, *args, **kwargs):
        self.binary = kwargs.pop('binary', False)
        super(JSONField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            if data:
                data = json.dumps(data)
            else:
                data=''
        except (TypeError, ValueError):
            self.fail('invalid')
        return data

    def to_representation(self, value):
        if value:
            try:
                value=json.loads(value)
            except:
                value=None
        return value
