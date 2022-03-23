from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
# Create your models here.
import uuid
import getpass
from django.utils.timezone import now

exposed_request  = None


class BaseModel(models.Model):
    usuarioCreacion     = models.CharField(settings.AUTH_USER_MODEL, max_length=20, editable=False)
    fechaCreacion       = models.DateTimeField(auto_now_add=True, editable=False)
    usuarioModificacion = models.CharField(settings.AUTH_USER_MODEL, max_length=20, null=True, blank=True,
                                           editable=False)
    fechaModificacion   = models.DateTimeField(auto_now=True, db_index=True, null=True, blank=True, editable=False)
    historico_cambios   = models.JSONField(null=True, blank=True, default=dict, editable=False,
                                         verbose_name="Historico de actualizaciones del campo.")
    estado              = models.BooleanField(default=True)
    borrado_logico      = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            self.usuarioCreacion = (getpass.getuser())
        else:
            self.usuarioModificacion = (getpass.getuser())
        agregar_valor = {str(uuid.uuid1()): {
                            "fecha": str(now()),
                            "usuario": getpass.getuser(),
                                            }
                         }

        self.historico_cambios.update(agregar_valor)

        super(BaseModel, self).save(force_insert, force_update, using, update_fields)


class Maestros(BaseModel):
    desc_corta = models.CharField(max_length=100, unique=False, blank=True, null=True)
    desc_larga = models.CharField(max_length=1000, blank=False, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return '{desc_larga}'.format(desc_larga=self.desc_larga)


class MaestrosDet(Maestros):
    nro_item = models.IntegerField(default=0, blank=False, null=False, editable=True)

    class Meta:
        abstract = True


class PeriodosModel(BaseModel):
    periodo                 = models.PositiveIntegerField(null=True, blank=True)  # solo año 2022
    mes                     = models.PositiveIntegerField(null=True, blank=True)  # mes/año 012022 - 122023 -etc
    fecha_documento         = models.DateField(default=now)  # Fecha emision del documento

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.mes = self.fecha_documento.month
        self.periodo = self.fecha_documento.year
        super().save(force_insert, force_update, using, update_fields)


class DocumentosManager(models.Manager):

    def object_by_sucursal(self, request):
        if self.model.tip_documento.tip_comprobante == 'LE':
            pass


class DocumentosModel(PeriodosModel):
    tip_documento       = models.ForeignKey('shared_apps.TipDocumentoDetModel', on_delete=settings.DB_ON_DELETE_TRANS, default=1)
    nro_documento       = models.CharField(max_length=100, null=False, blank=False, default="Cargar Nro Documento",
                                           help_text="Los Nros de documentos legales deben tener el siguiente formato: 0010010000001")  # Ej: para contratos CTS200/4 o facturas: 001-001-2020211
    fecha_transaccion   = models.DateField(default=now, null=False, blank=False)  # Fecha creacion_registro
    observaciones       = models.CharField(max_length=1000, null=False, blank=False)

    object_by_sucursal  = DocumentosManager()

    class Meta:
        abstract = True


        #  todo esto debe ser filtrado por sucursal, debemos ver la manera de hacer que
        #   solo quien pertenezca a la sucursal correspondiente pueda ver el documento


#  todo siempre dep_origen indica salida de articulo, siempre dep_destino indica  entrada de articulo
class CabMovArticulosModel(DocumentosModel):
    dep_origen = models.ForeignKey('stock.SubDepositoModel', default=1, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS, related_name='%(app_label)s_%(class)sorig')
    dep_destino = models.ForeignKey('stock.SubDepositoModel',default=1, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS, related_name='%(app_label)s_%(class)sdest')
    observaciones = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        abstract = True
        constraints = [models.UniqueConstraint(fields=['tip_documento', 'nro_documento'], name='%(app_label)s_%(class)smovart')]

    def __str__(self):
        return '{tip_documento} {nro_documento} {fecha_documento} {dep_origen}'.format(tip_documento=self.tip_documento, nro_documento=self.nro_documento, fecha_documento=self.fecha_documento, dep_origen=self.dep_origen,)

    def clean(self):
        try:
            if self.dep_origen == self.dep_destino:
                raise ValidationError('El deposito de origen debe ser diferente al deposito destino')
        except:
            pass
        super().clean()


class MovArticulosDetModel(MaestrosDet):
    impuesto            = models.ForeignKey('finanzas.ImpuestosDetModel', on_delete=settings.DB_ON_DELETE_TRANS, default=1)
    articulo            = models.ForeignKey('stock.ArticulosModel', on_delete=settings.DB_ON_DELETE_TRANS)
    cantidad            = models.PositiveIntegerField(default=1)
    precio_unitario     = models.PositiveIntegerField(default=0)
    monto_mon_local     = models.PositiveIntegerField(default=0)
    monto_mon_ext       = models.PositiveIntegerField(default=0)
    Observaciones       = models.CharField(max_length=1000, blank=True, null=True)

    desc_corta          = ""

    class Meta:
        abstract = True
