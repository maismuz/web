# myapp/forms.py
from django import forms
from .models import Veiculo, TipoVeiculo, Combustivel

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
               isinstance(field.widget, forms.NumberInput) or \
               isinstance(field.widget, forms.EmailInput) or \
               isinstance(field.widget, forms.URLInput) or \
               isinstance(field.widget, forms.PasswordInput) or \
               isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'