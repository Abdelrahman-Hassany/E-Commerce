import os
import random
from django.core.files import File
from django.utils.text import slugify
from Store.models import Product
from CoreAuth.models import Seller

from pathlib import Path

folder_path = r"E:\electronics_product\downloaded_products"
seller = Seller.objects.first()

def get_unique_slug(base_slug):
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.jpeg')):
        product_name = os.path.splitext(filename)[0]
        cleaned_name = slugify(product_name)
        unique_slug = get_unique_slug(cleaned_name)

        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'rb') as f:
            django_file = File(f)
            product = Product(
                name=product_name,
                slug=unique_slug,
                price=round(random.uniform(50.0, 1500.0), 2),
                seller=seller,
                rate=random.randint(1, 5),
            )
            product.image.save(filename, django_file, save=True)  # ✅ هنا بيتم الحفظ فعليًا في media/
