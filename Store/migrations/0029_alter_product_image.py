# Generated by Django 5.2 on 2025-04-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Store", "0028_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, max_length=255, null=True, upload_to="images/products"
            ),
        ),
    ]
