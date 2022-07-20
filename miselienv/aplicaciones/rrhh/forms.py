from django import forms
from django.utils.timezone import now
from aplicaciones.base.choices import sexo, tipodocumento, personeria
from aplicaciones.shared_apps.models import TipDocumentoDetModel

from .models import EmpleadosModel, PersonasModel, EmpleadosBeneficiosModel
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class EmpleadosForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    fecha_ingreso_ips = forms.DateField(initial=now(), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), label='Ingreso IPS')
    fecha_egreso = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    email = forms.EmailField(label="Correo Laboral")
    estado = forms.CheckboxSelectMultiple()

    class Meta:
        model = EmpleadosModel
        fields = '__all__'

# https://regexr.com/


class PersonasForm(forms.ModelForm):
    id                  = forms.IntegerField(required=False)
    personeria          = forms.ChoiceField(choices=personeria)
    nombre              = forms.CharField(max_length=100, required=True)
    apellido            = forms.CharField(max_length=100, required=True)
    razon_social        = forms.CharField(max_length=200, required=True)
    direccion           = forms.CharField(max_length=200, required=True)
    dir_geo             = forms.CharField(max_length=1000, label="GPS",  required=False)
    sexo                = forms.ChoiceField(choices=sexo, required=False)
    fecha_nac_const     = forms.DateField(initial=now(), required=False, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    tip_documento_pers  = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(tip_documento="4").exclude(id=11), label="Tip Doc")
    nro_documento_pers  = forms.CharField(max_length=100, required=False, label='Nro Documento Personal',)
    fec_venc_doc_pers   = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    tip_documento       = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(id="11"), label="RUC")
    nro_documento       = forms.CharField(max_length=100, required=False, validators=[RegexValidator("(\d){5,8}-(\d)", message="not valid")], label="Nro RUC",
                                          help_text="Formato obligatorio Ej. 99999901-5")
    fec_venc_doc        = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}), required=False)
    nro_celular         = forms.CharField(max_length=100, required=False)
    nro_whatsapp        = forms.CharField(max_length=100, required=False)
    email               = forms.EmailField(label="Correo Personal")

    # def clean_nro_documento(self):  # actualmente usado solo para RUC ----> DONT WORKING
    #     if self.clean_nro_documento is not None and self.tip_documento is not None:
    #         return
    #     elif self.clean_nro_documento is None and self.tip_documento is None:
    #         return
    #     elif bool(self.clean_nro_documento is None) != bool(self.tip_documento is None):
    #         raise ValidationError('Verifique Tipo de documento y RUC')

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
