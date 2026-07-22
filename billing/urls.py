from django.urls import path
from . import views

urlpatterns = [

    path("", views.billing_dashboard, name="billing_dashboard"),
    path("invoice/<int:id>/", views.invoice, name="invoice"),
    path("paid/<int:id>/", views.mark_paid, name="mark_paid"),

]