from django.urls import path
from . import views


app_name = 'suppliers'

urlpatterns = [
    path('', views.suppliers_list, name='suppliers_list'),
    path('create/', views.suppliers_create, name='suppliers_create'),
    path('<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
]