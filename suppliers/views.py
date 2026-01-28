from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from users import models
from django.db.models import Max
from .forms import SupplierForm
from users.models import UserRole
from .models import Suppliers

@login_required
def suppliers_list(request):
    # Obtener el rol del usuario
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__suppliers'))['max_permission'] or 0

    # Redirigir si no tiene permisos
    if max_permission == 0:
        return redirect('dashboard')

    # Obtener lista de Supplieres
    suppliers_list = Suppliers.objects.all()

    # Filtros por parámetros GET
    id_supplier = request.GET.get('id_supplier')
    name = request.GET.get('name')
    country = request.GET.get('country')
    status = request.GET.get('status')

    if id_supplier:
        suppliers_list = suppliers_list.filter(id_supplier__icontains=id_supplier)
    if name:
        suppliers_list = suppliers_list.filter(name__icontains=name)
    if country:
        suppliers_list = suppliers_list.filter(country__icontains=country)
    if status is not None and status != '':
        suppliers_list = suppliers_list.filter(status=status)

    if request.GET.get('export') == 'csv':
        # Exportar a CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Suppliers.csv"'

        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['ID Supplier', 'legal_name','Name', 'Tax ID','Country', 'State/Province',  
                         'City', 'Address', 'Zip Code', 'Phone', 'Email', 'Contact Name', 'Contact Role', 
                         'Category', 'Payment Terms', 'Currency', 'Payment Method', 'Bank Account', 'Status',
                         'Created By', 'Created At', 'Updated At'])

        for Supplier in suppliers_list:
            writer.writerow([
                Supplier.id_supplier,
                Supplier.legal_name,
                Supplier.name,
                Supplier.tax_id,
                Supplier.country,
                Supplier.state_province,
                Supplier.city,
                Supplier.address,
                Supplier.zip_code,
                Supplier.phone,
                Supplier.email,
                Supplier.contact_name,
                Supplier.contact_role,
                Supplier.category,
                Supplier.payment_terms,
                Supplier.currency,
                Supplier.payment_method,
                Supplier.bank_account,
                Supplier.status,
                Supplier.created_by.username if Supplier.created_by else 'N/A',
                Supplier.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                Supplier.updated_at.strftime('%Y-%m-%d %H:%M:%S') ,
            ])
        return response
    
    # Paginación
    paginator = Paginator(suppliers_list, 10)  # 10 Supplieres por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'suppliers/suppliers_list.html', {'page_obj': page_obj})
    
@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Suppliers, pk=pk)
    
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('suppliers:suppliers_list')
    if max_permission == 0:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:suppliers_list')
    else:
        form = SupplierForm(instance=supplier)
    
    context = {
        'form': form,
        'supplier': supplier,
    }

    return render(request, 'suppliers/suppliers_form.html', context)
    
@login_required
def supplier_delete(request, pk):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__suppliers'))['max_permission'] or 0

    if max_permission > 2:
        return redirect('suppliers:suppliers_list')
    supplier = get_object_or_404(Suppliers, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers:suppliers_list')
    return redirect('suppliers:suppliers_list')
       
    

@login_required
def suppliers_create(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('suppliers:suppliers_list')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            Supplier = form.save(commit=False)
            Supplier.created_by = request.user
            Supplier.save()

            return redirect('suppliers:suppliers_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/suppliers_form.html', {'form': form})