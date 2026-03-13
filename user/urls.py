from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #common urls
    path('home/',views.home , name='home'),
    path('',views.Login , name='Login'),
    path('logout/',views.logout , name='logout'),
    path('followDoctor/<int:id>/',views.followDoctor , name='followDoctor'),

    #doctor urls
    path('doctorRegister/',views.doctorRegister , name='doctorRegister'),
    path('doctorPostDetails/<int:id>/',views.doctorPostDetails , name='doctorPostDetails'),
    path('doctorPostAdd/',views.doctorPostAdd , name='doctorPostAdd'),
    path('doctorProfile/',views.doctorProfile , name='doctorProfile'),
    path('doctorDashboard/',views.doctorDashboard,name='doctorDashboard'),
    path('viewDoctorProfile/<int:id>/',views.viewDoctorProfile , name='viewDoctorProfile'),
    path('doctorUpdateProfile/',views.doctorUpdateProfile , name='doctorUpdateProfile'),
    path('doctorSearch/',views.doctorSearch , name='doctorSearch'),
    path('rejectAppointment/<int:id>/', views.rejectAppointment, name='rejectAppointment'),
    path('acceptAppointment/<int:id>/', views.acceptAppointment, name='acceptAppointment'),
    path('doctorAppointments/',views.doctorAppointments,name='doctorAppointments'), 
<<<<<<< HEAD
    path('doctorReviews/',views.doctorReviews,name='doctorReviews'),
    path('doctorMessages/',views.doctorMessages,name='doctorMessages'),

=======
    path('doctorMessages/',views.doctorMessages,name='doctorMessages'), 
    path('doctorReviews/',views.doctorReviews,name='doctorReviews'), 
>>>>>>> 8a65e0225cdbafd355e35c3917df33c1cd88c879

    #patient urls
    path('patientRegister/',views.patientRegister,name='patientRegister'),
    path('patientDashboard/',views.patientDashboard,name='patientDashboard'),
    path('patientDoctorsList/',views.patientDoctorsList,name='patientDoctorsList'),
    path('patientAppointments/',views.patientAppointments,name='patientAppointments'),
<<<<<<< HEAD
=======
    path('patientMyAppointments/',views.patientMyAppointments,name='patientMyAppointments'),
>>>>>>> 8a65e0225cdbafd355e35c3917df33c1cd88c879
]
