from django.urls import path
from . import views


app_name = 'materials'

urlpatterns = [
    path('', views.materials_list, name='materials'),
    path('create/', views.materials_create, name='materials_create'),
    path('<int:pk>/edit/', views.material_edit, name='material_edit'),
    path('<int:pk>/delete/', views.material_delete, name='material_delete'),
]