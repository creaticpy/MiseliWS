import pkgutil

from django.urls import path
from .views import EmpleadosView

app_name = 'rrhh'

urlpatterns = [
    path('rrhh/empleados', EmpleadosView.consultas, name='consultas_empleados'),
    path('rrhh/agregar_empleados', EmpleadosView.agregar, name='agregar_empleados'),
    path('rrhh/modificar_empleados', EmpleadosView.modificar, name='modificar_empleados'),
    path('rrhh/borrar_empleados', EmpleadosView.borrar, name='borrado_empleados'),


    # path('ventas/facturas', FacturasView.as_view(redirect="consulta"), name='facturas'),
]
