from django.db import models
from django.conf import settings
from django.utils.timezone import now
from aplicaciones.base.functions import cal_key
from core.models import BaseModel, Maestros, MaestrosDet


class CotizacionModel(BaseModel):
    moneda = models.ForeignKey('shared_apps.MonedaModel', on_delete=settings.DB_ON_DELETE_TRANS)
    compra = models.DecimalField(max_digits=10, decimal_places=0)
    venta = models.DecimalField(max_digits=10, decimal_places=0)
    fecha = models.DateField(default=now)

    class Meta:
        verbose_name = 'Cotizacion'
        verbose_name_plural = 'Cotizaciones'
        constraints = [models.UniqueConstraint(fields=['moneda', 'fecha'], name='cotimonfecsconst')]

    def __str__(self):
        return '{fecha} - {moneda}'.format(fecha=self.fecha, moneda=self.moneda.desc_corta)


class ImpuestosModel(Maestros):
    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos'


class ImpuestosDetModel(MaestrosDet):
    impuesto = models.ForeignKey(ImpuestosModel, on_delete=settings.DB_ON_DELETE_TRANS)
    formula = models.CharField(max_length=100, blank=True, null=True)
    valor1 = models.PositiveIntegerField(default=0)
    valor2 = models.PositiveIntegerField(default=0)
    valor3 = models.PositiveIntegerField(default=0)
    valor4 = models.PositiveIntegerField(default=0)
    valor5 = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'detalle impuesto'
        verbose_name_plural = 'detalles impuestos'
        constraints = [models.UniqueConstraint(fields=['impuesto', 'nro_item'], name='impdetconstraint')]

    def __str__(self):
        return '{desc_corta}'.format(desc_corta=self.desc_corta)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            self.nro_item = cal_key(ImpuestosDetModel, "impuesto", self.impuesto.id)

        super(ImpuestosDetModel, self).save(force_insert, force_update, using, update_fields)


class CondCompVentModel(Maestros):
    class Meta:
        verbose_name = 'Condicion compra/venta'
        verbose_name_plural = 'Condiciones de compra/venta'

    def __str__(self):
        return self.desc_corta


class ConfCuotasModel(Maestros):
    cant_cuotas                 = models.PositiveIntegerField(default=0)
    cant_dias_primera_cuota     = models.PositiveIntegerField(default=3)
    pago_anticipado             = models.BooleanField(default=False)
    venc_fecha_fija             = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name="Dia del Vencimiento Fijo", help_text="Dia del mes de cada cuota")
    pri_cuota_mes_factura       = models.BooleanField(default=True, verbose_name="Primera cuota en mes de factura",
                                                      help_text="Si la primera cuota se cuenta en el mismo "
                                                      "mes de la factura. Ej. Si una factura tiene"
                                                      "fecha 25 y fecha fija = True y esta "
                                                      "configurada al 26 de cada mes entonces la"
                                                      "primera cuota se daria recien el siguiente "
                                                      "mes")

    class Meta:
        verbose_name = "configuracion de cuota"
        verbose_name_plural = "configuraciones de cuotas"

    def __str__(self):
        return self.desc_corta


class ConfFinanzasModel(BaseModel):
    moneda_local        = models.ForeignKey('shared_apps.MonedaModel', related_name="moneda_local", default=1, on_delete=settings.DB_ON_DELETE_TRANS, verbose_name="Moneda Local")
    moneda_secundaria   = models.ForeignKey('shared_apps.MonedaModel', related_name="moneda_secundaria", default=2, on_delete=settings.DB_ON_DELETE_TRANS, verbose_name="Moneda secundaria",
                                            help_text="Es la moneda con la cual es estaremos generando los reportes internacionales")
    conf_comp_venta     = models.ForeignKey(CondCompVentModel, default=1, on_delete=settings.DB_ON_DELETE_TRANS)

