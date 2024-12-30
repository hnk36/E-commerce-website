from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, OrderItem, Cart, CartItem, Customer
from .serializers import ProductSerializer, UserSerializer, CustomerSerializer
from rest_framework.views import APIView

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # create the customer
        customer_data = {
            'user': user.id,
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone')
        }
        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            customer_serializer.save()
              # Log the user in
            login(request, user)
            return Response({'status': 'signup successful', 'success': True}, status=status.HTTP_201_CREATED)
        else:
            user.delete()# Rollback user creation if customer creation fails
            return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST', 'GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'status': 'login successful', 'success': True}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
    return render({'error': 'invalide request metthod'},status.HTTP_405_METHOD_NOT_ALLOWED)    
    
        


@api_view(['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def store(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return render(request, 'store.html', {'products': serializer.data})
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
        product_id = request.data.get('id')
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product_id = request.data.get('id')
        product = get_object_or_404(Product, id=product_id)
        if OrderItem.objects.filter(product=product).exists():
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def product(request, id):
    product_detail = get_object_or_404(Product, pk=id)
    return render(request, 'product.html', {"product": product_detail})


class AddToCartView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect('login')
        product = get_object_or_404(Product, pk=product_id)
        customer = get_object_or_404(Customer, user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response({'message': 'Item added successfully'}, status=status.HTTP_200_OK)

class UpdateCartView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def patch(self, request, product_id):
        if not request.user.is_authenticated:
            return redirect('login')

        product = get_object_or_404(Product, pk=product_id)
        customer = get_object_or_404(Customer, user=request.user)
        cart = get_object_or_404(Cart, customer=customer)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            new_quantity = request.data.get('quantity')
            if new_quantity is not None:
                new_quantity = int(new_quantity)
                if new_quantity > 0:
                    cart_item.quantity = new_quantity
                    cart_item.save()
                    return Response({'message': 'Item updated successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Quantity must be greater than zero'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Quantity not provided'}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
   
       

@api_view()
def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)



