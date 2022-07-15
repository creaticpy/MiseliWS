import pkgutil

from django.urls import path
from .views import EntidadesFinancierasView

app_name = 'tesoreria'

urlpatterns = [
    path('tesoreria/entidadesfinancieras', EntidadesFinancierasView.consultas, name='consultas_entidadesfinancieras'),
    path('tesoreria/agregar_entidadesfinancieras', EntidadesFinancierasView.agregar, name='agregar_entidadesfinancieras'),
    path('tesoreria/modificar_entidadesfinancieras', EntidadesFinancierasView.modificar, name='modificar_entidadesfinancieras'),
    path('tesoreria/borrar_entidadesfinancieras', EntidadesFinancierasView.borrar, name='borrado_entidadesfinancieras'),


    # path('ventas/facturas', FacturasView.as_view(redirect="consulta"), name='facturas'),
]
