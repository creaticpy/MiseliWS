import pkgutil

from django.urls import path
from .views import FacturasView, ClientesView

app_name = 'ventas'

urlpatterns = [
    path('ventas/facturas', FacturasView.consultas, name='consultas_facturas'),
    path('ventas/agregar_facturas', FacturasView.agregar, name='agregar_facturas'),
    path('ventas/modificar_facturas', FacturasView.modificar, name='modificar_facturas'),
    path('ventas/borrar_facturas', FacturasView.borrar, name='borrado_facturas'),

    path('ventas/clientes', ClientesView.consultas, name='consultas_clientes'),
    path('ventas/agregar_clientes', ClientesView.agregar, name='agregar_clientes'),
    path('ventas/modificar_clientes', ClientesView.modificar, name='modificar_clientes'),
    path('ventas/borrar_clientes', ClientesView.borrar, name='borrado_clientes'),

    # path('ventas/facturas', FacturasView.as_view(redirect="consulta"), name='facturas'),
]
