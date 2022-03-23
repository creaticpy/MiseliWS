# Generated by Django 4.0.2 on 2022-02-24 21:49

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('finanzas', '0001_initial'),
        ('rrhh', '0001_initial'),
        ('stock', '0001_initial'),
        ('shared_apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientesModel',
            fields=[
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='rrhh.personasmodel')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='FacturasModel',
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
                ('nro_documento', models.CharField(max_length=100)),
                ('fecha_transaccion', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True)),
                ('contado_credito', models.CharField(choices=[('CONT', 'CONTADO'), ('CRED', 'CREDITO')], default='CONT', max_length=4)),
                ('cotizacion', models.PositiveIntegerField(default=0)),
                ('monto_mon_local', models.PositiveIntegerField(default=0)),
                ('saldo_mon_local', models.PositiveIntegerField(default=0)),
                ('ruc', models.CharField(default='', max_length=100)),
                ('razon_social', models.CharField(default='', max_length=100)),
                ('quepasaaqui', models.CharField(max_length=100)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.clientesmodel')),
                ('conf_cuotas', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='finanzas.confcuotasmodel', verbose_name='Cant. cuotas')),
                ('dep_origen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(app_label)s_%(class)sorig', to='stock.subdepositomodel')),
                ('moneda', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shared_apps.monedamodel')),
                ('tip_documento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shared_apps.tipdocumentodetmodel')),
            ],
            options={
                'verbose_name': 'factura',
                'verbose_name_plural': 'facturas',
            },
            managers=[
                ('object_by_sucursal', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='RecibosVentasModel',
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
                ('nro_documento', models.CharField(max_length=100)),
                ('fecha_transaccion', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(max_length=1000)),
                ('monto_mon_local', models.PositiveIntegerField()),
                ('saldo_mon_local', models.PositiveIntegerField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.clientesmodel')),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shared_apps.conceptosdocumentosmodel')),
                ('moneda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shared_apps.monedamodel')),
                ('tip_documento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shared_apps.tipdocumentodetmodel')),
            ],
            options={
                'verbose_name': 'recibo',
                'verbose_name_plural': 'recibos',
            },
            managers=[
                ('object_by_sucursal', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='VentasCuotasDetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('desc_corta', models.CharField(blank=True, max_length=100, null=True)),
                ('desc_larga', models.CharField(max_length=1000)),
                ('nro_item', models.IntegerField(default=0)),
                ('monto', models.PositiveIntegerField()),
                ('saldo', models.PositiveIntegerField(default=0)),
                ('fecha_vencimiento', models.DateField()),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.facturasmodel')),
            ],
            options={
                'verbose_name': 'Detalle de cuotas',
                'verbose_name_plural': 'Detalles de cuotas',
            },
        ),
        migrations.CreateModel(
            name='VentasRecibosCuotasModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('monto_aplicado_mon_local', models.PositiveIntegerField()),
                ('cuota', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.ventascuotasdetmodel')),
                ('recibo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.recibosventasmodel')),
            ],
            options={
                'verbose_name': 'm2m recibo cuota',
                'verbose_name_plural': 'M2m Recibos Cuotas',
            },
        ),
        migrations.CreateModel(
            name='RecibosDetModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('monto_mon_local', models.PositiveIntegerField()),
                ('saldo_mon_local', models.PositiveIntegerField()),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finanzas.cotizacionmodel')),
                ('forma_cobro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shared_apps.formaspagoscobrosmodel')),
            ],
            options={
                'verbose_name': 'detalle de recibo',
                'verbose_name_plural': 'Detalles de recibos',
            },
        ),
        migrations.CreateModel(
            name='FacturasDetModel',
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
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ventas.facturasmodel')),
                ('impuesto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='finanzas.impuestosdetmodel')),
            ],
            options={
                'verbose_name': 'Detalle Factura',
                'verbose_name_plural': 'Detalles de Facturas',
            },
        ),
        migrations.CreateModel(
            name='ConfVentasModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('precio_articulo', models.CharField(choices=[('UC', 'ULTIMA COMPRA'), ('UV', 'ULTIMA VENTA'), ('PR', 'PROMEDIO')], default='PR', max_length=100)),
                ('donde_mueve_stock', models.CharField(choices=[('RE', 'REMISION'), ('FA', 'FACTURA')], default='RE', help_text='Indicamos en que punto actualizamos el stock', max_length=2, verbose_name='Donde mueve stock')),
                ('circuito_obligatorio_desde', models.CharField(choices=[('PED', 'PEDIDO'), ('PRE', 'PRESUPUESTO'), ('REM', 'REMISION'), ('FAC', 'FACTURA')], default='PRE', help_text='Indicamos desde que punto el circuito es obligaorio', max_length=3, verbose_name='Obligatorio desde: ')),
                ('dep_origen', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='stock.subdepositomodel')),
                ('impuesto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='finanzas.impuestosdetmodel')),
                ('moneda', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shared_apps.monedamodel')),
            ],
            options={
                'verbose_name': 'Conf Ventas',
                'verbose_name_plural': 'Configuraciones de Ventas',
            },
        ),
        migrations.CreateModel(
            name='ClientesSucursalesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('desc_corta', models.CharField(blank=True, max_length=100, null=True)),
                ('fec_ingreso', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True)),
                ('telefono', models.CharField(blank=True, max_length=100, null=True)),
                ('direccion', models.CharField(max_length=1000)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ventas.clientesmodel')),
                ('encargado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rrhh.personasmodel', verbose_name='Encargado/a')),
            ],
            options={
                'verbose_name': 'cliente sucursal',
                'verbose_name_plural': 'Sucursales de los Clientes',
            },
        ),
        migrations.CreateModel(
            name='FacturasProxyModel',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ventas.facturasmodel',),
            managers=[
                ('object_by_sucursal', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='ventasreciboscuotasmodel',
            constraint=models.UniqueConstraint(fields=('recibo', 'cuota'), name='ventreccuoconstraint'),
        ),
        migrations.AddConstraint(
            model_name='ventascuotasdetmodel',
            constraint=models.UniqueConstraint(fields=('factura', 'nro_item'), name='ventascuotadetsconstraint'),
        ),
        migrations.AddConstraint(
            model_name='facturasdetmodel',
            constraint=models.UniqueConstraint(fields=('factura', 'nro_item'), name='facdetconstraint'),
        ),
        migrations.AddConstraint(
            model_name='clientessucursalesmodel',
            constraint=models.UniqueConstraint(fields=('cliente', 'desc_corta'), name='clisucconstraint'),
        ),
    ]
