import json
from django.shortcuts import render
from rest_framework.views import APIView
from core import config
from core import models
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from functools import wraps
import random
from django.core.mail import EmailMessage
from core import const
import requests
from django.conf import settings
from . import utils
from core.models import SendMailLink
import time
import calendar
from django.template import loader, Context

class persist_session_vars(object):
    """ Some views, such as login and logout, will reset all session state.
    However, we occasionally want to persist some of those session variables.
    """

    session_backup = {}

    def __init__(self, vars):
        self.vars = vars

    def __enter__(self):
        for var in self.vars:
            self.session_backup[var] = self.request.session.get(var)

    def __exit__(self, exc_type, exc_value, traceback):
        for var in self.vars:
            self.request.session[var] = self.session_backup.get(var)

    def __call__(self, test_func, *args, **kwargs):

        @wraps(test_func)
        def inner(*args, **kwargs):
            if not args:
                raise Exception('Must decorate a view, ie a function taking request as the first parameter')
            self.request = args[0]
            with self:
                return test_func(*args, **kwargs)

        return inner

class Booking(APIView):
    template_name = "home.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Booking, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if "vehicle_type" in request.session:
                # Returning session data+configdata
                bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                pickup_time, selected_brand, selected_service_center_address, selected_specific_problems_listed, selected_vehicle_type, selected_service_type, selected_generic_problems = self.get_session_data(
                    request)
                return render(request, self.template_name, {"selected_vehicle_type": selected_vehicle_type,
                                                            "selected_brand": selected_brand,
                                                            "selected_specific_problems_listed": selected_specific_problems_listed,
                                                            "selected_service_center_address": selected_service_center_address,
                                                            "vehicle": vehicle,
                                                            "car": car, 'bike': bike, "service_center": service_center,
                                                            "generic_problems": generic_problems,
                                                            "pickup_time": pickup_time,
                                                            "selected_service_type": selected_service_type,
                                                            "selected_generic_problems": selected_generic_problems})
            else:
                # Returning only config data
                bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                return render(request, self.template_name, {"vehicle": vehicle, "car": car, 'bike': bike, "service_center": service_center, "generic_problems": generic_problems})

        else:
            if "source" in request.session:
                if request.session["source"] == "book":
                    request.session["current_order_completed"] = False
                    return HttpResponseRedirect('/website/confirmorder')

                elif request.session["source"] == "login":
                    if "vehicle_type" in request.session:
                        # Returning session data+configdata
                        bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                        pickup_time, selected_brand, selected_service_center_address, selected_specific_problems_listed, selected_vehicle_type, selected_service_type, selected_generic_problems = self.get_session_data(
                            request)
                        return render(request, self.template_name, {"selected_vehicle_type": selected_vehicle_type,
                                                            "selected_brand": selected_brand,
                                                            "selected_specific_problems_listed": selected_specific_problems_listed,
                                                            "selected_service_center_address": selected_service_center_address,
                                                            "vehicle": vehicle,
                                                            "car": car, 'bike': bike, "service_center": service_center,
                                                            "generic_problems": generic_problems,
                                                            "pickup_time": pickup_time,
                                                            "selected_service_type": selected_service_type,
                                                            "selected_generic_problems": selected_generic_problems})
                    else:
                        # Returning only config data
                        bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                        return render(request, self.template_name, {"vehicle": vehicle, "car": car, 'bike': bike, "service_center": service_center, "generic_problems": generic_problems})
                else:
                    if "vehicle_type" in request.session:
                        # Also check if request.session['vehicle_type']==None
                        # Returning session data+config data
                        bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                        pickup_time, selected_brand, selected_service_center_address, selected_specific_problems_listed, selected_vehicle_type, selected_service_type, selected_generic_problems = self.get_session_data(
                            request)
                        return render(request, self.template_name, {"selected_vehicle_type": selected_vehicle_type,
                                                            "selected_brand": selected_brand,
                                                            "selected_specific_problems_listed": selected_specific_problems_listed,
                                                            "selected_service_center_address": selected_service_center_address,
                                                            "vehicle": vehicle,
                                                            "car": car, 'bike': bike, "service_center": service_center,
                                                            "generic_problems": generic_problems,
                                                            "pickup_time": pickup_time,
                                                            "selected_service_type": selected_service_type,
                                                            "selected_generic_problems": selected_generic_problems})
                    else:
                        # Returning only config data
                        bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                        return render(request, self.template_name, {"vehicle": vehicle, "car": car, 'bike': bike, "service_center": service_center, "generic_problems": generic_problems})

            else:
                # Returning only config data
                bike, car, generic_problems, service_center, vehicle = self.get_config_data()
                return render(request, self.template_name, {"vehicle": vehicle, "car": car, 'bike': bike, "service_center": service_center, "generic_problems": generic_problems})

    def post(self, request):
        utils.set_session_data_from_post_request(request)
        utils.set_session_data_from_post_request(request)
        request.session["current_order_completed"] = False
        msg = {'status': 'done'}
        return HttpResponse(json.dumps(msg))
        # return HttpResponseRedirect('/website/confirmorder/')

    def get_session_data(self, request):
        selected_vehicle_type = request.session['vehicle_type']
        selected_brand = request.session["brand"]
        selected_specific_problems_listed = request.session["specific_problems_listed"]
        selected_service_center_address = request.session["service_center_address"]
        selected_service_type = request.session["service_type"]
        pickup_time = request.session["pickup_time"]
        selected_generic_problems = request.session["selected_generic_problems"]
        return pickup_time, selected_brand, selected_service_center_address, selected_specific_problems_listed, selected_vehicle_type, selected_service_type, selected_generic_problems

    def get_config_data(self):
        vehicle = config.VEHICLE
        car = json.dumps(config.BRAND['Car'])
        bike = json.dumps(config.BRAND['Bike'])
        service_center = json.dumps(config.SERVICE_CENTER)
        generic_problems = json.dumps(config.GENERIC_PROBLEMS)
        return bike, car, generic_problems, service_center, vehicle

