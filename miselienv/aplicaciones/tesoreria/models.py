from django.db import models

from aplicaciones.base.choices import entidadfinanciera

from aplicaciones.rrhh.models import PersonasModel
from django.conf import settings
from aplicaciones.base.models import BaseModel


class EntidadesFinancierasModel(BaseModel):
    persona             = models.OneToOneField(PersonasModel, on_delete=settings.DB_ON_DELETE_TRANS, blank=False, null=False)
    tipo_entidad        = models.CharField(choices=entidadfinanciera, max_length=100, blank=False, null=False, default='BANCO')
    observaciones       = models.CharField(max_length=1000, blank=True, null=True)
    oficial_cuentas     = models.ForeignKey(PersonasModel, blank=True, null=True, on_delete=settings.DB_ON_DELETE_TRANS, verbose_name="Oficial Ctas.", related_name='entfin_oficialcuentas')

    class Meta:
        verbose_name = "Entidad Financiera"
        verbose_name_plural = "Entidades Financieras"
