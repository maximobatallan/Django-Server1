from django.forms import ModelForm
from django import forms
from .models import Task, DatosPersonales, Producto
from django.forms.widgets import FileInput


class TaskForm (ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        
        
class DatosForm(ModelForm):
    class Meta:
        model = DatosPersonales
        fields = ['nombre', 'apellido', 'nacionalidad', 'ciudad', 
                  'telefono', 'nombreempresa', 'cbu', 'titular', 'descripcionempresa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nacionalidad'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefono'}),
            'nombreempresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Ecommerce'}),
            'cbu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CBU'}),
            'titular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titular de Cuenta'}),
            'descripcionempresa': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion del Ecommerce'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'important', 'cat', 'descripcion', 
                  'precio', 'imagen', 'imagen1', 'imagen2']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'cat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoria'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'imagen': FileInput(attrs={'class': 'form-control'}),
            'imagen1': FileInput(attrs={'class': 'form-control'}),
            'imagen2': FileInput(attrs={'class': 'form-control'}),
            
        }