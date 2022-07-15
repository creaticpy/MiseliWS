# Generated by Django 4.0.6 on 2022-07-14 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rrhh', '0013_empleadosmodel_fecha_ingreso_ips_and_more'),
        ('tesoreria', '0003_entidadesfinancierasmodel_persona_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidadesfinancierasmodel',
            name='oficial_cuentas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='entfin_oficialcuentas', to='rrhh.personasmodel', verbose_name='Oficial Ctas.'),
        ),
        migrations.AlterField(
            model_name='entidadesfinancierasmodel',
            name='persona',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='per_entidadfinanciera', to='rrhh.personasmodel'),
        ),
    ]