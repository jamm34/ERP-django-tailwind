from django.contrib import admin
from .models import Country, Currency, Status


# Register your models here.


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", )

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "code")

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin): 
    list_display = ('name', 'code')