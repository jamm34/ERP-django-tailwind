from django import forms
from .models import Customers


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ['id_customer',
                  'legal_name',
                  'name',
                  'tax_id',
                  'country', 
                  'state_province', 
                  'city', 
                  'address',
                  'zip_code',
                  'phone',
                  'email',
                  'contact_name',
                  "contact_role",
                  "category",
                  "payment_terms",
                  "currency",
                  'payment_method',
                  'bank_account',
                  "status",
                  ]
        
class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Customers CSV File',
        help_text='The file content headers that match the model fields.'
    )