from core import models
from common import stringutility
import json

def get_generic_problems(generic_problems_listed):

    generic_problems = ""
    for i in  range (len(generic_problems_listed)):
        if i < len(generic_problems_listed)-1:
            generic_problems = generic_problems + generic_problems_listed[i] + "|"
        else:
            generic_problems = generic_problems + generic_problems_listed[i]
    return generic_problems

def get_service_center_address(service_center_address):
    models.ServiceCenter.objects.get(service_center_address=service_center_address)

def get_service_center_chosen_by_customer(service_center_address):
    if service_center_address != "Select Service Center" and stringutility.is_not_null_empty(service_center_address):
        return True
    else:
        return False

def set_session_data_from_post_request(request):
    request.session["vehicle_type"] = request.POST.get('vehicle_type')
    request.session["brand"] = request.POST.get('brand')
    # request.session["generic_problems_listed"] = request.DATA.getlist('generic_problem')
    request.session["service_type"] = request.POST.get("serviceType")
    request.session["specific_problems_listed"] = request.POST.get('specificProblems')
    request.session["service_center_address"] = request.POST.get('location')
    request.session["pickup_time"] = request.POST.get('pickup_time')
    generic_problem_length = 0
    if request.POST.get('generic_problem_length'):
        generic_problem_length = int(request.POST.get('generic_problem_length'))
    generic_key = 'generic_problem_'
    selected_generic_problems = []
    for i in range(0, generic_problem_length):
        if request.POST.get(generic_key+str(i)):
            selected_generic_problems.append(str(request.POST.get(generic_key+str(i))))

    request.session["selected_generic_problems"] = json.dumps(selected_generic_problems)
