from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    def __str__(self):
        return self.name
    
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True,unique=True)
    address = models.TextField(blank=True, null=True)
    pass

    def __str__(self):
        return self.username