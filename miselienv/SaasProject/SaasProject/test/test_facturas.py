import pytest
from aplicaciones.ventas.models import FacturasModel, ClientesModel
from django.utils.timezone import now


@pytest.mark.django_db(databases=['default',])
def test_fact_creations():
    facturas = FacturasModel.objects.create(
        fecha_documento=now(),
        nro_documento="0010010000001",
        fecha_transaccion=now(),
        observaciones="text observaciones",
        contado_credito="CONT",
        cotizacion=5000,
        monto_mon_local=100323000,
        saldo_mon_local=100323000,
        ruc="1271061",
        razon_social="Marco Rodrigues",
        cliente_id=1,
        dep_origen_id=1,
        conf_cuotas_id=None,
        moneda_id=1,
        tip_documento_id=1
    )
    asdf = ClientesModel.objects.all().count()
    print(asdf, "hola mundo")
    assert facturas.nro_documento.isnumeric()
    assert len(facturas.nro_documento) == 13
