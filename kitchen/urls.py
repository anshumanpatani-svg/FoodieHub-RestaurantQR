from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="kitchen_dashboard"),
    path("status/<int:id>/<str:status>/", views.change_status, name="change_status"),
    path("notifications/", views.notification_count, name="notification_count"),

]