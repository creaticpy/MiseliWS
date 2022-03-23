import uuid
from django.template import Library
from aplicaciones.base.models import EmpresasModel

register = Library()


@register.simple_tag
def simple_tag_uuid():
    v_uuid = uuid.uuid1()
    # print(str(v_uuid).strip(), len(str(v_uuid).strip()), len(str(v_uuid)), "--"+str(v_uuid)+"--", "<--------------------------")
    return str(v_uuid).strip()


@register.simple_tag
def nombre_empresa():
    return EmpresasModel.objects.all().values('razon_social')[0].get('razon_social')
