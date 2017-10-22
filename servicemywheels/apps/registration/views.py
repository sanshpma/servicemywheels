from django.shortcuts import render
from rest_framework.views import APIView
from forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from facebook import *
from googlePlus import *
from django.views.decorators.csrf import csrf_exempt
from core.models import Customers
from core.models import SendMailLink
from django.utils.decorators import method_decorator
import json
from core import models
import pyotp
from core import const
from django.core.mail import EmailMessage
import requests
from django.conf import settings
import time
import calendar
import datetime
from django.contrib.auth.models import User
from common import stringutility
from django.template import loader, Context

profile_track = None
getFacebook = FacebookOauthClient(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
getGoogle = GooglePlus(settings.GOOGLE_PLUS_APP_ID, settings.GOOGLE_PLUS_APP_SECRET)

class Signup(APIView):

    # def get(self, request, *args, **kwargs):
    #     registered = False
    #     user_form = UserForm()
    #     return render(request,
    #                   'signup.html',
    #                   {'user_form': user_form, 'registered': registered})
    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.POST.get('email')
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            email = request.POST.get('email')
            password = request.POST.get('password')
            new_user = authenticate(username=email, password=password)
            login(request, new_user)
            msg = {'status': 'done'}
            return HttpResponse(json.dumps(msg))
        else:
            msg = {'status': user_form.errors["email"]}
            return HttpResponse(json.dumps(msg))

class GuestUser(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
            customer_name = request.POST.get('customer_name')
            email = request.POST.get('email')
            password = "123456"
            try:
                user = Customers.objects.get(email=email)
                context = {"status": "Account with this email already exists! Please click on forgot password"}
                return HttpResponse(json.dumps(context))
            except:
                new_user = Customers.objects.create_user(email, password)
                new_user.customer_name = customer_name
                new_user.save()
                user = authenticate(email=email, password=password)
            login(request, user)
            context = {"status": "success"}
            return HttpResponse(json.dumps(context))

class UserLogin(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        return render(request, 'login.html', {})

    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                msg = {'status': 'done'}
                return HttpResponse(json.dumps(msg))
            else:
                return HttpResponse("Your  account is disabled.")
        else:
            msg = {'status': 'failed'}
            return HttpResponse(json.dumps(msg))


class FacebookLogin(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        global profile_track
        profile_track = 'facebook'
        facebook_url = getFacebook.get_authorize_url()
        return HttpResponseRedirect(facebook_url)


class GoogleLogin(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        global profile_track
        profile_track = 'google'
        google_url = getGoogle.get_authorize_url()
        return HttpResponseRedirect(google_url)


class AfterLogin(APIView):
    template_name = "home.html"
    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if not request.user.is_active:
                if request.GET.items():
                    if profile_track == 'facebook':
                        if 'code' not in request.GET.keys():
                            return render(request, 'login.html', {})
                        code = request.GET['code']
                        getFacebook.get_access_token(code)
                        userinfo = getFacebook.get_user_info()
                        full_name = userinfo['name']
                        fb_uid = userinfo['id']
                        username = fb_uid+'@withfacebook.com'
                        password = fb_uid+'_fb'+'8ats10r'

                        try:
                            user = Customers.objects.get(email=username)
                        except:
                            new_user = Customers.objects.create_user(username,password)
                            new_user.set_password(password)
                            new_user.save()

                        user = authenticate(email=username, password=password)
                        login(request, user)

                    elif profile_track == 'google':
                        if 'code' not in request.GET.keys():
                            return render(request, 'login.html', {})
                        code = request.GET['code']
                        state = request.GET['state']
                        getGoogle.get_access_token(code, state)
                        userinfo = getGoogle.get_user_info()
                        first_name = userinfo['given_name']
                        last_name = userinfo['family_name']
                        gmail_uid = userinfo['id']
                        username = gmail_uid+'@withgoogleplus.com'
                        password = gmail_uid+'_gmail'+'8r69et2'
                        try:
                            user = Customers.objects.get(email=username)
                        except :
                            new_user = Customers.objects.create_user(username,password)
                            new_user.set_password(password)
                            new_user.save()
                        user = authenticate(email=username , password=password)
                        login(request, user)


class UserLogout(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/website/booking')


class LoginGoogle(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.POST.get('email')
        password = '123456'
        name = request.POST.get('name')
        social_id = request.POST.get('social_id')
        etag = request.POST.get('etag')
        customesr_obj = Customers.objects.filter(email=email)
        if not customesr_obj:
            new_user = Customers.objects.create_user(email, password)
            new_user.set_password(password)
            new_user.customer_name = name
            new_user.social_id = social_id
            new_user.token_etag = etag
            new_user.from_login = "google"
            new_user.save()
        user = Customers.objects.get(email=email)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        msg = {'status': 'done'}
        return HttpResponse(json.dumps(msg))

class LoginFb(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.POST.get('email')
        password = '123456'
        name = request.POST.get('name')
        social_id = request.POST.get('social_id')
        etag = request.POST.get('etag')
        if not stringutility.is_not_null_empty(email):
            email = social_id + "@dummyfbemail.com"
        customesr_obj = Customers.objects.filter(email=email)
        if not customesr_obj:
            new_user = Customers.objects.create_user(email, password)
            new_user.set_password(password)
            new_user.customer_name = name
            new_user.social_id = social_id
            new_user.token_etag = etag
            new_user.from_login = "facebook"
            new_user.save()
        user = Customers.objects.get(email=email)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        msg = {'status': 'done'}
        return HttpResponse(json.dumps(msg))


class ForGotPassword(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        return render(request, "test.html", {})

    @method_decorator(csrf_exempt)
    def post(self, request):
        request.session["otp_count"] = 1
        customer_mail_or_mobile = request.DATA.get('mail_mobile').split('@')
        is_user_exists = 0
        if len(customer_mail_or_mobile) > 1:
            customer_mail_id = request.DATA.get('mail_mobile')
            all_user_obj = models.Customers.objects.all()
            for obj in all_user_obj:
                if obj.email == customer_mail_id:
                    is_user_exists = 1
                    customer_registered_mobile_number = models.Customers.objects.get(email=customer_mail_id).registered_phone
                    request.session["customer_mail_id"] = customer_mail_id
                    request.session["customer_registered_mobile_number"] = customer_registered_mobile_number
                    break
        else:
            customer_registered_mobile_number = request.DATA.get('mail_mobile')
            all_user_obj = models.Customers.objects.all()
            for obj in all_user_obj:
                if obj.registered_phone == customer_registered_mobile_number:
                    is_user_exists = 1
                    customer_mail_id = models.Customers.objects.get(registered_phone=customer_registered_mobile_number).email
                    request.session["customer_mail_id"] =customer_mail_id
                    request.session["customer_registered_mobile_number"] = customer_registered_mobile_number
                    break
        message = {'status': 'error'}
        if not is_user_exists:
            return HttpResponse(json.dumps(message))
        else:
            if "otp_count" not in request.session:
                request.session["otp_count"] = 1
            else:
                request.session["otp_count"] += 1
            if request.session["otp_count"] <= 10:
                message = {'status': 'success'}
                return HttpResponse(json.dumps(message))
            else:
                message = {"status": "Message sent is increased for this user"}
                return HttpResponse(json.dumps(message))

class VerifyOtp(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        customer_email_id = request.session["customer_mail_id"]
        customer_registered_mobile_number = request.session["customer_registered_mobile_number"]
        customer_registered_mobile_number = customer_registered_mobile_number[0:len(customer_registered_mobile_number)-5]
        context = {"status": "success", "customer_email_id": customer_email_id, "customer_registered_mobile_number": customer_registered_mobile_number}
        return HttpResponse(json.dumps(context))

class ResendOtp(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        customer_mail_id = request.session["customer_mail_id"]
        customer_registered_mobile_number = request.session["customer_registered_mobile_number"]
        request.session["otp_count"] += 1
        if request.session["otp_count"] <= 10:
            message = {'status': 'success'}
            return HttpResponse(json.dumps(message))
        else:
            message = {"message": "Message sent is increased for this user"}
            return HttpResponse(json.dumps(message))

    @method_decorator(csrf_exempt)
    def post(self,request):
        one_time_password = request.DATA.get('one_time_password')
        customer_mail_id = request.session["customer_mail_id"]
        new_password = request.DATA.get('new_password')
        one_time_password_from_session = request.session["otp"]
        if one_time_password != one_time_password_from_session:
            context = {'message': 'error'}
            return HttpResponse(json.dumps(context))
        else:
            user_obj = Customers.objects.get(email=customer_mail_id)
            user_obj.set_password(new_password)
            user_obj.save()
            user = Customers.objects.get(email=customer_mail_id)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            context = {'message': 'success'}
            return HttpResponse(json.dumps(context))

class SetPassword(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        customer_email = request.GET['email']
        epoch_time = request.GET['epoch_time']
        return render(request, "changepassword.html", {"customer_email": customer_email, "epoch_time": epoch_time})

    @method_decorator(csrf_exempt)
    def post(self, request):
        customer_email = request.DATA.get('customer_email')
        epoch_time = int(request.DATA.get('epoch_time'))
        new_password = request.DATA.get('new_password')
        try:
            SendMailLink.objects.get(email=customer_email, email_epoch_time=epoch_time)
            self.delete_send_mail(epoch_time)
            customer_obj = Customers.objects.get(email=customer_email)
            customer_obj.set_password(new_password)
            customer_obj.save()
            SendMailLink.objects.filter(email=customer_email).delete()
            user = authenticate(email=customer_email, password=new_password)
            login(request, user)
            context = {"message": "success"}
            return HttpResponse(json.dumps(context))
        except:
            context = {"message": "failed"}
            return HttpResponse(json.dumps(context))

    @method_decorator(csrf_exempt)
    def delete_send_mail(self, epoch_time):
            send_mail_obj_list = SendMailLink.objects.all()
            epoch_time = time.gmtime(epoch_time)
            epoch_time = time.mktime(epoch_time)
            for obj in send_mail_obj_list:
                send_mail_epoch_time = obj.email_epoch_time
                send_mail_epoch_time = time.gmtime(send_mail_epoch_time)
                send_mail_epoch_time = time.mktime(send_mail_epoch_time)
                diff_time = abs(epoch_time-send_mail_epoch_time)
                if diff_time >=3600:
                    obj.delete()

class SendMail(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
         customer_registered_mobile = request.session["customer_registered_mobile_number"]
         customer_mail_id = request.session["customer_mail_id"]
         epoch_time = calendar.timegm(time.gmtime())
         send_mailobj = models.SendMailLink()
         customer_obj = models.Customers.objects.get(email=customer_mail_id)
         send_mailobj.customer_id = customer_obj
         send_mailobj.email_epoch_time = epoch_time
         send_mailobj.email = customer_mail_id
         send_mailobj.save()
         subject = 'Reset Your ServiceMyWheels Password'
         to_user_list = [customer_mail_id]
         mail_html = loader.get_template('change_password_mail.html')
         data = Context({"customer_mail_id": customer_mail_id, "epoch_time": epoch_time})
         content = mail_html.render(data)
         msg = EmailMessage(subject, content, settings.EMAIL_HOST_USER, to_user_list)
         msg.content_subtype = "html"
         msg.send()
         if len(customer_registered_mobile) > 0:
            generate_otp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
            otp = generate_otp.now()
            request.session["otp"] = otp
            # phone = request.user.registered_phone
            # sms_message = "Your order is confirmed now / Enjoy Mari"
            # sms_url = const.SMS_VENDOR_URL + "?method=SendMessage&msg_type=TEXT&userid=" + const.SMS_VENDOR_ID + "&auth_scheme=plain&password=" + const.SMS_VENDOR_PASSWORD + "&v=1.1&format=text&send_to=" + customer_registered_mobile_number + "&msg=" + sms_message
            # requests.get(sms_url).text



