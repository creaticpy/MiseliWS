from django.core.exceptions import ValidationError
from aplicaciones.rrhh.models import PersonasModel
from aplicaciones.shared_apps.models import ConceptosDocumentosModel, FormasPagosCobrosModel, MonedaModel
from django.db import models
from core.models import BaseModel, Maestros, DocumentosModel, MovArticulosDetModel, CabMovArticulosModel, MaestrosDet
from aplicaciones.base.choices import precioartpredeterminado, dondemuevestock, obligatoriodesde, contadocredito
from aplicaciones.finanzas.models import CotizacionModel, ImpuestosDetModel
from aplicaciones.finanzas.models import ConfCuotasModel
from django.conf import settings
from aplicaciones.base.functions import cal_key
from django.utils.timezone import now
from .Precargas import FacturasPrecargas


class ConfVentasModel(BaseModel):
    moneda                      = models.ForeignKey(MonedaModel, default=1, on_delete=settings.DB_ON_DELETE_TRANS)
    impuesto                    = models.ForeignKey(ImpuestosDetModel, default=1, on_delete=settings.DB_ON_DELETE_TRANS)
    dep_origen                  = models.ForeignKey("stock.SubDepositoModel", default=1, on_delete=settings.DB_ON_DELETE_TRANS)
    precio_articulo             = models.CharField(max_length=100, default="PR", choices=precioartpredeterminado)
    donde_mueve_stock           = models.CharField(max_length=2, default="RE", choices=dondemuevestock, verbose_name="Donde mueve stock",
                                                   help_text="Indicamos en que punto actualizamos el stock")
    circuito_obligatorio_desde  = models.CharField(max_length=3, default="PRE",  choices=obligatoriodesde, verbose_name="Obligatorio desde ",
                                                   help_text="Indicamos desde que punto el circuito es obligaorio")
    # contado_con_recibo          = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Conf Ventas'
        verbose_name_plural = 'Configuraciones de Ventas'

    def __str__(self):
        return '{moneda}, {impuesto}, {dep_origen}, Tipo de calculo precio: {precio_articulo}'.format(moneda=self.moneda, impuesto=self.impuesto, dep_origen=self.dep_origen, precio_articulo=self.get_precio_articulo_display())

    def clean(self):
        if self._state.adding:
            if ConfVentasModel.objects.count() >= 1:
                raise ValidationError('No puede haber mas de un registro por configuracion')
        super().clean()


class ClientesModel(BaseModel):
    id      = models.OneToOneField(PersonasModel, db_column='id', primary_key=True, on_delete=settings.DB_ON_DELETE_TRANS)
    ruc     = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self):
        return '{nombre}, {apellido}'.format(nombre=self.id.nombre, apellido=self.id.apellido)


class ClientesSucursalesModel(Maestros):
    cliente         = models.ForeignKey(ClientesModel, on_delete=settings.DB_ON_DELETE_TRANS)
    fec_ingreso     = models.DateField(default=now, blank=False, null=False)
    observaciones   = models.CharField(max_length=1000, blank=True, null=True)
    telefono        = models.CharField(max_length=100, blank=True, null=True)
    direccion       = models.CharField(max_length=1000)
    encargado       = models.ForeignKey(PersonasModel, on_delete=settings.DB_ON_DELETE_TRANS, verbose_name="Encargado/a")

    desc_larga = ""

    class Meta:
        verbose_name        = 'cliente sucursal'
        verbose_name_plural = 'Sucursales de los Clientes'
        constraints = [models.UniqueConstraint(fields=['cliente', 'desc_corta'], name='clisucconstraint')]

    def __str__(self):
        return '{razon_social} - Suc: {desc_corta}'.format(razon_social=self.cliente.id.razon_social, desc_corta=self.desc_corta)


