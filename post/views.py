from django.shortcuts import render

# Create your views here.
from relatedviews import mixins
from relatedviews.filters import MutableDjangoFilterBackend,OrderBackend,CountBackend

from relatedviews.pagination import NoPagination

from .models import Post
from .serializers import PostListSerializer,PostDetailSerializer

class PostListView(mixins.ListAPIView):
    queryset = Post.objects.filter(show_on_site=True).order_by('-publish_date')
    serializer_class = PostListSerializer
    pagination_class = NoPagination
    filter_backends = (MutableDjangoFilterBackend,CountBackend,)

class PostDetailView(mixins.RetrieveAPIView):
    queryset = Post.objects.filter(show_on_site=True)
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


from core.views import BaseAPIView 
class PostListBaseView(BaseAPIView):
    template_name = "post/post-list.html"
    related_views={
        'posts' : (PostListView.as_data(),),
        'recent_posts':(PostListView.as_data(),),
    }

class PostDetailBaseView(BaseAPIView):
    template_name = "post/post-detail.html"
    related_views = {
        'post': (PostDetailView.as_data(),'slug'),
        'recent_posts':(PostListView.as_data(),),
    }
    
