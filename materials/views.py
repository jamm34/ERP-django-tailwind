from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from users import models
from django.db.models import Max
from .forms import MaterialForm
from users.models import UserRole
from .models import Material

@login_required
def materials_list(request):
    # Obtener el rol del usuario
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__materials'))['max_permission'] or 0

    # Redirigir si no tiene permisos
    if max_permission == 0:
        return redirect('dashboard')

    # Obtener lista de materiales
    materials_list = Material.objects.all()

    # Filtros por parámetros GET
    id_material = request.GET.get('id_material')
    name = request.GET.get('name')
    material_type = request.GET.get('material_type')
    status = request.GET.get('status')

    if id_material:
        materials_list = materials_list.filter(id_material__icontains=id_material)
    if name:
        materials_list = materials_list.filter(name__icontains=name)
    if material_type:
        materials_list = materials_list.filter(material_type__icontains=material_type)
    if status is not None and status != '':
        materials_list = materials_list.filter(status=status)

    # Paginación
    paginator = Paginator(materials_list, 10)  # 10 materiales por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materials/materials_list.html', {'page_obj': page_obj})
    

@login_required
def materials_create(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST)

        if form.is_valid():
            material = form.save(commit=False)
            material.created_by = request.user
            material.save()

            return redirect('materials:materials')
    else:
        form = MaterialForm()
    return render(request, 'materials/materials_form.html', {'form': form})