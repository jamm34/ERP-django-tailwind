from django.contrib import admin
from django.urls import path, include

# Custom error handlers
from core import views as core_views


handler404 = core_views.custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('materials/', include('materials.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('customers/', include('customers.urls')),
]
