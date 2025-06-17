from django import forms

from .models import Trabajador


class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ["nombre", "apellido", "correo", "cedula", "codigo_empleado", "imagen"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el nombre"}
            ),
            "apellido": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ingrese el apellido"}
            ),
            "correo": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"}
            ),
            "cedula": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Número de cédula"}
            ),
            "codigo_empleado": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código del empleado"}
            ),
            "imagen": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data["cedula"]
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener solo números")
        if len(cedula) < 8:
            raise forms.ValidationError("La cédula debe tener al menos 8 dígitos")
        return cedula
