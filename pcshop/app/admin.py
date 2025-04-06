from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Brand, Product, CustomUser

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CustomUser)

