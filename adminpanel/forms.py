from django import forms
from menu.models import *
from orders.models import RestaurantTable


class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = [
            "food_name",
            "category",
            "price",
            "description",
            "image",
            "available",
        ]


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = [
            "category_name",
            "image",
        ]

        widgets = {

            "category_name": forms.TextInput(
                attrs={
                    "class":"form-control",
                    "placeholder":"Category Name"
                }
            ),

        }




class TableForm(forms.ModelForm):

    class Meta:
        model = RestaurantTable
        fields = [
            "table_number",
            "status",
        ]

        widgets = {
            "table_number": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Table Number"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }