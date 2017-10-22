from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = patterns('',

    url(r"^saveaddress/", views.SaveAddress.as_view(), name='SaveAddress'),
)
