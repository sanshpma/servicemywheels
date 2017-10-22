from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = patterns('',

    url(r"^newOrderNotification/", views.NewOrderNotification.as_view(), name='newOrderNotification'),
    url(r"^searchorder/", views.SearchOrder.as_view(), name='searchOrder'),
)