import pkgutil

from django.urls import path
from .views import FacturasView

app_name = 'ventas'

urlpatterns = [
    path('ventas/facturas', FacturasView.consultas, name='consultas_facturas'),
    path('ventas/agregar_facturas', FacturasView.agregar, name='agregar_facturas'),
    path('ventas/modificar_facturas', FacturasView.modificar, name='modificar_facturas'),
    path('ventas/borrar_facturas', FacturasView.borrar, name='borrado_facturas'),



    # path('ventas/facturas', FacturasView.as_view(redirect="consulta"), name='facturas'),
]
