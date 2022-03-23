from django import forms
from aplicaciones.shared_apps.models import TipDocumentoDetModel
from aplicaciones.ventas.models import PedidosModel, FacturasModel, RemisionesModel
from django.contrib.admin.widgets import FilteredSelectMultiple


class PedidosForm(forms.ModelForm):
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="PER"), initial="PER")
    nro_documento = forms.CharField(label='Nro Documento ', help_text="Cargar Nro documento")

    class Meta:
        model = PedidosModel
        fields = '__all__'


class RemisionesForm(forms.ModelForm):
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="PER"), initial="PER")
    nro_documento = forms.CharField(label='Nro Documento ', help_text="Cargar Nro documento")

    class Meta:
        model = RemisionesModel
        fields = '__all__'


class FacturasForm(forms.ModelForm):
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="FV"), initial="FV")
    nro_documento = forms.CharField(label='Nro Documento ', help_text="Ingresar Nro documento con formato: 0010020000123")

    class Meta:
        model = FacturasModel
        fields = '__all__'

