from django import forms
from .models import Accidente


class AccidenteForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        label='Fecha del accidente',
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    latitud = forms.FloatField(
        required=False,
        label='Latitud',
        widget=forms.HiddenInput(attrs={'id': 'id_latitud'})
    )
    longitud = forms.FloatField(
        required=False,
        label='Longitud',
        widget=forms.HiddenInput(attrs={'id': 'id_longitud'})
    )

    class Meta:
        model = Accidente
        fields = ['titulo', 'ubicacion', 'descripcion', 'gravedad', 'fecha', 'latitud', 'longitud']
        labels = {
            'titulo': 'Título',
            'ubicacion': 'Ubicación',
            'descripcion': 'Descripción',
            'gravedad': 'Gravedad',
            'fecha': 'Fecha del accidente',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del accidente'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección o lugar', 'id': 'id_ubicacion'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el accidente...'}),
            'gravedad': forms.Select(attrs={'class': 'form-select'}),
        }
