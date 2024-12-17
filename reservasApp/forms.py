from django import forms
from .models import *

#clase para editar reservas
class ReservaForm(forms.Form):
    class Meta:
        model = Reserva
        fields = ['nombre', 'telefono', 'fecha', 'hora', 'estado', 'personas', 'observacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Para que sea un selector de fechas
            'hora': forms.TimeInput(attrs={'type': 'time'}),    # Para que sea un selector de hora
            'observacion': forms.Textarea(attrs={'cols': 40, 'rows': 5}),  # Definir el tamaño del campo
        }

    def clean_personas(self):
        personas = self.cleaned_data['personas']
        if personas < 1 or personas > 15:
            raise forms.ValidationError('El número de personas debe estar entre 1 y 15.')
        return personas

#clase para agregar reservas
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['nombre', 'telefono', 'fecha', 'hora', 'estado', 'personas', 'observacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),  # Para que sea un selector de fechas
            'hora': forms.TimeInput(attrs={'type': 'time'}),    # Para que sea un selector de hora
            'observacion': forms.Textarea(attrs={'cols': 40, 'rows': 5}),  # Definir el tamaño del campo
        }

    def clean_personas(self):
        personas = self.cleaned_data['personas']
        if personas < 1 or personas > 15:
            raise forms.ValidationError('El número de personas debe estar entre 1 y 15.')
        return personas
