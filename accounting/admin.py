from django.contrib import admin
from .models import AccountNature, AccountGroup, AccountType, AccountAccount
# Register your models here.


@admin.register(AccountNature)
class AccountNatureAdmin(admin.ModelAdmin): 
    list_display = ('id_account_nature', 'name', 'symbol', 'effect_on_balance')

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('id_account_group', 'name', 'code_prefix', 'description', 'created_by')

@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):   
    list_display = ('id_account_type', 'name', 'description')

@admin.register(AccountAccount)
class AccountAccountAdmin(admin.ModelAdmin):
    list_display = ('id_account', 'name', 'code', 'account_type','account_group', 'nature', 'is_control_account', 'status')


