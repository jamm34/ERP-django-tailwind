import json
from django.http import JsonResponse 
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Max, Q
from django.http import Http404
from .models import PurchaseOrder, LinesPurchaseOrder, OrderStatus
from suppliers.models import Suppliers
from materials.models import Material, Unit
from core.models import Currency
from django.shortcuts import render
from django.db import transaction

# Create your views here.

def get_supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Suppliers, id_supplier=supplier_id)
    data = {
        'id_supplier': supplier.id_supplier,
        'name': supplier.name,
        'address': supplier.address,
        'legal_name': supplier.legal_name,
        'tax_id': supplier.tax_id,
        'city': supplier.city,
        'state_province': supplier.state_province,
        'country': supplier.country,
        'zip_code': supplier.zip_code,
        'phone': supplier.phone,
        'email': supplier.email,
        'contact_name': supplier.contact_name,
        'payment_terms': supplier.payment_terms,
        'currency': supplier.currency

    }
    return JsonResponse(data)

def get_material_detail(request, material_id):
    material = get_object_or_404(Material, id_material=material_id)
    data = {
        'id_material': material.id_material,
        'unit': material.unit.symbol if material.unit else None,
        'description': material.description,
        

    }
    return JsonResponse(data)


def purchase_order_form(request):
    context = {
        'title': "Create new purchase order",
    }
    return render(request, 'purchases/purchase_order_create.html', context)

@csrf_exempt
@require_POST
@transaction.atomic
def create_purchase_order(request):
    try:
        data = json.loads(request.body)

        supplier_id_str = data.get('supplier_id') or data.get('id_supplier')
        estimated_delivery_date = data.get('estimated_delivery_date')
        lines_data = data.get('lines', [])
        if not supplier_id_str:
            return JsonResponse({'error': 'Supplier ID is required.'}, status=400)
        if not estimated_delivery_date:
            return JsonResponse({'error': 'Estimated delivery date is required.'}, status=400)
        if not lines_data:
            return JsonResponse({'error': 'At least one line item is required.'}, status=400)
        
        supplier_id_value = str(supplier_id_str).strip()
        try:
            supplier = get_object_or_404(Suppliers, id_supplier=supplier_id_value)
        except Http404:
            return JsonResponse({'error': f'Supplier "{supplier_id_value}" not found.'}, status=400)

        status = OrderStatus.objects.filter(pk=2).first() or OrderStatus.objects.first()
        if not status:
            return JsonResponse({'error': 'No order status configured.'}, status=400)
        
        max_id_result = PurchaseOrder.objects.aggregate(max_id=Max('id_purchase_order'))
        last_id_str = max_id_result['max_id']

        next_po_number = 1
        if last_id_str:
            try:
                next_po_number = int(last_id_str) + 1
            except ValueError:
                print(f'Warning: the last ID "{last_id_str}" is not a valid integer')
                next_po_number = 1  
        next_po_id = str(next_po_number)

        purchase_order = PurchaseOrder.objects.create(
            id_purchase_order=next_po_id,
            id_supplier=supplier,
            estimated_delivery_date=estimated_delivery_date,
            status=status,
            created_by=request.user
        )
        for i, line_data in enumerate(lines_data, start=1):
            material_id = line_data.get('id_material')
            unit_symbol = line_data.get('unit_material')
            currency_symbol = line_data.get('currency_supplier')
            quantity = line_data.get('quantity')
            price = line_data.get('price')
            position = line_data.get('position', i)

            material = Material.objects.filter(id_material=material_id).first()
            if not material:
                raise ValueError(f'Material with ID {material_id} not found for line {i}.')

            unit_obj = Unit.objects.filter(symbol=unit_symbol).first()
            if not unit_obj:
                raise ValueError(f'Unit "{unit_symbol}" not found for line {i}.')

            currency_obj = Currency.objects.filter(
                Q(code__iexact=currency_symbol) | Q(name__iexact=currency_symbol)
            ).first()
            if not currency_obj:
                raise ValueError(f'Currency "{currency_symbol}" not found for line {i}.')
            
            line_po_id = f"{next_po_id}--{str(position).zfill(3)}"
                

            LinesPurchaseOrder.objects.create(
                id_purchase_order_line=line_po_id,
                id_purchase_order=purchase_order,
                id_material=material,
                position=position,
                quantity=quantity,
                unit_material=unit_obj,
                currency_supplier=currency_obj,
                price=price,
                received_quantity=0,
                created_by=request.user
            )
        
        response_data = {
            'success': True,
            'id_purchase_order': next_po_id,
            'message': f"Purchase order {next_po_id} created successfully.",
            'redirect_url': "/purchases/purchase_list/"
        }
        return JsonResponse(response_data, status=201)
    except ValueError as e:
        return JsonResponse({'error': f"Validation error: {str(e)}"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return JsonResponse({'error': f"An unexpected server error: {str(e)}"}, status=500)
