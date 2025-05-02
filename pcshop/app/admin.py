from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Brand, Product, CustomUser,Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'low_stock_warning')

    def low_stock_warning(self, obj):
        return "⚠️ Low!" if obj.stock < 5 else "✅ OK"
    low_stock_warning.short_description = "Stock Status"
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'ordered_at')
    list_filter = ('status',)

admin.site.register(Order, OrderAdmin)
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(CustomUser)