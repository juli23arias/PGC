from django import forms
from .models import NormaTransito


class NormaForm(forms.ModelForm):
    class Meta:
        model = NormaTransito
        fields = ['titulo', 'descripcion', 'categoria', 'articulo']
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'articulo': 'Artículo de la ley',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la norma'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'articulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Art. 77, Ley 769 de 2002'}),
        }
