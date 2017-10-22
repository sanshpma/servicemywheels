import json
from rest_framework.views import APIView
from core import models
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class SaveAddress(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            customer_obj = request.user
            customer_new_addresses = request.DATA.get('address')
            customer_new_city = request.DATA.get('city')
            customer_country_name = "India"
            customer_new_pincode = request.DATA.get('pincode')
            customer_new_state = request.DATA.get('state')
            customer_address_obj = models.CustomerAddresses()
            customer_address_obj.address = customer_new_addresses
            customer_address_obj.customer_id = customer_obj
            customer_address_obj.city = customer_new_city
            customer_address_obj.state = customer_new_state
            customer_address_obj.pincode = customer_new_pincode
            customer_address_obj.country = customer_country_name
            customer_address_obj.save()
            return HttpResponseRedirect("/website/confirmorder")
        else:
            return HttpResponseRedirect("/website/login")

