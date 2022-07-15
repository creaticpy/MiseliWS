from aplicaciones.base.choices import sino, estado
from django.db import models
from aplicaciones.base.models import BaseModel, UserProfile, SucursalesModel, Maestros
from django.conf import settings
from django.utils.timezone import now
from aplicaciones.base import choices
from django.core.exceptions import ValidationError
from core.models import DocumentosModel


class PersonasModel(DocumentosModel):
    personeria          = models.CharField(max_length=100, blank=True, null=True, choices=choices.personeria)
    nombre              = models.CharField(max_length=100, blank=True, null=True)
    apellido            = models.CharField(max_length=100, blank=True, null=True)
    razon_social        = models.CharField(max_length=200, blank=True, null=True)
    direccion           = models.CharField(max_length=200, blank=True, null=True)
    dir_geo             = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Ubicacion GPS")
    sexo                = models.CharField(max_length=100, blank=True, null=True, choices=choices.sexo)
    fecha_nac_const     = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento/constitucion")
    nro_celular         = models.CharField(max_length=100, blank=True, null=True)
    nro_whatsapp        = models.CharField(max_length=100, blank=True, null=True)
    email               = models.EmailField(max_length=100)
    tip_documento_pers  = models.ForeignKey('shared_apps.TipDocumentoDetModel', on_delete=settings.DB_ON_DELETE_TRANS, related_name='personas_tip_doc_pers')
    nro_documento_pers  = models.CharField(max_length=100, null=False, blank=False, default="CI/DNI, ETC",)  # Ej: para contratos CTS200/4 o facturas: 001-001-2020211
    fec_venc_doc_pers   = models.DateField(blank=True, null=True)
    fecha_transaccion   = models.DateField(default=now, null=True, blank=True)  # Fecha creacion_registro
    observaciones       = models.CharField(max_length=1000, null=True, blank=True)


    userprofile         = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS, related_name='userprofid')

    objects             = models.Manager()

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return '{id} {nombre} {apellido}'.format(id=self.id, nombre=self.nombre, apellido=self.apellido)

    def _permisos(self):
        # aqui pregunto los premisos especiales
        pass

    def nombreapellido(self):
        return '{nombre} - {apellido}'.format(nombre=self.nombre, apellido=self.apellido)
        # return f"{0}, {1}".format(self, self.nombre, self.apellido)


class EmpleadosSucursalesManager(models.Manager):
    # def get_queryset(self):
    #     return super().get_queryset().filter(empleado=1)

    def basic_filter(self, request):
        if UserProfile.object.get(is_superuser=True, email=request.user):
            return super().get_queryset().all()
        else:
            return super().get_queryset().filter(empleado=UserProfile.object.get(email=request.user).pk)


class EmpleadosSucursalesModel(BaseModel):
    empleado = models.ForeignKey('EmpleadosModel', on_delete=settings.DB_ON_DELETE_TRANS)
    sucursal = models.ForeignKey(SucursalesModel, on_delete=settings.DB_ON_DELETE_TRANS)

    objects = models.Manager()  # The default manager.
    filter_objects = EmpleadosSucursalesManager()

    def __str__(self):
        return '{sucursal} - {nombre} {apellido}'.format(sucursal=self.sucursal.desc_larga, nombre=self.empleado.id.nombre, apellido=self.empleado.id.apellido)

    def clean(self):
        count = EmpleadosSucursalesModel.objects.filter(empleado=self.empleado, estado=True).count()
        if self._state.adding:
            if count >= 1 and self.estado:
                raise ValidationError("Un empleado no puede estar activo en mas de 1 sucursal al mismo tiempo")
        else:
            if count >= 1 and self.estado:
                raise ValidationError("Un empleado no puede estar activo en mas de 1 sucursal al mismo tiempo:"
                                      " Primero cambie el estado a inactivo y luego prosiga a la activacion de este registro")
        super().clean()


class BeneficiosModel(Maestros):
    verbose_name = 'Beneficio'
    verbose_name_plural = 'Beneficios'


class EmpleadosBeneficiosModel(BaseModel):
    empleado = models.ForeignKey('EmpleadosModel', blank=False, null=False, on_delete=settings.DB_ON_DELETE_TRANS)
    beneficio = models.ForeignKey(BeneficiosModel, blank=False, null=False, on_delete=settings.DB_ON_DELETE_TRANS)

    class Meta:
        verbose_name = 'Empleado Beneficio'
        verbose_name_plural = 'Empleados Beneficios'


class EmpleadosModel(BaseModel):
    id                  = models.OneToOneField(PersonasModel, on_delete=settings.DB_ON_DELETE_TRANS, primary_key=True, db_column='id', related_name='idpersona')
    fecha_ingreso       = models.DateField(default=now, blank=False, null=False, editable=True)
    fecha_ingreso_ips   = models.DateField(default=now, blank=False, null=False, editable=True)
    fecha_egreso        = models.DateField(blank=True, null=True)
    email               = models.EmailField(blank=True, null=True, verbose_name="Correo Laboral")
    contacto_emergencia = models.ForeignKey(PersonasModel, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS, verbose_name='Contacto de Emergencia', related_name='contactoemergencia')
    empleado_sucursal   = models.ManyToManyField(SucursalesModel, through=EmpleadosSucursalesModel)
    beneficios = models.ManyToManyField(BeneficiosModel, through="EmpleadosBeneficiosModel")

    def __str__(self):
        return '{nombre} {apellido}'.format(nombre=self.id.nombre, apellido=self.id.apellido)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    # pagohoraextra = models.BooleanField(default=False, blank=False, null=False)
    # sucdeparsecc = models.ForeignKey(SucDeparSecc, on_delete=settings.DB_ON_DELETE_TRANS)
    # super(Entidad) validar, es para que despues recien cargue los atributos heredados





# este proxim es usado unicamente para que cada empleado
# pueda cambiar la boca con la cual estara trabajando
# esto es para no usar la clasica forma login por sucursal.
class EmpleadosBocasProxy(EmpleadosModel):
    class Meta:
        proxy = True
        verbose_name = "Empleado/boca"
        verbose_name_plural = "Empleados/Bocas"

