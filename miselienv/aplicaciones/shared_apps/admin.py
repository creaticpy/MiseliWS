from aplicaciones.shared_apps.models import MenusSistemaModel
from aplicaciones.shared_apps.models import RucsModel, SubMenusSistemasModel, ClasificacionesMenusModel
from aplicaciones.shared_apps.models import PaisModel, ModulosSistemaModel, TipDocumentoDetModel, TipDocumentoModel
from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin


admin.site.register(PaisModel)


# class ClasificacionesMenusResource(resources.ModelResource):
#     class Meta:
#         model = ClasificacionesMenusModel


# @admin.register(ClasificacionesMenusModel)
# class ClasificacionesMenusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = ClasificacionesMenusResource


class InLineSubMenusSistemaAdmin(admin.TabularInline):
    model = SubMenusSistemasModel
    extra = 1


@admin.register(MenusSistemaModel)
class MenusSistemaAdmin(admin.ModelAdmin):
    inlines = [InLineSubMenusSistemaAdmin]


@admin.register(ModulosSistemaModel)
class ModulosSistemaAdmin(admin.ModelAdmin):
    pass


@admin.register(RucsModel)
class RucsAdmin(admin.ModelAdmin):
    search_fields = ['ruc_completo', 'razon_social',]


class InLineTipDocumentoDetAdmin(admin.TabularInline):
    model = TipDocumentoDetModel
    extra = 1


class TipDocumentoAdmin(admin.ModelAdmin):
    inlines = [InLineTipDocumentoDetAdmin]


admin.site.register(TipDocumentoModel, TipDocumentoAdmin)