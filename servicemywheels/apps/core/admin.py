from django.contrib import admin
from .models import Customers, Order, CustomerAddresses, CustomerContactNumbers, CustomerVehicles, ServiceCenter, \
    ServiceCenterContactNumbers, ServiceCenterContactPersons, CrewMember, CrewMemberContactNumbers, CrewMemberIdProof, \
    Invoices, CrewMemberStatus, CustomerVehiclesTypeMake
# Register your models here.

admin.site.register(Customers)
admin.site.register(Order)
admin.site.register(CustomerAddresses)
admin.site.register(CustomerContactNumbers)
admin.site.register(CustomerVehicles)
admin.site.register(ServiceCenter)
admin.site.register(ServiceCenterContactNumbers)
admin.site.register(ServiceCenterContactPersons)
admin.site.register(CrewMember)
admin.site.register(CrewMemberContactNumbers)
admin.site.register(CrewMemberIdProof)
admin.site.register(Invoices)
admin.site.register(CrewMemberStatus)
admin.site.register(CustomerVehiclesTypeMake)
