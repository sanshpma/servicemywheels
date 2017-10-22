from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = patterns('',
    url(r"^signup/", views.Signup.as_view(), name='signup'),
    url(r"^login/", views.UserLogin.as_view(), name='login'),
    url(r"^logout/", views.UserLogout.as_view(), name='logout'),
    url(r"^facebook_login/", views.FacebookLogin.as_view(), name='fb_login'),
    url(r"^google_login/", views.GoogleLogin.as_view(), name='google_login'),
    url(r"^login_google/", views.LoginGoogle.as_view(), name='login_google'),
    url(r"^login_fb/", views.LoginFb.as_view(), name='login_fb'),
    url(r"^forgot_password/", views.ForGotPassword.as_view(), name='forgot_password'),
    url(r"^verify_otp/", views.VerifyOtp.as_view(), name='verify_otp'),
    url(r"^re_send_otp/", views.ResendOtp.as_view(), name='resend_otp'),
    url(r"^guestUser/", views.GuestUser.as_view(), name='guest_user'),
    url(r"^set_password/", views.SetPassword.as_view(), name='set_password'),
    url(r"^send_mail/", views.SendMail.as_view(), name='send_mail'),
)
