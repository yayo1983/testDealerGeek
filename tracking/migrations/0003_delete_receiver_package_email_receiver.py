# Generated by Django 4.1.6 on 2023-02-04 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_receiver_alter_tracking_package_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Receiver',
        ),
        migrations.AddField(
            model_name='package',
            name='email_receiver',
            field=models.EmailField(max_length=254, null=True, verbose_name='Correo'),
        ),
    ]