class SaveBooking(APIView):
    def post(self, request):
            # Setting data in session from AJAX call
            request.session["vehicle_type"] = request.DATA.get('vehicle_type')
            request.session["brand"] = request.DATA.get('brand')
            request.session["source"] = request.DATA.get('source')
            request.session["service_type"] = request.DATA.get("service_type")
            request.session["specific_problems_listed"] = request.DATA.get('specificProblems')
            request.session["service_center_address"] = request.DATA.get('service_center_address')
            request.session["pickup_time"] = request.DATA.get('pickup_time')
            request.session["selected_generic_problems"] = json.dumps(request.DATA.get('selected_generic_problems'))
            context = {"message": "SUCCESS", "error": "error"}
            return Response(context)

class ConfirmOrder(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        if "current_order_completed" in request.session:
            if request.session["current_order_completed"] == False :
                 request.session["source"] = None
                 customer_mail_id = request.user
                 customer_addresses = []
                 customer_mobile_number = []
                 customer_id = models.Customers.objects.get(email=customer_mail_id).id
                 customer_addresses_obj = models.CustomerAddresses.objects.filter(customer_id=customer_id)
                 for obj in customer_addresses_obj:
                     customer_addresses.append(obj.address)
                 customer_registered_mobile_number = models.Customers.objects.get(id=customer_id).registered_phone
                 customer_mobile_obj = models.CustomerContactNumbers.objects.filter(customer_id=customer_id)
                 for obj in customer_mobile_obj:
                     if customer_registered_mobile_number != obj.phone_number:
                         customer_mobile_number.append(obj.phone_number)
                 customer_name = request.user.customer_name
                 pickup_time, vehicle_type, brand, service_center_address, service_center_address_obj, service_type, specific_problem_listed, selected_generic_problems = self.processOrderFromSession(request)
                 return render(request, "confirmation.html", {"pickup_time": pickup_time,
                                                              "vehicle_type": vehicle_type, "brand": brand,
                                                              "service_center_address": service_center_address,
                                                              "customers_addresses": customer_addresses,
                                                              "customers_addresses_list": customer_addresses_obj,
                                                              "customer_registered_mobile_number": customer_registered_mobile_number,
                                                              "customer_mobile_number": customer_mobile_number,
                                                              "customer_name": customer_name,
                                                              "service_type": service_type,
                                                              "specific_problems": specific_problem_listed,
                                                              "selected_generic_problems": selected_generic_problems,
                                                              "customer_mail_id": customer_mail_id})
            else:
                 return HttpResponseRedirect('/website/booking')
        else:
            return HttpResponseRedirect('/website/booking')

    def post(self, request):
         request.session["source"] = None
         customer_mail_id = request.user
         customer_addresses = []
         customer_mobile_number = []
         customer_id = models.Customers.objects.get(email=customer_mail_id).id
         customer_addresses_obj = models.CustomerAddresses.objects.filter(customer_id=customer_id)
         for obj in customer_addresses_obj:
             customer_addresses.append(obj.address)
         customer_registered_mobile_number = models.Customers.objects.get(id=customer_id).registered_phone
         customer_mobile_obj = models.CustomerContactNumbers.objects.filter(customer_id=customer_id)
         for obj in customer_mobile_obj:
             if customer_registered_mobile_number != obj.phone_number:
                 customer_mobile_number.append(obj.phone_number)
         customer_name = request.user.customer_name
         pickup_time, vehicle_type, brand, service_center_address, service_center_address_obj, service_type, specific_problem_listed, selected_generic_problems = self.processOrderFromSession(request)
         return render(request, "confirmation.html", {"pickup_time": pickup_time,
                                                      "vehicle_type": vehicle_type, "brand": brand,
                                                      "service_center_address": service_center_address,
                                                      "customers_addresses": customer_addresses,
                                                      "customer_registered_mobile_number": customer_registered_mobile_number,
                                                      "customer_mobile_number": customer_mobile_number,
                                                      "customer_name": customer_name,
                                                      "service_type": service_type,
                                                      "specific_problems": specific_problem_listed,
                                                      "selected_generic_problems": selected_generic_problems,
                                                      "customer_mail_id": customer_mail_id})

    def processOrderFromSession(self, request):
        # rendering data from session request
        vehicle_type = request.session["vehicle_type"]
        brand = request.session["brand"]
        selected_generic_problems = request.session["selected_generic_problems"]
        service_type = request.session["service_type"]
        specific_problem_listed = request.session["specific_problems_listed"]
        service_center_address = request.session["service_center_address"]
        service_center_chosen_by_customer = utils.get_service_center_chosen_by_customer(service_center_address)
        if service_center_chosen_by_customer:
            service_center_address_obj = models.ServiceCenter.objects.get(service_center_address=service_center_address,
                                                                          service_center_brand=brand)
        else:
            service_center_address_obj = None
        pickup_date_time = request.session["pickup_time"]
        return pickup_date_time, vehicle_type, brand, service_center_address, service_center_address_obj, service_type, specific_problem_listed, selected_generic_problems

class YourOrder(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        if "current_order_completed" in request.session:
            if request.session["current_order_completed"]:
                order_id = request.session["order_id"]
                pickup_address = request.session["pickup_address_send"]
                drop_address = request.session["drop_address_send"]
                pickup_time = request.session["pickup_time_send"]
                return render(request, "thankyou.html", {'order_id': order_id, 'pickup_address_send': pickup_address, 'drop_address_send': drop_address, 'pickup_time': pickup_time})
            else:
                return HttpResponseRedirect('/website/booking')
        else:
            return HttpResponseRedirect('/website/booking')
    @method_decorator(csrf_exempt)
    def post(self, request):
        # saving order in database
        order_id = random.randint(10, 10000)
        order_id_send = order_id
        customer_obj = request.user
        pickUpAddresId = request.POST.get('pick-up-address-id')
        dropAddressId = request.POST.get('drop-address-id')
        selected_service_type = request.POST.get('selected-service-type')
        user_phone_number_for_current_order = request.POST.get('user_mobile_number')
        pick_address_obj = models.CustomerAddresses.objects.get(id=pickUpAddresId)
        pickup_address_send = pick_address_obj.address
        drop_address_obj = models.CustomerAddresses.objects.get(id=dropAddressId)
        drop_address_send = drop_address_obj.address
        pickup_time, selected_brand, selected_service_center_address, selected_specific_problems_listed, selected_vehicle_type, selected_generic_problems = self.get_session_data(
                    request)

        service_center_chosen_by_customer = utils.get_service_center_chosen_by_customer(selected_service_center_address)
        if service_center_chosen_by_customer:
            service_center_address_obj = models.ServiceCenter.objects.get(service_center_address=selected_service_center_address,
                                                                          service_center_brand=selected_brand)
        else:
            service_center_address_obj = None

        # insert vehicle record in table only after getting vehicle number
        # vehicle_obj = models.CustomerVehicles()
        # vehicle_obj.vehicle_type = vehicle_type
        # vehicle_obj.vehicle_make = brand
        # vehicle_obj.customer_id = customer_obj
        # vehicle_obj.save()
        try:
            customer_vehicles_type_make = models.CustomerVehiclesTypeMake.objects.get(vehicle_type=selected_vehicle_type,
                                                                                      vehicle_make=selected_brand)
        except models.CustomerVehiclesTypeMake.DoesNotExist:
            return HttpResponse('data not exist')
        order_obj = models.Order()
        order_obj.customer_id = customer_obj
        order_obj.customer_pickup_address_id = pick_address_obj
        order_obj.customer_drop_address_id = drop_address_obj
        order_obj.customer_vehicle_type_make = customer_vehicles_type_make
        # order_obj.customer_vehicle_id =vehicle_obj
        order_obj.specific_problems_listed = selected_specific_problems_listed
        order_obj.service_type = selected_service_type
        order_obj.service_center_id = service_center_address_obj
        order_obj.generic_problems_listed = selected_generic_problems
        # order_obj.customer_vehicle_id = vehicle_obj
        order_obj.status = "Waiting for Pickup"
        order_obj.customer_requested_pickup_time = pickup_time
        order_obj.sc_chosen_by_customer = service_center_chosen_by_customer
        order_obj.phone = user_phone_number_for_current_order
        order_obj.order_id = order_id
        order_obj.save()
        request.session["specific_problems_listed"] = None
        request.session["source"] = None
        request.session["vehicle_type"] = None
        request.session["service_center_address"] = None
        request.session["brand"] = None
        request.session["service_type"] = None
        request.session["pickup_time"] = None
        request.session["selected_generic_problems"] = None
        request.session["order_id"] = order_id
        request.session["drop_address_send"] = drop_address_send
        request.session["pickup_address_send"] = pickup_address_send
        request.session["pickup_time_send"] = pickup_time
        request.session["current_order_completed"] = True
        request.session["mail_sent"] = False
        return render(request, "thankyou.html", {'order_id': order_id, 'pickup_address_send':pickup_address_send, 'drop_address_send': drop_address_send, 'pickup_time': pickup_time})

    def get_session_data(self, request):
        selected_vehicle_type = request.session['vehicle_type']
        selected_brand = request.session["brand"]
        selected_specific_problems_listed = request.session["specific_problems_listed"]
        selected_service_center_address = request.session["service_center_address"]
        pickup_time = request.session["pickup_time"]
        selected_generic_problems = request.session["selected_generic_problems"]
        return pickup_time, selected_brand, selected_service_center_address, selected_specific_problems_listed, selected_vehicle_type, selected_generic_problems

class SendMail(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        order_id_from_session = request.session["order_id"]
        order_id_from_session = str(order_id_from_session)
        current_order_id = request.DATA.get('current_order_id')
        if order_id_from_session == current_order_id:
            if request.session["mail_sent"] == False:
                order_obj = models.Order.objects.get(order_id=current_order_id)
                customer_pickup_adddress = order_obj.customer_pickup_address_id.address
                customer_drop_address = order_obj.customer_drop_address_id.address
                customer_requested_pickup_time = order_obj.customer_requested_pickup_time
                customer_mail_id = request.user.email
                mail_html = loader.get_template('your_order.html')
                data = Context({"customer_mail_id": customer_mail_id, "order_id": current_order_id, "customer_pickup_adddress": customer_pickup_adddress, "customer_drop_address": customer_drop_address, "customer_requested_pickup_time": customer_requested_pickup_time})
                content = mail_html.render(data)
                subject = 'Thank you for your order'
                to_user_list = [customer_mail_id]
                msg = EmailMessage(subject, content, settings.EMAIL_HOST_USER, to_user_list)
                msg.content_subtype = "html"
                msg.send()
                request.session["mail_sent"] = True
                self.delete_send_mail()
        phone = request.user.registered_phone
        if len(phone) > 0:
            sms_message = "Your order is confirmed now / Enjoy Mari"
            sms_url = const.SMS_VENDOR_URL + "?method=SendMessage&msg_type=TEXT&userid=" + const.SMS_VENDOR_ID + "&auth_scheme=plain&password=" + const.SMS_VENDOR_PASSWORD + "&v=1.1&format=text&send_to=" + phone + "&msg=" + sms_message
            requests.get(sms_url).text
        context = {"message": "SUCCESS", "error": "error"}
        return Response(context)
    def delete_send_mail(self):
        current_epoch_time = calendar.timegm(time.gmtime())
        current_epoch_time = time.gmtime(current_epoch_time)
        current_epoch_time = time.mktime(current_epoch_time)
        send_mail_obj_list = SendMailLink.objects.all()
        for obj in send_mail_obj_list:
                send_mail_epoch_time = obj.email_epoch_time
                send_mail_epoch_time = time.gmtime(send_mail_epoch_time)
                send_mail_epoch_time = time.mktime(send_mail_epoch_time)
                diff_time = abs(current_epoch_time-send_mail_epoch_time)
                if diff_time >=3600:
                    obj.delete()
