# Generated by Django 4.0.5 on 2022-07-10 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_apps', '0006_alter_clasificacionesmenusmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='submenussistemasmodel',
            name='charger_function',
            field=models.CharField(default='Elegir funcion Adecuada', max_length=100),
        ),
    ]