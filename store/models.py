from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator


class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/', default='images/placeholder')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    slug = models.SlugField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(upload_to='image/')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name']


class Order(models.Model):
    orderitem_set = None
    PAYMENT_PENDING = 'P'
    PAYMENT_CONFIRMED = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        ('PAYMENT_PENDING', 'Pending'),
        ('PAYMENT_CONFIRMED', 'Confirmed'),
        ('PAYMENT_FAILED', 'Failed'),
    ]
    date_order = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    complete = models.CharField(max_length=17, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.first_name} {self.customer.last_name}"

    class Meta:
        ordering = ['-date_order']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=3, validators=[MinValueValidator(0.01)])
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    class Meta:
        ordering = ['price']

    @property
    def get_total_price(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    Zip_code = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.street}, {self.city}, {self.Zip_code}'

    class Meta:
        ordering = ['customer']


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"













