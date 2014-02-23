from django.contrib import admin
from models import *

# Register your models here.

class AssociatedAdmin(admin.ModelAdmin):
    pass
admin.site.register(Associated, AssociatedAdmin)

class LocationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Location, LocationAdmin)

class StatusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Status, StatusAdmin)

class RouteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Route, RouteAdmin)

class DeliveryRequestAdmin(admin.ModelAdmin):
    pass
admin.site.register(DeliveryRequest, DeliveryRequestAdmin)

class PackageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Package, PackageAdmin)

class BillAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bill, BillAdmin)

class RoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Role, RoleAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Employee, EmployeeAdmin)

class LogEntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(LogEntry, LogEntryAdmin)

class ReportAdmin(admin.ModelAdmin):
    pass
admin.site.register(Report, ReportAdmin)

class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)