# Generated by Django 5.1 on 2024-08-16 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_zip_code_shippingaddress_zip_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='birth_of_date',
            new_name='Birth_of_date',
        ),
    ]