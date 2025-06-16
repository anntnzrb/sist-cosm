from django import forms
from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'descripcion', 'telefono', 'pais', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del proveedor'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+57 123 456 7890'}),
            'pais': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País de origen'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'proveedor@ejemplo.com'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'}),
        }
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        # Remove spaces and special characters for validation
        clean_phone = ''.join(filter(str.isdigit, telefono))
        if len(clean_phone) < 7:
            raise forms.ValidationError("El teléfono debe tener al menos 7 dígitos")
        return telefono