class PedidosModel(CabMovArticulosModel):
    cliente         = models.ForeignKey(ClientesSucursalesModel, on_delete=settings.DB_ON_DELETE_TRANS)
    moneda          = models.ForeignKey(MonedaModel, on_delete=settings.DB_ON_DELETE_TRANS, default=1)
    cotizacion      = models.PositiveIntegerField(default=FacturasPrecargas.cotizacion)  # todo por ahora cero, luego debe estirar de la tabla
    monto_mon_local = models.PositiveIntegerField(default=0)
    ruc             = models.CharField(max_length=100, default="")
    razon_social    = models.CharField(max_length=100, default="")
    realizado_por   = models.ForeignKey(PersonasModel, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS)

    dep_destino     = ""  # inhabilitamos depósito destino, ya que con ello indicaríamos que existe una entrada y una salida.

    class Meta:
        verbose_name        = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return 'Pedido de: {nombre} {apellido}'.format(nombre=self.cliente.cliente.id.nombre, apellido=self.cliente.cliente.id.apellido)

    def clean(self):
        if self.tip_documento.desc_corta != 'PER':
            raise ValidationError("El tipo de comprobante debe ser PER -> PEDIDO RECIBIDO")
        super().clean()


class PedidosDetModel(MovArticulosDetModel):
    pedido             = models.ForeignKey(PedidosModel, on_delete=settings.DB_ON_DELETE_REC)

    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalle de Pedidos'
        constraints = [models.UniqueConstraint(fields=['pedido', 'nro_item'], name='peddetconstraint')]

    def __str__(self):
        return '{pedido}'.format(pedido=self.pedido)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            # actualizamos nro_item
            self.nro_item = cal_key(PedidosDetModel, "pedido", self.pedido.id)
            # Actualizamos el detalle
            self.monto_mon_local = self.cantidad * self.precio_unitario
            self.monto_mon_ext = 0  # todo dejar asi mientras resolvemos moneda extranjera
        else:
            # Actualizamos el detalle
            self.monto_mon_local = self.cantidad * self.precio_unitario
            self.monto_mon_ext = 0  # todo dejar asi mientras resolvemos moneda extranjera
        super().save(force_insert, force_update, using, update_fields)


class PedidosRemisionesModel(BaseModel):
    pedido      = models.ForeignKey(PedidosDetModel, on_delete=settings.DB_ON_DELETE_TRANS)
    remision    = models.ForeignKey('RemisionesDetModel', on_delete=settings.DB_ON_DELETE_TRANS)
    cantidad    = models.PositiveIntegerField(default=0)


class RemisionesModel(CabMovArticulosModel):
    cliente         = models.ForeignKey(ClientesSucursalesModel, on_delete=settings.DB_ON_DELETE_TRANS)
    contado_credito = models.CharField(max_length=4, choices=contadocredito, default="CONT")
    conf_cuotas     = models.ForeignKey(ConfCuotasModel, blank=True, null=True, verbose_name="Cant. cuotas", on_delete=settings.DB_ON_DELETE_TRANS)
    moneda          = models.ForeignKey(MonedaModel, on_delete=settings.DB_ON_DELETE_TRANS, default=1)
    cotizacion      = models.PositiveIntegerField(default=FacturasPrecargas.cotizacion)  # todo por ahora cero, luego debe estirar de la tabla
    monto_mon_local = models.PositiveIntegerField(default=0)
    ruc             = models.CharField(max_length=100, default="")
    razon_social    = models.CharField(max_length=100, default="")

    objects         = models.Manager()
    dep_destino     = ""  # inhabilitamos depósito destino, ya que con ello indiciaríamos que existe una entrada y una salida.

    class Meta:
        verbose_name        = 'Remision'
        verbose_name_plural = 'Remisiones'

    def __str__(self):
        return 'Factura de: {nombre} {apellido}'.format(nombre=self.cliente.cliente.id.nombre, apellido=self.cliente.cliente.id.apellido)

    def clean(self):
        if not self.nro_documento.isnumeric():
            raise ValidationError('El Nro de documento debe ser completamente numerico')
        if self.tip_documento.tip_documento.id in (1, 2):  # documentos de compra y venta
            if len(self.nro_documento) != 13:
                raise ValidationError('Nro documento debe tener una longitud exacta de 13 digitos')
        if self.contado_credito == "CONT":
            if self.conf_cuotas:
                raise ValidationError("Los comprobantes al CONTADO no pueden tener cuotas")
        elif self.contado_credito == "CRED":
            if not self.conf_cuotas:
                raise ValidationError("Los comprobantes a CREDITO deben tener cuotas asignadas")
        super().clean()


