from django.contrib import admin
from aplicaciones.stock.models import DepositoModel, SubDepositoModel, MarcaModel, ClasificacionModel
from aplicaciones.stock.models import GrupoModel, SubGrupoModel, MovimientosArticulosModel
from aplicaciones.stock.models import MovimientosDetArticulosModel, ArticulosModel, UnidadMedidaModel
from aplicaciones.stock.models import ArticuloSubDepositoModel

admin.site.register(UnidadMedidaModel)


@admin.register(ArticulosModel)
class ArticulosAdmin(admin.ModelAdmin):
    search_fields = ('desc_corta', 'desc_larga', )
    raw_id_fields = ("marca",) # buenisimo para no pre cargar los selects de tablas grandes
    list_display = (
                'desc_corta',
                'desc_larga',
                'cant_min',
                'mueve_stock',
                'marca',
    )
    fields = [('estado', 'mueve_stock'),
              'impuesto',
              ('desc_corta', 'desc_larga'),
              ('cant_min', 'cant_max',),
              ('codigo_barra', 'codigo_barra_alternativo'),
              ('precio_base',),
              ('marca', 'clasificacion', 'sub_grupo', 'un_medida'),
              ]


class InLineMovimientosDetArticulos(admin.TabularInline):
    model = MovimientosDetArticulosModel
    readonly_fields = ('nro_item',)
    extra = 1


class MovimientosArticulosAdmin(admin.ModelAdmin):
    inlines = [InLineMovimientosDetArticulos]
    list_display = ('tip_documento', 'nro_documento', 'fecha_documento', 'dep_origen',)

    readonly_fields = ('mes', 'periodo')  # campos de solo lectura

    # list_editable =
    list_filter = ['tip_documento__desc_larga', 'mes', 'periodo', ]
    search_fields = ('desc_corta', 'desc_larga', 'tip_documento__desc_corta')
    # formfield_overrides = ?????????
    # raw_id_fields = ??????
    fields = [
                'estado',
                ('tip_documento',   'nro_documento',),
                ('fecha_documento', 'mes', 'periodo',),
                ('dep_origen',      'dep_destino',), 'observaciones',
              ]

    def combinartipdocydoc(self, obj):
        return '{} - {}'.format(obj.tip_documento, obj.nro_documento)

    #  agregado para que manualmente indiquemos cuales son los tipos de documentos que pueden ser vistos en el admin
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(tip_documento__desc_corta__in=['FC', 'FV'])
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        return queryset


admin.site.register(MovimientosArticulosModel, MovimientosArticulosAdmin)


class InLineSubDeposito(admin.TabularInline):
    model = SubDepositoModel
    extra = 1


class DepositoAdmin(admin.ModelAdmin):
    inlines = [InLineSubDeposito]


admin.site.register(DepositoModel, DepositoAdmin)


class InLineSubGrupo(admin.TabularInline):
    model = SubGrupoModel
    extra = 1


class GrupoAdmin(admin.ModelAdmin):
    inlines = [InLineSubGrupo]


admin.site.register(GrupoModel, GrupoAdmin)


@admin.register(MarcaModel)
class MarcaAdmin(admin.ModelAdmin):
    pass


class InLineArticuloSubDeposito(admin.TabularInline):
    model = ArticuloSubDepositoModel
    extra = 1


class SubDepositoAdmin(admin.ModelAdmin):
    inlines = [InLineArticuloSubDeposito]
    extra = 1


admin.site.register(SubDepositoModel, SubDepositoAdmin)


@admin.register(ClasificacionModel)
class ClasificacionAdmin(admin.ModelAdmin):
    pass
