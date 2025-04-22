import os
from Store.models import Product
from CoreAuth.models import Seller
from django.utils.text import slugify
import random


def get_unique_slug(base_slug):
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


folder_path = r"E:\electronics_product\downloaded_products"
products_dict = {}

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.jpeg',)):
        product_name = os.path.splitext(filename)[0]
        image_path = os.path.join("images/products", filename) 
        products_dict[product_name] = image_path

seller = Seller.objects.first()
count = 0

for name, image in products_dict.items():
    base_slug = slugify(name)
    unique_slug = get_unique_slug(base_slug)

    Product.objects.create(
        name=name,
        slug=unique_slug,
        price=round(random.uniform(50.0, 1500.0), 2),
        seller=seller,
        image=image,
        rate=random.randint(1, 5)
    )
    count += 1