class RemisionesDetModel(MovArticulosDetModel):
    remision    = models.ForeignKey(RemisionesModel, blank=False, null=False, on_delete=settings.DB_ON_DELETE_REC)
    pedido      = models.ManyToManyField(PedidosDetModel, through=PedidosRemisionesModel, related_name='pedidosremisiones')

    class Meta:
        verbose_name = 'Detalle de Remision'
        verbose_name_plural = 'Detalles de Remisiones'
        constraints = [models.UniqueConstraint(fields=['remision', 'nro_item'], name='remdetconstraint')]

    def __str__(self):
        return '{factura}'.format(factura=self.remision)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            # actualizamos nro_item
            self.nro_item = cal_key(RemisionesDetModel, "remision", self.remision.id)
            # Actualizamos el detalle
            self.monto_mon_local = self.cantidad * self.precio_unitario
            self.monto_mon_ext = 0  # todo dejar asi mientras resolvemos moneda extranjera
        else:
            # Actualizamos el detalle
            self.monto_mon_local = self.cantidad * self.precio_unitario
            self.monto_mon_ext = 0  # todo dejar asi mientras resolvemos moneda extranjera
        super().save()


class RemisionesFacturasModel(BaseModel):
    remision    = models.ForeignKey(RemisionesDetModel, blank=False, null=False, on_delete=settings.DB_ON_DELETE_TRANS)
    factura     = models.ForeignKey('FacturasDetModel', blank=False, null=False, on_delete=settings.DB_ON_DELETE_TRANS)
    cantidad    = models.PositiveIntegerField(blank=False, null=False, )


class FacturasModel(CabMovArticulosModel):
    cliente         = models.ForeignKey(ClientesModel, on_delete=settings.DB_ON_DELETE_TRANS)
    contado_credito = models.CharField(max_length=4, choices=contadocredito, default="CONT")
    conf_cuotas     = models.ForeignKey(ConfCuotasModel, blank=True, null=True, verbose_name="Cant. cuotas", on_delete=settings.DB_ON_DELETE_TRANS)
    moneda          = models.ForeignKey(MonedaModel, on_delete=settings.DB_ON_DELETE_TRANS, default=1)
    cotizacion      = models.PositiveIntegerField(default=FacturasPrecargas.cotizacion)  # todo por ahora cero, luego debe estirar de la tabla
    monto_mon_local = models.PositiveIntegerField(default=0)
    saldo_mon_local = models.PositiveIntegerField(default=0)
    ruc             = models.CharField(max_length=100, default="")
    razon_social    = models.CharField(max_length=100, default="")

    objects         = models.Manager()
    dep_destino     = ""  # inhabilitamos deposito destino ya que con ello indicariamos que existe una entrada y una salida.

    class Meta:
        verbose_name        = 'factura'
        verbose_name_plural = 'facturas'

    def __str__(self):
        return 'Factura de: {nombre} {apellido}'.format(nombre=self.cliente.id.nombre, apellido=self.cliente.id.apellido)

    def clean(self):
        FacturasPrecargas.nextnumber(self.tip_documento)
        if not self.nro_documento.isnumeric():
            raise ValidationError('El Nro de documento debe ser completamente numerico')
        if self.tip_documento.tip_documento.id in (1, 2):  # documentos de compra y venta
            if len(self.nro_documento) != 13:
                raise ValidationError('Nro documento debe tener una longitud exacta de 13 digitos')
        if self.contado_credito == "CONT":
            if self.conf_cuotas:
                raise ValidationError("Los comprobantes al CONTADO no pueden tener cuotas")
        elif self.contado_credito == "CRED":
            if not self.conf_cuotas:
                raise ValidationError("Los comprobantes a CREDITO deben tener cuotas asignadas")
        super().clean()


