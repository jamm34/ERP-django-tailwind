from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import UserRole


def custom_404_view(request, exception=None):
    # Nota: Django pasa `exception` a handler404; lo mantenemos opcional.
    return render(request, '404.html', status=404)


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard_view(request):
    user_roles = UserRole.objects.filter(user_id= request.user)

    permissions = {
        'customers': 0,
        'suppliers': 0,
        'materials': 0,
        'purchases': 0,
        'sales': 0,
        'inventory': 0,
        'accounting': 0,
        'reporting': 0,
    }

    for user_role in user_roles:
        role = user_role.role
        for module in permissions.keys():
            current_permission = getattr(role, module)
            if current_permission > permissions[module]:
                permissions[module] = current_permission
    
    context = {
        'user': request.user,
        'permissions': permissions,
        'roles': [ur.role.role_name for ur in user_roles],
    }
    
    return render(request, 'core/dashboard.html', context)
