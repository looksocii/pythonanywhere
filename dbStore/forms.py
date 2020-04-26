from django import forms
from management.models import *

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = (
            'store_id', 
            'store_name', 
            'store_pic', 
            'branch', 
            'phone', 
            'cost_total', 
            'repaired', 
            'other_notes', 
            'manage_manag_id', 
            'company_company_id'
        )
        widgets = {
            'store_name': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'store_pic': forms.FileInput(
                attrs={
                    'class':'file-upload',
                    'onchange':'readURL(this);'
                }
            ),
            'branch': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'cost_total': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'repaired': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),
            'other_notes': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':'4'
                }
            ),
        }

class CostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = (
            'electric_bill',
            'water_bill',
            'rent_fee',
            'repair_fee',
            'insurance_fee',
            'other_fee',
            'accountant_employee_emp_id',
            'store_store_id'
        )