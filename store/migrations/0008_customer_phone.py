# Generated by Django 5.1 on 2024-08-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_customer_phone_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
