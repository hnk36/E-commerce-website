from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image']
    list_editable = ['image']
    search_fields = ('name', 'slug')
    list_filter = ('digital',)
    fields = ('slug', 'name', 'price', 'digital', 'image', 'category')


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']
    list_editable = ['last_name', 'phone',]
    list_pre_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['date_order', 'customer', 'complete', 'transaction_id']
    list_display_links = ['date_order']
    list_editable = ['customer', 'complete', 'transaction_id']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    list_display_links = ['order']
    list_editable = ['price', 'product', 'quantity']


@admin.register(models.ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'street', 'city', 'Zip_code', 'city']
    list_display_links = ['customer']
    list_editable = ['street', 'street', 'Zip_code', 'city']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at']
    list_editable = ['customer']


@admin.register(models.CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
    list_editable = ['cart', 'product', 'quantity']
