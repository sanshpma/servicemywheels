from django.db import models
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.models import UserManager
from datetime import datetime
from datetime import date
from djutil.models import TimeStampedModel
from constants import *
from . import manager


class ModelBase(TimeStampedModel):
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        # self.modified_at = datetime.now()
        return super(ModelBase, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Soft delete """
        self.is_deleted = True
        self.save()


class Customers(AbstractBaseUser, ModelBase):
        """
        creates account models
        """
        email = models.EmailField(max_length=254, unique=True)
        customer_name = models.CharField(max_length=75, blank=True, default="")
        registered_phone = models.CharField(max_length=20, default="")

        is_staff = models.BooleanField(default=False)
        is_active = models.BooleanField(default=True)

        # social info
        from_login = models.CharField(max_length=20, blank=True, null=True, default="")
        social_id = models.CharField(max_length=255, blank=True, null=True, default="")
        token_etag = models.CharField(max_length=255, blank=True, null=True, default="")

        # objects = UserManager()
        objects = manager.CustomUserManager()

        USERNAME_FIELD = 'email'

        def get_short_name(self):
            """
            Returns the short name for the user.
            """
            return self.customer_name.strip()

        def has_perm(self, perm, obj=None):
            return self.is_staff

        def has_module_perms(self, app_label):
            return self.is_staff

class CustomerAddresses(ModelBase):
    customer_id = models.ForeignKey(Customers, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, default="")
    zoneid = models.CharField(max_length=75, blank=True, default="")
    pincode = models.CharField(max_length=10, blank=True, default="")
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    city = models.CharField(max_length=75, blank=True, default="")
    state = models.CharField(max_length=75, blank=True, default="")
    country = models.CharField(max_length=10, blank=True, default="")


class CustomerContactNumbers(ModelBase):
    customer_id = models.ForeignKey(Customers, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, default="")


class CustomerVehiclesTypeMake(ModelBase):
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default="")
    vehicle_make = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):  # __unicode__ on Python 2
        return self.vehicle_type + " " + self.vehicle_make + " id  " + str(self.id)


class CustomerVehicles(ModelBase):
    vehicle_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    customer_id = models.ForeignKey(Customers, blank=True, null=True)
    vehicle_type_make = models.ForeignKey(CustomerVehiclesTypeMake, blank=True, null=True)
    # vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default="")
    # vehicle_make = models.CharField(max_length=50, blank=True, default="")
    vehicle_model = models.CharField(max_length=50, blank=True, default="")
    last_serviced_time = models.DateTimeField(blank=True, null=True)
    last_order_number_id = models.IntegerField(blank=True, null=True)
    km_runs = models.CharField(max_length=50, blank=True, default="")

    # __unicode__ on Python 2
    def __str__(self):
        return " id  " + str(self.id)

class SendMailLink(models.Model):
    customer_id = models.ForeignKey(Customers, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=False)
    email_epoch_time = models.IntegerField(blank=True, null=True)


class ServiceCenter(ModelBase):

    service_center_id = models.CharField(unique=True, max_length=20, default="")
    service_center_brand = models.CharField(max_length=20, default="")
    service_center_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default="")
    service_center_address = models.CharField(max_length=200, blank=True, default="")
    service_center_area_name = models.CharField(max_length=50, blank=True, default="")  
    service_center_pincode = models.CharField(max_length=10, blank=True, default="")  
    service_center_zoneid = models.CharField(max_length=10, blank=True, default="")  
    service_center_emailid = models.EmailField(max_length=75, blank=True)  

    def __str__(self): # __unicode__ on Python 2
        return self.service_center_brand + " " + self.service_center_type + " logical id  " + str(self.service_center_id) + " surrogate id  " + str(self.id) + " address " + self.service_center_address


class ServiceCenterContactNumbers(ModelBase):
    service_center_id = models.ForeignKey(ServiceCenter)  
    phone_number = models.CharField(max_length=20, blank=True, default="")  


class ServiceCenterContactPersons(ModelBase):
    service_center_id = models.ForeignKey(ServiceCenter)  
    contact_person_name = models.CharField( max_length=50, blank=True, default="")  
    contact_person_designation = models.CharField(max_length=30, blank=True, default="")  
    contact_person_emailid = models.EmailField(max_length=75, blank=True)  
    contact_person_personal_phone_number = models.CharField(max_length=20, blank=True, default="")  


class CrewMember(ModelBase):
    crew_member_name = models.CharField(max_length=75, blank=True, default="")  
    permanent_address = models.CharField(max_length=200, blank=True, default="")  
    current_address = models.CharField(max_length=200, blank=True, default="")  
    email_id = models.EmailField(max_length=75, blank=True)  
    zoneid = models.CharField(max_length=75, blank=True, default="")  
    can_drive = models.CharField(max_length=10, choices=CAN_DRIVE_CHOICES, blank=True, default="")
    driving_license_number = models.CharField(max_length=75, blank=True, default="")  


class CrewMemberContactNumbers(ModelBase):
    crew_member_id = models.ForeignKey(CrewMember)  
    crew_member_phone_number = models.CharField(max_length=20, blank=True, default="")  


class CrewMemberIdProof(ModelBase):
    crew_member_id = models.ForeignKey(CrewMember)  
    crew_member_id_proof_url = models.FileField(max_length=200)


class Invoices(ModelBase):
    service_center_invoice_url = models.FileField(max_length=200)
    our_invoice_url = models.FileField(max_length=200)


class Order(ModelBase):
    order_id = models.CharField(max_length=20, default="")  
    customer_id = models.ForeignKey(Customers, blank=True, null=True)
    service_center_id = models.ForeignKey(ServiceCenter, blank=True, null=True)  
    customer_vehicle_id = models.ForeignKey(CustomerVehicles, blank=True, null=True)
    customer_vehicle_type_make = models.ForeignKey(CustomerVehiclesTypeMake, blank=True, null=True)
    service_type = models.CharField(max_length=4, default="")  
    specific_problems_listed = models.CharField(max_length=1000, blank=True, default="")  
    generic_problems_listed = models.CharField(max_length=200, blank=True, default="")  
    customer_requested_pickup_time = models.DateTimeField(blank=True, null=True)  
    actual_pickup_time = models.DateTimeField(blank=True, null=True)  
    sc_delivered_time = models.DateTimeField(blank=True, null=True)  
    sc_pickup_time = models.DateTimeField(blank=True, null=True)  
    customer_delivered_time = models.DateTimeField(blank=True, null=True)  
    zoneid = models.CharField(max_length=75, blank=True, default="")  
    invoice_id = models.ForeignKey(Invoices, blank=True, null=True)  
    sc_bill_amount = models.DecimalField(max_digits=11, decimal_places=4, blank=True, null=True)  
    handling_charges = models.DecimalField(max_digits=11, decimal_places=4, blank=True, null=True)  
    status = models.CharField(max_length=75, blank=True, default="")  
    pickup_crew_member_id = models.ForeignKey(CrewMember, blank=True, null=True, related_name="pickup_crew_member_id")
    drop_crew_member_id = models.ForeignKey(CrewMember, blank=True, null=True, related_name="drop_crew_member_id")
    sc_chosen_by_customer = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, default="")
    phone = models.CharField(max_length=20, default="")
    customer_pickup_address_id = models.ForeignKey(CustomerAddresses, blank=True, null=True, related_name="customer_pickup_address_id")
    customer_drop_address_id = models.ForeignKey(CustomerAddresses, blank=True, null=True, related_name="customer_drop_address_id")

class CrewMemberStatus(ModelBase):
    crew_member_id = models.ForeignKey(CrewMember)
    current_order_id = models.ForeignKey(Order)
    status = models.CharField(max_length=60, default="")
    remarks = models.CharField(max_length=200, default="")
