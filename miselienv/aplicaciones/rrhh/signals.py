from aplicaciones.rrhh.models import EmpleadosSucursalesModel
from django.db.models.signals import post_delete, post_save
from django.core.exceptions import ValidationError


# class EmpleadosSucursalesValidaciones:
#     @staticmethod
#     def method_post_save(instance, sender, *args, **kwargs):
#
#         try:
#             if sender.objects.filter(empleado=instance.empleado, estado=True).count() > 1:
#                 raise ValidationError("Un empleado no puede estar activo en mas de 1 sucursal al mismo tiempo")
#         except ValidationError:
#             print("noseqeu ahcer con el errro")
#
#
# post_save.connect(EmpleadosSucursalesValidaciones.method_post_save, sender=EmpleadosSucursalesModel, dispatch_uid="post_saveEmpleadosSucursalesModel")
#
