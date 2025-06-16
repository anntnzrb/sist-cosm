from django import forms
from .models import Empresa
from datetime import datetime


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'direccion', 'mision', 'vision', 'anio_fundacion', 'ruc', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'}),
            'mision': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Misión de la empresa'}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Visión de la empresa'}),
            'anio_fundacion': forms.NumberInput(attrs={'class': 'form-control', 'min': '1800', 'max': str(datetime.now().year)}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUC de la empresa'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def clean_anio_fundacion(self):
        anio = self.cleaned_data['anio_fundacion']
        current_year = datetime.now().year
        if anio < 1800 or anio > current_year:
            raise forms.ValidationError(f"El año debe estar entre 1800 y {current_year}")
        return anio