class FacturasProxyModel(FacturasModel):
    class Meta:
        proxy = True


class FacturasDetModel(MovArticulosDetModel):
    factura             = models.ForeignKey(FacturasModel, on_delete=settings.DB_ON_DELETE_REC)
    remision            = models.ManyToManyField(RemisionesDetModel, through=RemisionesFacturasModel, related_name='remisionesfacturas')
    class Meta:
        verbose_name = 'Detalle Factura'
        verbose_name_plural = 'Detalles de Facturas'
        constraints = [models.UniqueConstraint(fields=['factura', 'nro_item'], name='facdetconstraint')]

    def __str__(self):
        return '{factura}'.format(factura=self.factura)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            # actualizamos nro_item
            self.nro_item = cal_key(FacturasDetModel, "factura", self.factura.id)
            # Actualizamos el detalle
            self.monto_mon_local = self.cantidad * self.precio_unitario
            self.monto_mon_ext = 0  # todo dejar asi mientras resolvemos moneda extranjera
        else:
            # Actualizamos el detalle
            self.monto_mon_local = self.cantidad * self.precio_unitario
            self.monto_mon_ext = 0  # todo dejar asi mientras resolvemos moneda extranjera
        super(FacturasDetModel, self).save(force_insert, force_update, using, update_fields)


class VentasCuotasDetModel(MaestrosDet):
    factura             = models.ForeignKey(FacturasModel, on_delete=settings.DB_ON_DELETE_TRANS)
    monto               = models.PositiveIntegerField()
    saldo               = models.PositiveIntegerField(default=0)
    fecha_vencimiento   = models.DateField()

    class Meta:
        verbose_name = 'Detalle de cuotas'
        verbose_name_plural = 'Detalles de cuotas'
        constraints = [models.UniqueConstraint(fields=['factura', 'nro_item'], name='ventascuotadetsconstraint')]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            self.nro_item = cal_key(VentasCuotasDetModel, "factura", self.factura.id)

        super(VentasCuotasDetModel, self).save(force_insert, force_update, using, update_fields)


# unimos cabecera de recibos con el detalle de las cuotas.
class RecibosVentasModel(DocumentosModel):
    cliente           = models.ForeignKey(ClientesModel, on_delete=settings.DB_ON_DELETE_TRANS)
    concepto          = models.ForeignKey(ConceptosDocumentosModel, on_delete=settings.DB_ON_DELETE_TRANS)
    moneda            = models.ForeignKey(MonedaModel, on_delete=settings.DB_ON_DELETE_TRANS)
    monto_mon_local   = models.PositiveIntegerField()
    saldo_mon_local   = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'recibo'
        verbose_name_plural = 'recibos'


# todo necesitamos el detalle ya que podemos tener mas de una forma de pago en un solo recibo.
class RecibosDetModel(BaseModel):
    forma_cobro     = models.ForeignKey(FormasPagosCobrosModel, on_delete=settings.DB_ON_DELETE_TRANS)
    cotizacion      = models.ForeignKey(CotizacionModel, on_delete=settings.DB_ON_DELETE_TRANS)
    monto_mon_local = models.PositiveIntegerField()
    saldo_mon_local = models.PositiveIntegerField()

    class Meta:
        verbose_name = "detalle de recibo"
        verbose_name_plural = "Detalles de recibos"


class VentasRecibosCuotasModel(BaseModel):
    recibo                    = models.ForeignKey(RecibosVentasModel, on_delete=settings.DB_ON_DELETE_TRANS)
    cuota                     = models.ForeignKey(VentasCuotasDetModel, on_delete=settings.DB_ON_DELETE_TRANS)
    monto_aplicado_mon_local  = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'm2m recibo cuota'
        verbose_name_plural = 'M2m Recibos Cuotas'
        constraints = [models.UniqueConstraint(fields=['recibo', 'cuota'], name='ventreccuoconstraint')]