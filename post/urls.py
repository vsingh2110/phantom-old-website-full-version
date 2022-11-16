from django.conf.urls import include, url
from .views import PostListBaseView,PostDetailBaseView

urlpatterns = [
    url('^post/(?P<slug>[-\w]+)/$',PostDetailBaseView.as_view(),name="post_detail"),
    url('^post/$',PostListBaseView.as_view(),name="post_list")
]

