from django import forms
from django.utils.timezone import now
from aplicaciones.base.choices import sexo, tipodocumento, personeria
from .models import EmpleadosModel, PersonasModel, EmpleadosBeneficiosModel


class EmpleadosForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    fecha_ingreso = forms.DateField(initial=now(), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    fecha_egreso = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    email = forms.EmailField()
    estado = forms.CheckboxSelectMultiple()

    class Meta:
        model = EmpleadosModel
        fields = '__all__'


class PersonasForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    personeria = forms.ChoiceField(choices=personeria)
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    razon_social = forms.CharField(max_length=200, required=True)
    direccion = forms.CharField(max_length=200, required=True)
    ruc = forms.CharField(max_length=100, required=False)
    dir_geo = forms.CharField(max_length=1000, required=False)
    sexo = forms.ChoiceField(required=True, choices=sexo)
    fecha_nac_const = forms.DateField(initial=now(), required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    tipo_documento = forms.ChoiceField(required=True, choices=tipodocumento)
    nro_documento = forms.CharField(max_length=100, required=False)
    fec_venc_doc_iden = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    nro_celular = forms.CharField(max_length=100, required=False)
    nro_whatsapp = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()

    class Meta:
        model = PersonasModel
        fields = '__all__'


class EmpleadosBeneficiosForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    empleado = forms.CheckboxSelectMultiple()
    beneficio = forms.CheckboxSelectMultiple()

    class Meta:
        model = EmpleadosBeneficiosModel
        fields = '__all__'
