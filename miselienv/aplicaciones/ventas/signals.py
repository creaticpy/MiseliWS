from aplicaciones.ventas.models import FacturasModel, FacturasDetModel, ClientesModel, ClientesSucursalesModel
from django.db.models import F, Sum
from django.db.models.signals import post_delete, post_save
from aplicaciones.stock import actmovart


class FacturaDetSignal:
    @staticmethod
    def method_post_save(instance, sender, *args, **kwargs):
        # aqui actualizamos la cabecera - usamos el concepto de acumulador
        if kwargs['created']:  # entra si es insert
            factura = FacturasModel.objects.filter(id=instance.factura.id)
            factura.update(monto_mon_local=F('monto_mon_local') + instance.monto_mon_local)
        else:
            detalle_factura = sender.objects.filter(factura=instance.factura.id).aggregate(Sum('monto_mon_local'))
            factura = FacturasModel.objects.filter(id=instance.factura.id)
            factura.update(monto_mon_local=detalle_factura['monto_mon_local__sum'])

    @staticmethod
    def method_post_delete(instance, sender, *args, **kwargs):
        factura = FacturasModel.objects.filter(id=instance.factura.id)
        factura.update(monto_mon_local=F('monto_mon_local') - instance.monto_mon_local)


post_save.connect(FacturaDetSignal.method_post_save, sender=FacturasDetModel, dispatch_uid="post_saveFacturasDet")
post_delete.connect(receiver=FacturaDetSignal.method_post_delete, sender=FacturasDetModel)


# Esto fue incialmente para que el cliente no tuviera que estar cargando la primera sucursal
# class ClienteSignal:
#     @staticmethod
#     def method_post_save(instance, sender, *args, **kwargs):
#         if kwargs['created']:
#             if not ClientesSucursalesModel.objects.filter(cliente=instance)[:1].exists():
#                 asd = ClientesSucursalesModel.objects.create(cliente=instance,
#                                                              desc_corta=instance.persona.nombre,
#                                                              direccion=instance.persona.direccion,
#                                                              encargado=instance.persona,
#                                                              observaciones="",
#                                                              )
#                 asd.save()
#
#
# post_save.connect(ClienteSignal.method_post_save, sender=ClientesModel, dispatch_uid="post_saveClientesModel")