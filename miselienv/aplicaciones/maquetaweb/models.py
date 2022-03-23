from django.db import models
from django.conf import settings
from core.models import BaseModel, Maestros, MaestrosDet
from aplicaciones.base.functions import cal_key


class SeccionesModel(Maestros, BaseModel):
    pass


class SubSeccionesModel(MaestrosDet, BaseModel):
    secciones = models.ForeignKey(SeccionesModel, on_delete=settings.DB_ON_DELETE_TRANS)

    # class Meta:
    #     unique_together = ("nro_item", "secciones")
    #
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     if self._state.adding:
    #         nro_item = cal_key(self.secciones, SubSeccionesModel, "secciones")
    #         self.nro_item = nro_item
    #     super(SubSeccionesModel, self).save(force_insert, force_update, using, update_fields)

# Secciones home, services, hoo I'm, contact...
# SubSecciones services/ limpieza de residencias, limpieza post obra, limpieza vidrios, etc
# SubSubSecciones services/ limpieza de residencias / promociones, paquetes diarios, etc.


class SubSubSeccionesModel(MaestrosDet, BaseModel):
    subsecciones = models.ForeignKey(SubSeccionesModel, on_delete=settings.DB_ON_DELETE_TRANS)


class TablasSeccionesModel(Maestros, BaseModel):
    subsubsecciones = models.ForeignKey(SubSubSeccionesModel, on_delete=settings.DB_ON_DELETE_TRANS)
    monto = models.PositiveIntegerField()


