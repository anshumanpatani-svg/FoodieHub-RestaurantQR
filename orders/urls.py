from django.urls import path
from . import views

urlpatterns = [

    path("cart/", views.cart, name="cart"),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    # path("remove-cart/<int:id>/", views.remove_cart, name="remove_cart"),
    path("increase-cart/<int:id>/", views.increase_cart, name="increase_cart"),
    path("decrease-cart/<int:id>/", views.decrease_cart, name="decrease_cart"),
    path("remove-cart/<int:id>/", views.remove_cart, name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),

    path("track-order/<int:order_id>/", views.track_order, name="track_order"),
    path("status/<int:order_id>/", views.order_status_api, name="order_status_api"),

    path("scan/<int:table_number>/", views.scan_table, name="scan_table"),
]



    

