from rest_framework import generics
from relatedviews import mixins
class BaseAPIView(mixins.APIView):
    def fetch_related(self,*args,**kwargs):
        from shared.views import HeaderView
        if hasattr(self,'related_views'):
            self.related_views['header'] = (HeaderView.as_data(),)
        else:
            self.related_views={
                'header' : (HeaderView.as_data(),)
            }
        return super(BaseAPIView,self).fetch_related(*args,**kwargs)



