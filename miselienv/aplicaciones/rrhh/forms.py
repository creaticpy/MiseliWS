from django import forms
from django.utils.timezone import now
from .models import EmpleadosModel, PersonasModel


class EmpleadosForm(forms.ModelForm):
    class Meta:
        model = EmpleadosModel
        fields = '__all__'


class PersonasForm(forms.ModelForm):
    class Meta:
        model = PersonasModel
        fields = '__all__'
