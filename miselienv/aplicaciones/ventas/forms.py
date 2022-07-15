from aplicaciones.shared_apps.models import TipDocumentoDetModel
from aplicaciones.stock.models import SubDepositoModel
from aplicaciones.ventas.models import PedidosModel, FacturasModel, RemisionesModel, ClientesModel, FacturasDetModel, \
    ClientesSucursalesModel


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
    # error_css_class = 'error'
    # required_css_class = 'required'
    id = forms.IntegerField(required=False)
    tip_documento = forms.ModelChoiceField(queryset=TipDocumentoDetModel.objects.filter(desc_corta="FV"), initial="FV",
                                           label="Tip Doc")
    nro_documento = forms.CharField(label='Nro Documento', required=True, help_text="Formato: 0010020000123")

    fecha_documento = forms.DateField(initial=now(), widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    fecha_transaccion = forms.DateField(initial=now(), widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}))
    dep_origen = forms.ModelChoiceField(required=True, label="Deposito", queryset=SubDepositoModel.objects.all(),
                                        initial="1")
    cliente = forms.ModelChoiceField(required=True, label="Cliente", queryset=ClientesModel.objects.all(), initial="1")

    class Meta:
        model = FacturasModel
        fields = '__all__'

    def clean_conf_cuotas(self):
        conf_cuotas = self.cleaned_data.get("conf_cuotas")

        if self.cleaned_data.get("contado_credito") == 'CRED' and not conf_cuotas:
            raise forms.ValidationError("Debe seleccionar la cantidad de cuotas")

        return conf_cuotas


class FacturasDetForm(forms.ModelForm):
    class Meta:
        model = FacturasDetModel
        fields = '__all__'


class ClientesForm(forms.ModelForm):
    class Meta:
        model = ClientesModel
        fields = '__all__'


class ClientesSucursalesForm(forms.ModelForm):
    desc_corta      = forms.CharField(label='Descripcion', required=True, widget=forms.TextInput(attrs={'style': 'width: 250px'}))
    fec_ingreso     = forms.DateField(required=True, widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    observaciones   = forms.CharField(label='Observaciones', widget=forms.TextInput(attrs={'style': 'width: 250px'}))
    telefono        = forms.CharField(label='Telefono', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    celular         = forms.CharField(label='Celular', widget=forms.TextInput(attrs={'style': 'width: 100px'}))
    direccion       = forms.CharField(label='Direccion', widget=forms.TextInput(attrs={'style': 'width: 300px'}))
    dir_gps         = forms.CharField(label='GPS', widget=forms.TextInput(attrs={'style': 'width: 300px'}))
    encargado       = forms.CheckboxSelectMultiple()

    class Meta:
        model = ClientesSucursalesModel
        fields = '__all__'
