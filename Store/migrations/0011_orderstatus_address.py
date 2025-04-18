# Generated by Django 5.2 on 2025-04-18 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_orderstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstatus',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.shippingaddress'),
        ),
    ]
