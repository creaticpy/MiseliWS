# Generated by Django 4.0.2 on 2022-03-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_alter_movimientosarticulosmodel_nro_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientosarticulosmodel',
            name='nro_documento',
            field=models.CharField(default='Cargar Nro Documento', help_text='Los Nros de documentos legales deben tener el siguiente formato: 0010010000001', max_length=100),
        ),
    ]
