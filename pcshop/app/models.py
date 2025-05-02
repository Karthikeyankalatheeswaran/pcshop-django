from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


AUTH_USER_MODEL = 'app.CustomUser'


class Category(models.Model):
    name = models.CharField(max_length=50,unique=True,null=False)
    
    def __str__(self):
        return self.name
        

class Brand(models.Model):
    name = models.CharField(max_length=50,unique=True,null=False)
    
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/', default='products/default.jpg', blank=True, null=True)
    stock = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.name
    
    
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True,unique=True)
    address = models.TextField(blank=True, null=True)
    pass

    def __str__(self):
        return self.username
    
User = get_user_model()
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ordered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # store snapshot of price at order time

    def get_total_price(self):
        return self.quantity * self.price
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
