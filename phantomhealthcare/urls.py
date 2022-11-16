"""phantomhealthcare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.urls import include, path, re_path

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
    path('',include('product.urls')),
    path('',include('post.urls')),
    path('',include('shared.urls')),
    path('',include('service.urls')),
    path('',include('lead.urls')),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)), 
    ] + urlpatterns
