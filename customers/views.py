from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
import re
import io
from users import models
from django.db.models import Max
from .forms import CustomerForm, CsvUploadForm
from users.models import UserRole
from .models import Customers
from django.contrib import messages

@login_required
def customers_list(request):
    # Obtener el rol del usuario
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__customers'))['max_permission'] or 0

    # Redirigir si no tiene permisos
    if max_permission == 0:
        return redirect('dashboard')

    # Obtener lista de Customers
    customers_list = Customers.objects.all()

    # Filtros por parámetros GET
    id_customer = request.GET.get('id_customer')
    name = request.GET.get('name')
    country = request.GET.get('country')
    status = request.GET.get('status')

    if id_customer:
        customers_list = customers_list.filter(id_customer__icontains=id_customer)
    if name:
        customers_list = customers_list.filter(name__icontains=name)
    if country:
        customers_list = customers_list.filter(country__icontains=country)
    if status is not None and status != '':
        customers_list = customers_list.filter(status=status)

    if request.GET.get('export') == 'csv':
        # Exportar a CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Customers.csv"'

        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['ID Customer', 'legal_name','Name', 'Tax ID','Country', 'State/Province',  
                         'City', 'Address', 'Zip Code', 'Phone', 'Email', 'Contact Name', 'Contact Role', 
                         'Category', 'Payment Terms', 'Currency', 'Payment Method', 'Bank Account', 'Status',
                         'Created By', 'Created At', 'Updated At'])

        for Customer in customers_list:
            writer.writerow([
                Customer.id_customer,
                Customer.legal_name,
                Customer.name,
                Customer.tax_id,
                Customer.country,
                Customer.state_province,
                Customer.city,
                Customer.address,
                Customer.zip_code,
                Customer.phone,
                Customer.email,
                Customer.contact_name,
                Customer.contact_role,
                Customer.category,
                Customer.payment_terms,
                Customer.currency,
                Customer.payment_method,
                Customer.bank_account,
                Customer.status,
                Customer.created_by.username if Customer.created_by else 'N/A',
                Customer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                Customer.updated_at.strftime('%Y-%m-%d %H:%M:%S') ,
            ])
        return response
    
    # Paginación
    paginator = Paginator(customers_list, 10)  # 10 Customeres por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers/customers_list.html', {'page_obj': page_obj})
    
@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customers, pk=pk)
    
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__customers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('customers:customers_list')
    if max_permission == 0:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:customers_list')
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
    }

    return render(request, 'customers/customers_form.html', context)
    
@login_required
def customer_delete(request, pk):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__customers'))['max_permission'] or 0

    if max_permission > 2:
        return redirect('customers:customers_list')
    customer = get_object_or_404(Customers, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers:customers_list')
    return redirect('customers:customers_list')
       
    

@login_required
def customers_create(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__customers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('customers:customers_list')
    if max_permission == 0:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            Customer = form.save(commit=False)
            Customer.created_by = request.user
            Customer.save()

            return redirect('customers:customers_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customers_form.html', {'form': form})


@login_required
def customer_bulk_create(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=Max('role__customers'))['max_permission'] or 0
    
    if max_permission < 2:
        return redirect('customers:customers_list')
    
    if request.method == 'POST':
        form = CsvUploadForm(request.POST,request.FILES)
        
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            try:
                data_set = csv_file.read().decode('UTF-8')
            except UnicodeDecodeError:
                try:
                    csv_file.seek(0)
                    data_set = csv_file.read().decode('ISO-8859-1')
                except Exception as e:
                    return render(request, 'customers/customers_bulk_upload.html', {'form': form})
        
            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)

            if reader.fieldnames:
                if reader.fieldnames[0].startswith('\ufeff'):
                    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

                cleaned_fieldnames = [key.strip().lower() for key in reader.fieldnames]
                reader.fieldnames = cleaned_fieldnames

            successful_records = []
            error_records = []
            customers_to_create = []

            for i, row in enumerate(reader):
                row_number = i + 2
                form_data = {}

                for key, value in row.items():
                    cleaned_value = value.strip() if isinstance(value, str) else value 
                    form_data[key] = cleaned_value

                form = CustomerForm(form_data)

                if form.is_valid():
                    customer = form.save(commit=False)
                    customer.created_by = request.user
                    customers_to_create.append(customer)
                    successful_records.append({'row':row, 'data':form_data})
                else:
                    errors = {field:', '.join(err) for field, err in form.errors.items()}
                    error_records.append({
                        'row': row_number,
                        'data': form_data,
                        'errors': errors
                    })

            if customers_to_create:
                Customers.objects.bulk_create(customers_to_create)
            messages.success(request, f'Process finished. {len(successful_records)} customers created successfully')

            context = {
                'form': form,
                'successful_count': len(successful_records),
                'error_count': len(error_records),
                'total_rows': len(successful_records) + len(error_records),
                'error_records': error_records,
                'successful_records': successful_records,
                'report_generated': True
            }
            return render(request, 'customers/customers_bulk_upload.html', context)
        return render(request, 'customers/customers_bulk_upload.html', {'form': form})
    else:
        form = CsvUploadForm()
        return render(request, 'customers/customers_bulk_upload.html', {'form': form})


@login_required
def download_template_customers(request):
    header_fields = ['id_customer', 'legal_name', 'name', 'tax_id', 'country', 'state_province', 'city',
                     'address', 'zip_code', 'phone', 'email', 'contact_name', 'contact_role', 'category',
                     'payment_terms', 'currency', 'payment_method', 'bank_account', 'status']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_template.csv"'

    writer = csv.writer(response)
    writer. writerow(header_fields)
    
    return response
    