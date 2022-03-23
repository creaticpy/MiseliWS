from aplicaciones.base.functions import nrossiguientes
from aplicaciones.finanzas.models import CotizacionModel, ConfFinanzasModel
from django.utils.timezone import now


class FacturasPrecargas:
    @staticmethod
    def cotizacion(v_fecha=None, v_moneda=None):
        if v_fecha and v_moneda:
            return \
            CotizacionModel.objects.filter(fecha__lte=v_fecha, moneda=v_moneda).order_by('-fecha').values('venta')[:1].get()['venta']
        else:
            return CotizacionModel.objects.filter(fecha__lte=now(), moneda=ConfFinanzasModel.objects
                                                  .values("moneda_secundaria")[:1]
                                                  ).order_by('-fecha').values('venta')[:1].get()['venta']

    @staticmethod
    def nextnumber(v_tipdoc):
        print(nrossiguientes(v_tipdoc))
