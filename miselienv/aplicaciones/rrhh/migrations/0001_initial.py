# Generated by Django 4.0.2 on 2022-02-24 21:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonasModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('personeria', models.CharField(blank=True, choices=[('F', 'Fisica'), ('J', 'Juridica')], max_length=100, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('apellido', models.CharField(blank=True, max_length=100, null=True)),
                ('razon_social', models.CharField(blank=True, max_length=200, null=True)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('ruc', models.CharField(blank=True, max_length=100, null=True)),
                ('dir_geo', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Ubicacion GPS')),
                ('sexo', models.CharField(blank=True, choices=[('F', 'Femenino'), ('M', 'Masculino')], max_length=100, null=True)),
                ('fecha_nac_const', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento/constitucion')),
                ('tipo_documento', models.CharField(blank=True, choices=[('RUC', 'Registro unico de contribuyente'), ('CI', 'Cedula de identidad'), ('DNI', 'Documento nacional de identidad')], max_length=100, null=True)),
                ('nro_documento', models.CharField(blank=True, max_length=100, null=True)),
                ('fec_venc_doc_iden', models.DateField(blank=True, null=True)),
                ('nro_celular', models.CharField(blank=True, max_length=100, null=True)),
                ('nro_whatsapp', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('userprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='userprofid', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
            },
        ),
        migrations.CreateModel(
            name='EmpleadosModel',
            fields=[
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('id', models.OneToOneField(db_column='id', on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='idpersona', serialize=False, to='rrhh.personasmodel')),
                ('fec_ingreso', models.DateField(default=django.utils.timezone.now)),
                ('fec_egreso', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contacto_emergencia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contactoemergencia', to='rrhh.personasmodel', verbose_name='Contacto de Emergencia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmpleadosSucursalesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuarioCreacion', models.CharField(editable=False, max_length=20, verbose_name='base.UserProfile')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('usuarioModificacion', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='base.UserProfile')),
                ('fechaModificacion', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('historico_cambios', models.JSONField(blank=True, default=dict, editable=False, null=True, verbose_name='Historico de actualizaciones del campo.')),
                ('estado', models.BooleanField(default=True)),
                ('borrado_logico', models.BooleanField(default=False, editable=False)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.sucursalesmodel')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rrhh.empleadosmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='empleadosmodel',
            name='empleado_sucursal',
            field=models.ManyToManyField(through='rrhh.EmpleadosSucursalesModel', to='base.SucursalesModel'),
        ),
    ]
