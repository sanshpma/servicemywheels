from django.shortcuts import render
from rest_framework.views import APIView
from core import models
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class NewOrderNotification(APIView):
    template_name = "staffHome.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        order_waiting_for_pickup_crewMemberAssignment = models.Order.objects.filter(pickup_crew_member_id=None)
        order_waiting_for_serviceCenterAssignment = models.Order.objects.filter(service_center_id=None)
        order_waiting_for_drop_crewMemberAssignment = models.Order.objects.filter(drop_crew_member_id=None)
        return render(request, "staffHome.html",
                      {"order_waiting_for_pickup_crewMemberAssignment": order_waiting_for_pickup_crewMemberAssignment,
                       "order_waiting_for_serviceCenterAssignment": order_waiting_for_serviceCenterAssignment,
                       "order_waiting_for_drop_crewMemberAssignment": order_waiting_for_drop_crewMemberAssignment})


class SearchOrder(APIView):
    template_name = "searchorder.html"

    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        requested_order_id = request.POST.get('requested_order_id')
        if requested_order_id != '':
            order_obj = models.Order.objects.get(order_id=requested_order_id)
        requested_id = request.POST.get('requested_id')
        if requested_id != '':
            order_obj = models.Order.objects.get(id=requested_id)
        requested_phone_no = request.POST.get('requested_phone_no')
        if requested_phone_no != '':
            user_obj = models.Customers.objects.get(registered_phone=requested_phone_no)
            order_obj = models.Order.objects.filter(customer_id=user_obj.id)
        return render(request, "searchorder.html", {"order_obj": order_obj})
