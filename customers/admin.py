from .models import Customers
from django.contrib import admin

# Register your models here.
@admin.register(Customers)
class UnitMeasureAdmin(admin.ModelAdmin):
    list_display = ("name",)