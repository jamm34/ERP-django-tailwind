from django.contrib import admin
from .models import Unit, MaterialType
# Register your models here.

@admin.register(Unit)
class UnitMeasureAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("name", )
