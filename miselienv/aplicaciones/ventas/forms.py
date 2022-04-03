import uuid

from aplicaciones.shared_apps.models import TipDocumentoDetModel
from aplicaciones.stock.models import SubDepositoModel
from aplicaciones.ventas.models import PedidosModel, FacturasModel, RemisionesModel, ClientesModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Row, Column
from django import forms
from django.utils.timezone import now


class PedidosForm(forms.ModelForm):
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="PER"),
                                           initial="PER")
    nro_documento = forms.CharField(label='Nro Documento ', help_text="Cargar Nro documento")

    class Meta:
        model = PedidosModel
        fields = '__all__'


class RemisionesForm(forms.ModelForm):
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="PER"),
                                           initial="PER")
    nro_documento = forms.CharField(label='Nro Documento ', help_text="Cargar Nro documento")

    class Meta:
        model = RemisionesModel
        fields = '__all__'


class FacturasForm(forms.ModelForm):
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="FV"), initial="FV",
                                           label="Tip Doc")
    nro_documento = forms.CharField(label='Nro Documento ', required=True, help_text="Formato: 0010020000123")

    fecha_documento = forms.DateField(initial=now(), widget=forms.DateInput(attrs={'type': 'date'}))
    dep_origen = forms.ModelChoiceField(required=True, label="Deposito", queryset=SubDepositoModel.objects.all(), initial="1")
    cliente = forms.ModelChoiceField(required=True, label="Cliente", queryset=ClientesModel.objects.all(), initial="1")

    # cliente   = forms.ModelChoiceField(queryset=ClientesModel.objects.all(), widget=forms.TextInput)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_id = 'form_{uuid}'.format(uuid=uuid.uuid4())
    #     self.helper.form_class = 'form-inline'  # 'blueForms'
    #     self.helper.form_style = 'inline'
    #     self.helper.form_method = 'post'
    #     self.helper.form_action = ''
    #     self.helper.form_tag = False  # esto se agrega para que no quite el boton de adentro el formulario
    #     self.helper.layout = Layout(
    #         Row(
    #             Column(Field('tip_documento'), css_class="col-md-2"),
    #             Column(Field('nro_documento', css_class='text-end'), css_class="col-md-3 "),
    #             Column(Field('dep_origen'), css_class="col-md-2"),
    #
    #
    #         ),
    #         Row(
    #             Column(Field('fecha_documento')),
    #             Column(Field('fecha_transaccion')),
    #             Column(Field('periodo')),
    #             Column(Field('mes')),
    #         ),
    #         Row(
    #             Column(Field('conf_cuotas')),
    #             Column(Field('contado_credito')),
    #             Column(Field('moneda')),
    #             Column(Field('monto_mon_local')),
    #             Column(Field('saldo_mon_local')),
    #             Column(Field('cotizacion')),
    #         ),
    #         Row(
    #             Column(Field('cliente')),
    #             Column(Field('razon_social')),
    #             Column(Field('ruc')),
    #         ),
    #         'observaciones',
    #
    #     )

    class Meta:
        model = FacturasModel
        fields = '__all__'
