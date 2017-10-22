from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = patterns('',

    url(r"^booking/", views.Booking.as_view(), name='booking'),
    url(r"^confirmorder/", views.ConfirmOrder.as_view(), name='confirmorder'),
    url(r"^savebooking/", views.SaveBooking.as_view(), name='savebooking'),
    url(r"^yourorder/", views.YourOrder.as_view(), name='Yourorder'),
    url(r"^sendmail/", views.SendMail.as_view(), name='sendmail'),

)
