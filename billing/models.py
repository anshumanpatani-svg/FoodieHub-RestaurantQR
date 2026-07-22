from django.db import models
from orders.models import Order


class Bill(models.Model):

    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
    )

    PAYMENT_STATUS = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    def __str__(self):
        return f"Bill - {self.order.order_number}"