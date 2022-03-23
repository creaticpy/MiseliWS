from aplicaciones.base.admin import BocasEmpleadosAdmin
from aplicaciones.base.models import UserProfile
from django.contrib import admin
from .models import PersonasModel, EmpleadosSucursalesModel, EmpleadosModel

# Register your models here.

admin.site.register(PersonasModel)
# admin.site.register(models.Clientes)


@admin.register(EmpleadosModel)
class EmpleadosAdmin(admin.ModelAdmin):
    raw_id_fields = ['id', 'contacto_emergencia',]
    search_fields = ["id"]



@admin.register(EmpleadosSucursalesModel)
class EmpleadosSucursalesAdmin(admin.ModelAdmin):
    raw_id_fields = ['empleado',]
    fields = ['estado', 'empleado', 'sucursal']
    list_display = ['estado', 'empleado', 'sucursal']
    list_display_links = ['estado', 'empleado']

    def get_queryset(self, request):
        queryset = EmpleadosSucursalesModel.filter_objects.basic_filter(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        return queryset

