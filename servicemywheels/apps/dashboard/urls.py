from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = patterns('',

    url(r"^myprofile/", views.MyProfile.as_view(), name='myprofile'),
    url(r"^myorder/", views.MyOrder.as_view(), name='myorder'),
    url(r"^myaddress/", views.MyAddress.as_view(), name='myaddress'),
    url(r"^myvehicle/", views.MyVehicle.as_view(), name='myvehicle'),
    url(r"^test/", views.Test.as_view(), name='test')
)
