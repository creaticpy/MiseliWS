from django.db import models
from django.conf import settings
from core.models import Maestros, BaseModel
from aplicaciones.base.choices import sumaoresta
from aplicaciones.base.choices import tipocomprobante


# Create your models here.

class RucsModel(BaseModel):
    personeria          = models.CharField(max_length=1)
    ruc_completo        = models.CharField(max_length=100)
    ruc                 = models.CharField(max_length=100)
    dv                  = models.CharField(max_length=1)
    razon_social        = models.CharField(max_length=100)
    fecha_actualizacion = models.DateField()
    categoria           = models.CharField(max_length=100)
    codigo              = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'RUC'
        verbose_name_plural = 'RUCs'

    def __str__(self):
        return '{razon_social}, {ruc}'.format(ruc=self.ruc_completo, razon_social=self.razon_social)


class PaisModel(Maestros):
    class Meta:
        verbose_name = 'pais'
        verbose_name_plural = 'paises'


class ClasificacionesMenusModel(Maestros):
    class Meta:
        verbose_name = 'Clasificacion'
        verbose_name_plural = 'Clasificaciones'


class ModulosSistemaModel(Maestros):

    class Meta:
        verbose_name = "modulo SAAS"
        verbose_name_plural = 'modulos SAAS'


class MenusSistemaModel(Maestros):
    orden_visualizacion = models.PositiveIntegerField(default=0)
    modulo              = models.ForeignKey(ModulosSistemaModel, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name = "Menu SAAS"
        verbose_name_plural = 'Menus SAAS'


class SubMenusSistemasModel(Maestros):
    menu                    = models.ForeignKey(MenusSistemaModel, on_delete=settings.DB_ON_DELETE_TRANS)
    clasificacion_menu      = models.ForeignKey(ClasificacionesMenusModel, on_delete=settings.DB_ON_DELETE_TRANS)
    # nombre_modelo           = models.CharField(max_length=100, blank=False, null=False) Creo que no lo vamos a necesitar.
    orden_visualizacion     = models.PositiveIntegerField(default=0)
    url                     = models.CharField(max_length=100, blank=False, null=False)
    charger_function        = models.CharField(max_length=100, blank=False, null=False, default="Elegir funcion Adecuada")

    class Meta:
        verbose_name = "Sub Modulo SAAS"
        verbose_name_plural = 'Sub Modulos SAAS'


class TipDocumentoModel(Maestros):
    class Meta:
        verbose_name = 'tipo documento'
        verbose_name_plural = 'tipos de documentos'


class TipDocumentoDetModel(Maestros):
    modulo = models.ForeignKey(ModulosSistemaModel, on_delete=settings.DB_ON_DELETE_TRANS)
    tip_documento = models.ForeignKey(TipDocumentoModel, on_delete=settings.DB_ON_DELETE_TRANS)
    suma_resta = models.CharField(max_length=20, choices=sumaoresta, blank=True, null=True)
    tip_comprobante = models.CharField(max_length=10, choices=tipocomprobante)

    class Meta:
        verbose_name = 'detalle tipo documento'
        verbose_name_plural = 'detalles de tipos de documentos'

    def __str__(self):
        return '{desc_corta}'.format(desc_corta=self.desc_corta, modulo=self.modulo.desc_corta)


class MonedaModel(Maestros):
    pais = models.ForeignKey(PaisModel, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name = 'moneda'
        verbose_name_plural = 'monedas'


class ConceptosDocumentosModel(Maestros):
    tip_documento_det = models.ForeignKey(TipDocumentoDetModel, on_delete=settings.DB_ON_DELETE_TRANS)


class FormasPagosCobrosModel(Maestros):
    pass
