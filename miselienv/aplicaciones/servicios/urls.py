from django.urls import path
# from .views import EmpleadosView
from aplicaciones.servicios.views import ServiciosView

app_name = 'servicios'

urlpatterns = [
    path('srv/consultar_tablero', ServiciosView.consultar_tablero, name='consultar_tablero'),
    # path('rrhh/agregar_empleados', EmpleadosView.agregar, name='agregar_empleados'),
    # path('rrhh/modificar_empleados', EmpleadosView.modificar, name='modificar_empleados'),
    # path('rrhh/borrar_empleados', EmpleadosView.borrar, name='borrado_empleados'),


    # path('ventas/facturas', FacturasView.as_view(redirect="consulta"), name='facturas'),
]
