# Generated by Django 4.1.6 on 2023-02-04 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_alter_package_email_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracking',
            name='status',
            field=models.CharField(choices=[('A', 'Aceptado'), ('I', 'Iniciado'), ('T', 'En tránsito'), ('E', 'Entregado')], default='I', max_length=10, null=True, verbose_name='Estatus'),
        ),
    ]
