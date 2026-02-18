from django.contrib import admin
from .models import LocationInventory, MovementType, InventoryMovements
# Register your models here.


@admin.register(LocationInventory)
class LocationInventoryAdmin(admin.ModelAdmin):
    list_display = ('id_location', 'name', 'code', 'status', 'main_location', 'location')

@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')

@admin.register(InventoryMovements)
class InventoryMovementsAdmin(admin.ModelAdmin):
    list_display = ('id_inventory_movement', 'id_location', 'id_material', 'quantity', 'unit_type', 'movement_type')