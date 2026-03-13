# from django.contrib import admin
# from .models import *

# admin.site.register(tblUser)
# admin.site.register(tblCity)
# admin.site.register(tblState)
# admin.site.register(tblSubcategory)
# admin.site.register(tblCategory)
# admin.site.register(tblDoctorPost)
# admin.site.register(tblDoctor)
# admin.site.register(tblDoctorImages)
# admin.site.register(tblComments)
# admin.site.register(tblClient)
# admin.site.register(tblAppointment)
# admin.site.register(tblclientHistory)   
# admin.site.register(tblReview)
# admin.site.register(tblchat)
# admin.site.register(tblnotification)
# admin.site.register(tblFollow)

# # Register your models here.
from django.contrib import admin
from .models import *

from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'userName', 'email', 'mobileNumber', 'cityID', 'IsDoctor')
    list_filter = ('IsDoctor', 'cityID')
    search_fields = ('userName', 'email', 'mobileNumber')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctorID', 'displayName', 'displayContact', 'subcategoryID', 'mode_status')
    list_filter = ('subcategoryID', 'mode')
    search_fields = ('displayName', 'displayContact', 'bio')

    def mode_status(self, obj):
        if obj.mode == 1:
            return format_html('<span class="badge badge-success">Online</span>')
        return format_html('<span class="badge badge-warning">Offline</span>')
    mode_status.short_description = 'Status'

class ClientAdmin(admin.ModelAdmin):
    list_display = ('clientID', 'name', 'gender', 'bloodGroup', 'dob')
    list_filter = ('gender', 'bloodGroup')
    search_fields = ('name', 'description')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointmentID', 'clientID', 'doctorID', 'appointmentDate', 'appointmentTime', 'status_badge')
    list_filter = ('isAccepted', 'isRejected', 'appointmentDate')
    search_fields = ('clientID__name', 'doctorID__displayName')

    def status_badge(self, obj):
        if obj.isAccepted:
            return format_html('<span class="badge badge-success">Accepted</span>')
        elif obj.isRejected:
            return format_html('<span class="badge badge-danger">Rejected</span>')
        return format_html('<span class="badge badge-warning">Pending</span>')
    status_badge.short_description = 'Status'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewID', 'doctorID', 'userID', 'rating', 'createdDT')
    list_filter = ('rating',)
    search_fields = ('review',)

admin.site.register(tblUser, UserAdmin)

admin.site.register(tblCity)
admin.site.register(tblState)
admin.site.register(tblSubcategory)
admin.site.register(tblCategory)
admin.site.register(tblDoctorPost)

admin.site.register(tblDoctor, DoctorAdmin)
admin.site.register(tblDoctorImages)
admin.site.register(tblComments)

admin.site.register(tblClient, ClientAdmin)
admin.site.register(tblAppointment, AppointmentAdmin)
admin.site.register(tblclientHistory)   

admin.site.register(tblReview, ReviewAdmin)
admin.site.register(tblchat)
admin.site.register(tblnotification)
admin.site.register(tblFollow)


# Register your models here.
