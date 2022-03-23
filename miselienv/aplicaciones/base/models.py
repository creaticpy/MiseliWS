from aplicaciones.shared_apps.models import TipDocumentoDetModel
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .choices import sino
from django.conf import settings
from core.models import BaseModel, Maestros


class UserProfileManager(BaseUserManager):
    """Manager para perfiles de usuarios"""

    def create_user(self, email, name, password=None):
        """Crear Nuevo User Profile"""
        if not email:
            raise ValueError("Usuario debe tener Email")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin, BaseModel):
    """ Modelo Base de Datos para Usuarios en el Sistema """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserProfileManager()

    # USERNAME_FIELD A string describing the name of the field on the user model that is used as the unique identifier.
    # This will usually be a username of some kind, but it can also be an email address, or any other unique identifier.
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS A list of the field names that will be prompted for when creating a user via the createsuperuser
    # management command
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Obtener Nombre Completo"""
        return self.name

    def get_sort_name(self):
        """Obtener Nombre corto Completo"""
        return self.name

    def __str__(self):
        """ Retornar cadena representando nuestro usuario"""
        return self.email


class EmpresasModel(BaseModel):
    nombre_fantasia = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=45)

    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'

    def __str__(self):
        return '{nomfan} - {razonsocial}'.format(nomfan=self.nombre_fantasia, razonsocial=self.razon_social)


class SucursalesModel(Maestros):
    empresa = models.ForeignKey(EmpresasModel, on_delete=settings.DB_ON_DELETE_TRANS)
    direccion = models.CharField(max_length=100, verbose_name='Direccion')
    ubi_gps = models.CharField(max_length=100, verbose_name="GPS")
    esmatriz = models.CharField(max_length=2, default='SI', blank=False, null=False, choices=sino)

    class Meta:
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

    def __str__(self):
        return '{desc_corta} - {desc_larga}'.format(desc_corta=self.desc_corta, desc_larga=self.desc_larga)


class ConfBaseModel(BaseModel):
    pass

    def clean(self):
        if self._state.adding:
            if ConfBaseModel.objects.count() >= 1:
                from django.core.exceptions import ValidationError
                raise ValidationError('No puede haber mas de un registro por configuracion')
        super().clean()


class BocasEmpleadosModel(BaseModel):
    # -------------------> modelo BocasExpedicion/Empleados
    boca_expedicion = models.ForeignKey('BocasExpedicionModel', on_delete=settings.DB_ON_DELETE_TRANS)
    empleado        = models.ForeignKey('rrhh.EmpleadosModel', on_delete=settings.DB_ON_DELETE_TRANS)
    estado          = models.BooleanField(default=True, help_text="Indica cual es la sucursal/boca usadas en este momento")

    class Meta:
        constraints = [models.UniqueConstraint(fields=['boca_expedicion', 'empleado'], name='bocasempleadosconst')]


class BocasExpedicionModel(BaseModel):
    sucursal            = models.ForeignKey(SucursalesModel, on_delete=settings.DB_ON_DELETE_TRANS, default=1)
    nro_boca            = models.CharField(max_length=100, default="001")
    boca_empleado       = models.ManyToManyField('rrhh.EmpleadosModel',  through=BocasEmpleadosModel)

    def __str__(self):
        return '{sucursal} - {boca}'.format(sucursal=self.sucursal, boca=self.nro_boca)

    def nombresucursal(self):
        return self.sucursal.desc_larga

    class Meta:
        verbose_name        = "Boca de expedicion"
        verbose_name_plural = u"Bocas de Expedicion"
        constraints = [models.UniqueConstraint(fields=['sucursal', 'nro_boca'], name='sucbocaconst')]


class NumerosSiguientesModel(BaseModel):
    tip_documento   = models.ForeignKey(TipDocumentoDetModel, on_delete=settings.DB_ON_DELETE_TRANS)
    boca_expedicion = models.ForeignKey(BocasExpedicionModel, on_delete=settings.DB_ON_DELETE_TRANS)
    nro_documento   = models.PositiveIntegerField(default=1, blank=False, null=False)
    codigo_1        = models.CharField(max_length=100, blank=True, null=True)
    codigo_2        = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Nro. Siguiente'
        verbose_name_plural = 'Nros. Siguientes'
        constraints = [models.UniqueConstraint(fields=['tip_documento', 'boca_expedicion'], name='nrosigbocaexpconst'), ]

