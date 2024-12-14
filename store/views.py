from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def store(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        product_id = request.data.get('id')
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = ProductSerializer(Product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product_id = request.data.get('id')
        product = get_object_or_404(Product, id=product_id)
        if OrderItem.objects.filter(product=product).exists():
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def cart(request):
    customer = request.user.customer  # Assuming Customer is linked to User via a OneToOneField
    order = Order.objects.filter(customer=customer, complete=Order.PAYMENT_PENDING).first()

    if not order:
        # If no pending order is found, you can create a new order or return a message
        context = {
            'order_items': [],
            'total': 0,
        }
        return render(request, 'cart.html', context)

    # Retrieve all order items related to the order
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'cart.html', context)


@api_view()
def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)
