from aplicaciones.shared_apps.models import MonedaModel
from django.contrib import admin

from .models import CotizacionModel, ImpuestosModel, ImpuestosDetModel, ConfFinanzasModel
from .models import CondCompVentModel, ConfCuotasModel


admin.site.register(MonedaModel)
admin.site.register(ConfFinanzasModel)


@admin.register(CotizacionModel)
class CotizacionAdmin(admin.ModelAdmin):
    search_fields = ('moneda',)
    list_filter = ('moneda', 'fecha',)
    list_display = ('fecha', 'moneda', 'compra', 'venta', )
#     radio_fields = {"moneda": admin.HORIZONTAL} PARA TENER EN CUENTA, NO CAMBA LA FORMA DE PRESENTAR LAS FOREIGN KEY


class InLineImpuestosDetAdmin(admin.TabularInline):
    model = ImpuestosDetModel
    readonly_fields = ('nro_item',)


class ImpuestosAdmin(admin.ModelAdmin):
    inlines = [InLineImpuestosDetAdmin]


admin.site.register(ImpuestosModel, ImpuestosAdmin)


@admin.register(ConfCuotasModel)
class ConfCuotasAdmin(admin.ModelAdmin):
    list_display = ('desc_corta', 'cant_cuotas',)
    fields = (
        'desc_corta',
        'desc_larga',
        'cant_cuotas',
        'cant_dias_primera_cuota',
        'pago_anticipado',
        'venc_fecha_fija',
        'pri_cuota_mes_factura',

    )

    def get_queryset(self, request):  # dejo aqui solo para ejemplo
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter()
        return qs.filter(author=request.user)


@admin.register(CondCompVentModel)
class CondCompVentModelAdmin(admin.ModelAdmin):
    pass