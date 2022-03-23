import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SaasProject.SaasProject.settings")
import django
django.setup()

import time
import random as rd
from random import random
from django.utils.timezone import now
from aplicaciones.ventas.models import FacturasModel, ClientesModel


vocals = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'y', 'z',
              'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z']


def generate_string(length):
    if length <= 0:
        return False

    random_string = ''

    for i in range(length):
        decision = rd.choice(('vocals', 'consonants'))

        if random_string[-1:].lower() in vocals:
            decision = 'consonants'
        if random_string[-1:].lower() in consonants:
            decision = 'vocals'

        if decision == 'vocals':
            character = rd.choice(vocals)
        else:
            character = rd.choice(consonants)

        random_string += character

    return random_string


def generate_number():
    return int(random()*10+1)


def test_fact_creations(count):
    nro_documento = 0
    for i in range(count):
        nro_documento = nro_documento + 1

        FacturasModel.objects.create(
            fecha_documento=now(),
            nro_documento=str(nro_documento),
            fecha_transaccion=now(),
            observaciones="observaciones" + generate_string(generate_number()),
            contado_credito="CONT",
            cotizacion=5000,
            monto_mon_local=100323000,
            saldo_mon_local=100323000,
            ruc="1271061",
            razon_social=generate_string(generate_number()),
            cliente_id=1,
            dep_origen_id=1,
            conf_cuotas_id=None,
            moneda_id=1,
            tip_documento_id=1
        )


if __name__ == "__main__":
    print("Inicio de creación de población")
    print("Por favor espere . . . ")
    start = time.strftime("%c")
    print(f'Fecha y hora de inicio: {start}')
    test_fact_creations(100000)
    end = time.strftime("%c")
    print(f'Fecha y hora de finalización: {end}')
