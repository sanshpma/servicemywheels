from django.conf.urls import patterns, include, url
from django.contrib import admin
from website import views as website_views

handler404 = 'common.utils.handler404'
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'serviceMyWheels.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^website/', include("website.urls")),
    url(r'^$', website_views.Booking.as_view(), name='booking'),
    url(r'^staff/', include("staff.urls")),
    url(r'^dashboard/', include("dashboard.urls")),
    url(r'^auth/', include("registration.urls")),
    url(r'^users/', include("users.urls")),

)
