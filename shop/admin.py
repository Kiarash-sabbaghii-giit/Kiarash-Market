from django.contrib import admin
from .models import UserInfo, Cart, Order, OrderItem, Category

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'phone')
    # list_filter رو حذف کن چون created_at وجود نداره

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'product_name', 'quantity', 'product_price')
    search_fields = ('product_name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'user_phone', 'total_amount', 'status', 'created_at')
    list_editable = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_fa', 'category_en', 'image_url')
    search_fields = ('category_fa', 'category_en')