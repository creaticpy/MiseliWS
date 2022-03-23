from aplicaciones.base.models import NumerosSiguientesModel, BocasEmpleadosModel, UserProfile
from django.core.exceptions import ValidationError


def cal_key(modelo, fk_name, fk_value):
    filters = {fk_name: fk_value}
    try:
        present_keys = modelo.objects.filter(**filters).order_by('-nro_item').values("nro_item")[:1].get()["nro_item"]
        return present_keys + 1
    except modelo.DoesNotExist:
        return 1


def nrossiguientes(v_tip_documento):
    v_boca_expedicion = None

    if NumerosSiguientesModel.objects.filter(tip_documento=v_tip_documento, boca_expedicion=v_boca_expedicion).values("nro_documento")[:1].exists():
        return NumerosSiguientesModel.objects.filter(tip_documento=v_tip_documento, boca_expedicion=v_boca_expedicion).values("nro_documento")[:1].get()['nro_documento']
    else:
        pass
        # raise ValidationError("Debe configurar Nro siguiente")
