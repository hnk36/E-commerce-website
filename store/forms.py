from django import forms
from .models import Product, Customer, Order, OrderItem


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'





