from django.contrib import admin
from .models import OrderStatus


# Register your models here.
@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')