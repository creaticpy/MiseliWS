from django.db import models
from django.conf import settings

from core.models import Maestros, BaseModel, MovArticulosDetModel, PeriodosModel
from core.models import CabMovArticulosModel

from aplicaciones.base.models import SucursalesModel
from aplicaciones.finanzas.models import ImpuestosDetModel


class UnidadMedidaModel(Maestros):
    class Meta:
        verbose_name = "unidad de medida"
        verbose_name_plural = "unidades de medida"


class DepositoModel(Maestros):
    sucursal = models.ForeignKey(SucursalesModel, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name = "deposito"
        verbose_name_plural = "depositos"


class SubDepositoModel(Maestros):
    deposito = models.ForeignKey(DepositoModel, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name = "subdeposito"
        verbose_name_plural = "sub depositos"

    def __str__(self):
        return self.desc_corta


class MarcaModel(Maestros):

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marcas"


class GrupoModel(Maestros):

    class Meta:
        verbose_name = "grupo"
        verbose_name_plural = "grupos"


class SubGrupoModel(Maestros):
    grupo = models.ForeignKey(GrupoModel, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name = "sub grupo"
        verbose_name_plural = "sub grupos"


class ClasificacionModel(Maestros):
    class Meta:
        verbose_name = "Clasificacion"
        verbose_name_plural = "Clasificaciones"


class ArticuloSubDepositoModel(BaseModel):
    # -------------------> modelo Articulo/SubDeposito
    sub_deposito = models.ForeignKey(SubDepositoModel, on_delete=settings.DB_ON_DELETE_TRANS)
    articulo = models.ForeignKey('ArticulosModel', on_delete=settings.DB_ON_DELETE_TRANS)
    cantidad = models.IntegerField(default=0)  # aqui si puede ser negativo, depende de la politica de cada empresa
    cant_min = models.PositiveIntegerField(help_text="Configuracion predeterminada pero aplicada al deposito/articulo")
    cant_max = models.PositiveIntegerField(help_text="Configuracion predeterminada pero aplicada al deposito/articulo")

    class Meta:
        constraints = [models.UniqueConstraint(fields=['sub_deposito', 'articulo'], name='artsubdepconstraint')]

    def __str__(self):
        return '{articulo} - {marca} - {deposito}'.format(articulo=self.articulo.desc_corta,
                                                          marca=self.articulo.marca.desc_corta,
                                                          deposito=self.sub_deposito.desc_corta)


class ArticulosModel(Maestros):
    mueve_stock              = models.BooleanField(default=True)
    cant_min                 = models.PositiveIntegerField(help_text="Configuracion predeterminada, se copiará a cada nuevo deposito")
    cant_max                 = models.PositiveIntegerField(help_text="Configuracion predeterminada, se copiará a cada nuevo deposito")
    marca                    = models.ForeignKey(MarcaModel, on_delete=settings.DB_ON_DELETE_TRANS)
    un_medida                = models.ForeignKey(UnidadMedidaModel, on_delete=settings.DB_ON_DELETE_TRANS)
    sub_grupo                = models.ForeignKey(SubGrupoModel, on_delete=settings.DB_ON_DELETE_TRANS)

    clasificacion            = models.ForeignKey(ClasificacionModel, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS)

    codigo_barra             = models.CharField(max_length=100, blank=True, null=False)
    codigo_barra_alternativo = models.CharField(max_length=100, blank=True, null=False, verbose_name="Cod. Barras Alter.")

    impuesto                 = models.ForeignKey(ImpuestosDetModel, default=1, on_delete=settings.DB_ON_DELETE_TRANS)
    precio_base              = models.PositiveIntegerField(default=0, blank=False, null=False)

    sub_deposito             = models.ManyToManyField(SubDepositoModel, through=ArticuloSubDepositoModel)

    class Meta:
        verbose_name = 'articulo'
        verbose_name_plural = 'articulos'

    def __str__(self):
        return '{desc_corta}, {desc_larga},  {marca}'.format(desc_corta=self.desc_corta, desc_larga=self.desc_larga, marca=self.marca)


class ArticulosImagenesModel(Maestros):
    articulo = models.ForeignKey(ArticulosModel, on_delete=settings.DB_ON_DELETE_TRANS)


class MovimientosArticulosModel(CabMovArticulosModel):

    class Meta:
        verbose_name = "movimiento de articulo"
        verbose_name_plural = "movimientos de articulos"
        constraints = [models.UniqueConstraint(fields=['tip_documento', 'nro_documento'], name='movartsconstraint')]


class MovimientosDetArticulosModel(MovArticulosDetModel):
    movimiento_articulo = models.ForeignKey(MovimientosArticulosModel, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name        = "detalle de movimiento de articulo"
        verbose_name_plural = "detalles de movimientos de articulos"
        constraints = [models.UniqueConstraint(fields=['movimiento_articulo', 'nro_item'], name='movdetartconstraint'),]

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if self._state.adding:
        #     if self.nro_item is None and not self.nro_item:
        #         self.nro_item = cal_key(MovimientosDetArticulosModel, "movimientoarticulos", self.movimiento_articulo.id)
        #     if self.movimiento_articulo.entradaosalida == 'E':
        #         artcant = ArticuloSubDepositoModel.objects.filter(id=self.articulo.id)
        #         artcant.update(cantidad=models.F('cantidad')+self.cantidad)  # https://docs.djangoproject.com/en/4.0/ref/models/expressions/
        #     elif self.movimiento_articulo.entradaosalida == 'S':
        #         artcant = ArticuloSubDepositoModel.objects.filter(id=self.articulo.id)
        #         artcant.update(cantidad=models.F('cantidad')-self.cantidad)
        #         # no existe el caso de modificacion puesto que el registro debe borrarse y volverse a cargar.
        # super(MovimientosDetArticulosModel, self).save(force_insert, force_update, using, update_fields)


class AcumuladorArticulos(PeriodosModel):
    articulo                 = models.ForeignKey(ArticulosModel, on_delete=settings.DB_ON_DELETE_TRANS)
    precio_compra_promedio   = models.PositiveIntegerField(default=0, blank=False, null=False)
    precio_venta_promedio    = models.PositiveIntegerField(default=0, blank=False, null=False)
    precio_ultima_compra     = models.PositiveIntegerField(default=0, blank=False, null=False)
    precio_ultima_venta      = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'articulo'
        verbose_name_plural = 'articulos'
