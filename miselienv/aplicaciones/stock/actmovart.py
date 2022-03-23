from aplicaciones.stock.models import MovimientosArticulosModel


class ActMovArt:
    def __init__(self, instance, sender, *args, **kwargs):
        self.instance = instance
        self.sender   = sender
        self.args     = args
        self.kwargs   = kwargs
        self.actcab()

    def actcab(self):
        if MovimientosArticulosModel.objects.filter(tip_documento=self.instance.factura.tip_documento,
                                                    nro_documento=self.instance.factura.nro_documento).exists():
            if self.kwargs['kwargs']['evento'] == 'create':
                print('esto pasa si es create')
            elif self.kwargs['kwargs']['evento'] == 'update':
                print('esto pasa si es update')
        else:
            print('no existe nio la cabecera todavia')

        print('que se imprimio???', self.instance)
        print('que se imprimio???', self.sender)
        print('que se imprimio???', self.args)
        print('que se imprimio???', self.kwargs)

