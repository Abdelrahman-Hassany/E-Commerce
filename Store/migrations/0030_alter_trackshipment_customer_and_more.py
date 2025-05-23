# Generated by Django 5.2 on 2025-04-22 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CoreAuth", "0002_alter_customer_user"),
        ("Store", "0029_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trackshipment",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="CoreAuth.customer",
            ),
        ),
        migrations.AlterField(
            model_name="trackshipment",
            name="seller",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="CoreAuth.seller",
            ),
        ),
    ]
