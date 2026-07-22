from django.urls import path
from . import views

urlpatterns = [

    path("", views.dashboard, name="admin_dashboard"),
    path("foods/", views.food_list, name="food_list"),
    path("foods/add/", views.food_add, name="food_add"),
    path("foods/<int:id>/edit/", views.food_edit, name="food_edit"),
    path("foods/<int:id>/delete/", views.food_delete, name="food_delete"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_add, name="category_add"),
    path("categories/<int:id>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:id>/delete/", views.category_delete, name="category_delete"),

    path("tables/", views.table_list, name="table_list"),
    path("tables/add/", views.table_add, name="table_add"),
    path("tables/<int:id>/edit/", views.table_edit, name="table_edit"),
    path("tables/<int:id>/delete/", views.table_delete, name="table_delete"),

    path("tables/<int:id>/generate-qr/", views.generate_qr, name="generate_qr"),
    path("tables/qr-cards/", views.qr_cards, name="qr_cards"),

    path("orders/", views.order_list, name="order_list"),
    path("orders/<int:id>/", views.order_detail, name="order_detail"),
    path("orders/<int:id>/status/<str:status>/", views.update_order_status, name="update_order_status"),
    path("orders/ajax/", views.order_table_ajax, name="order_table_ajax"),

    
]