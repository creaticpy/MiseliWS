# Generated by Django 4.0.5 on 2022-07-01 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_userprofile_managers'),
        ('rrhh', '0007_delete_empleadosproxy_empleadosbocasproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleadosmodel',
            name='empleado_sucursal',
            field=models.ManyToManyField(blank=True, null=True, through='rrhh.EmpleadosSucursalesModel', to='base.sucursalesmodel'),
        ),
    ]
