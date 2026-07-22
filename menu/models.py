from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    def __str__(self):
        return self.category_name


class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='foods/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.food_name