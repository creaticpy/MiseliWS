from django import forms
from django.utils.timezone import now
from aplicaciones.base.choices import entidadfinanciera, personeria, tipodocumento
from aplicaciones.tesoreria.models import EntidadesFinancierasModel
from aplicaciones.rrhh.models import PersonasModel


class EntidadesFinancierasForm(forms.ModelForm):
    id                  = forms.IntegerField(required=False)
    persona             = forms.IntegerField(required=False)
    tipo_entidad        = forms.ChoiceField(choices=entidadfinanciera, initial='BANCO')
    estado              = forms.CheckboxInput()
    observaciones       = forms.CharField(max_length=1000, required=False)

    class Meta:
        model = EntidadesFinancierasModel
        fields = '__all__'


class EntFinancierasPersonasForm(forms.ModelForm):
    id          = forms.IntegerField(required=False)
    personeria  = forms.ChoiceField(choices=personeria)
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    razon_social = forms.CharField(max_length=200, required=True)
    direccion = forms.CharField(max_length=200, required=True)
    ruc = forms.CharField(max_length=100, required=False)
    dir_geo = forms.CharField(max_length=1000, required=False)
    fecha_nac_const = forms.DateField(initial=now(), required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    tipo_documento = forms.ChoiceField(required=True, choices=tipodocumento)
    nro_documento = forms.CharField(max_length=100, required=False)
    nro_celular = forms.CharField(max_length=100, required=False)
    nro_whatsapp = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(label="Correo Personal")

    class Meta:
        model = PersonasModel
        fields = '__all__'

