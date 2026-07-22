from django.db import models
from menu.models import Food
import os

class RestaurantTable(models.Model):

    table_number = models.IntegerField(unique=True)

    STATUS = (
        ('Available','Available'),
        ('Occupied','Occupied'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Available'
    )

    qr_code = models.ImageField(
        upload_to="qr_codes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Table {self.table_number}"


class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
    )

    table = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.food.food_name} ({self.quantity})"
    


class Cart(models.Model):

    session_key = models.CharField(max_length=100)

    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.food.food_name} ({self.quantity})"