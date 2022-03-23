# Generated by Django 4.0.2 on 2022-03-02 13:41

import aplicaciones.ventas.Precargas
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_alter_movimientosarticulosmodel_dep_destino_and_more'),
        ('finanzas', '0004_remove_conffinanzasmodel_moneda_predeterminada_and_more'),
        ('rrhh', '0007_delete_empleadosproxy_empleadosbocasproxy'),
        ('shared_apps', '0001_initial'),
        ('ventas', '0009_alter_facturasmodel_dep_origen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidosmodel',
            name='realizado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rrhh.personasmodel'),
        ),
        migrations.AlterField(
            model_name='confventasmodel',
            name='circuito_obligatorio_desde',
            field=models.CharField(choices=[('PED', 'PEDIDO'), ('PRE', 'PRESUPUESTO'), ('REM', 'REMISION'), ('FAC', 'FACTURA')], default='PRE', help_text='Indicamos desde que punto el circuito es obligaorio', max_length=3, verbose_name='Obligatorio desde '),
        ),
        migrations.AlterField(
            model_name='pedidosmodel',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.clientessucursalesmodel'),
        ),
        migrations.CreateModel(
            name='RemisionesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('periodo', models.PositiveIntegerField(blank=True, null=True)),
                ('mes', models.PositiveIntegerField(blank=True, null=True)),
                ('fecha_documento', models.DateField(default=django.utils.timezone.now)),
                ('nro_documento', models.CharField(default='Cargar Nro Documento', help_text='Los Nros de documentos legales deben tener el siguiente formato: 0010010000001', max_length=100)),
                ('fecha_transaccion', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True)),
                ('contado_credito', models.CharField(choices=[('CONT', 'CONTADO'), ('CRED', 'CREDITO')], default='CONT', max_length=4)),
                ('cotizacion', models.PositiveIntegerField(default=aplicaciones.ventas.Precargas.FacturasPrecargas.cotizacion)),
                ('monto_mon_local', models.PositiveIntegerField(default=0)),
                ('ruc', models.CharField(default='', max_length=100)),
                ('razon_social', models.CharField(default='', max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.clientessucursalesmodel')),
                ('conf_cuotas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='finanzas.confcuotasmodel', verbose_name='Cant. cuotas')),
                ('dep_origen', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)sorig', to='stock.subdepositomodel')),
                ('moneda', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shared_apps.monedamodel')),
                ('tip_documento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shared_apps.tipdocumentodetmodel')),
            ],
            options={
                'verbose_name': 'Remision',
                'verbose_name_plural': 'Remisiones',
            },
        ),
        migrations.CreateModel(
            name='RemisionesDetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('desc_larga', models.CharField(max_length=1000)),
                ('nro_item', models.IntegerField(default=0)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio_unitario', models.PositiveIntegerField(default=0)),
                ('monto_mon_local', models.PositiveIntegerField(default=0)),
                ('monto_mon_ext', models.PositiveIntegerField(default=0)),
                ('Observaciones', models.CharField(blank=True, max_length=1000, null=True)),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock.articulosmodel')),
                ('impuesto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='finanzas.impuestosdetmodel')),
                ('remision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.remisionesmodel')),
            ],
            options={
                'verbose_name': 'Detalle Factura',
                'verbose_name_plural': 'Detalles de Facturas',
            },
        ),
        migrations.AddConstraint(
            model_name='remisionesdetmodel',
            constraint=models.UniqueConstraint(fields=('remision', 'nro_item'), name='remdetconstraint'),
        ),
    ]
