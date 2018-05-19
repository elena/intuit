"""project URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from inputs import views as inputs_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^projection/$',
        inputs_views.projection,
        name='projection',
    ),

    url(r'^projection/detail/$',
        inputs_views.projection_day,
        name='projection_day',
    ),


    url(r'^periods/$',
        inputs_views.WeekListView.as_view(),
        name='week_list',
    ),

    url(r'^period/(?P<pk>\d+)/$',
        inputs_views.WeekDetailView.as_view(),
        name='week_detail',
    ),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns