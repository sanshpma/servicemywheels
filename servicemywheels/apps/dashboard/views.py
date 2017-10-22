from django.shortcuts import render
from rest_framework.views import APIView
from core import models
from django.http import HttpResponse, HttpResponseRedirect


class MyProfile(APIView):
    template_name = "new_dashboard.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user_id = request.user.id
            user_obj = models.Customers.objects.get(id=user_id)
            email = request.user.email
            name = request.user.customer_name
            registeredPhoneNumber = request.user.registered_phone
            # addresses = request.user.customeraddresses_set.all()
            return render(request, "new_dashboard.html", {"id": id, "email": email, "name": name, "user_obj": user_obj,
                                                          "registeredPhoneNumber": registeredPhoneNumber, "page": "profile"})
        else:
            return HttpResponseRedirect("/website/login")


class MyOrder(APIView):
    template_name = "new_myorder.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            generic_problem_list = {}
            user_id = request.user.id
            order_objects = models.Order.objects.filter(customer_id=user_id)
            # vehicle_id = order_objects.customer_vehicle_type_make
            # vehicle_details = models.CustomerVehiclesTypeMake.objects.get(id=vehicle_id)
            return render(request, self.template_name, {"order_objects": order_objects,  "page": "order"})
        else:
            return HttpResponseRedirect("/website/login")


class MyVehicle(APIView):
    template_name = "myvehicle.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user_id = request.user.id
            vehicle_objects = models.CustomerVehicles.objects.filter(customer_id=user_id)
            return render(request, self.template_name, {"vehicle_objects": vehicle_objects, "page": "vehicle"})
        else:
            return HttpResponseRedirect("/website/login")

class MyAddress(APIView):
    template_name = "myAddress.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            user_id = request.user.id
            user_obj = models.Customers.objects.get(id=user_id)
            email = request.user.email
            name = request.user.customer_name
            registeredPhoneNumber = request.user.registered_phone
            # addresses = request.user.customeraddresses_set.all()
            return render(request, "myAddress.html", {"id": id, "email": email, "name": name, "user_obj": user_obj,
                                                          "registeredPhoneNumber": registeredPhoneNumber, "page": "profile"})
        else:
            return HttpResponseRedirect("/website/login")


class Test(APIView):
    template_name = "order-summary.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
