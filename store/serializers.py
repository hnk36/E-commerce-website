from django.contrib.auth.models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Order, OrderItem, ShippingAddress, Customer, Cart, CartItem, Product


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'slug', 'name', 'price', 'digital', 'image', 'category']


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Customer
        fields = [id, 'user', 'first_name', 'last_name', 'email', 'phone']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='product_set', many=True, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'quantity', 'get_total_price']


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['id', 'customer', 'street', 'city', 'Zip_code']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitems_set', many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(source='shippingaddress_set', many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.firstname', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'date_order', 'customer_name', 'complete', 'transaction_id', 'order_items','shipping_address']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['created_at']


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(source='cart_set', many=True, read_only=True)
    product = ProductSerializer(source='Product_set', many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']



