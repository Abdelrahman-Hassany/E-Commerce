from Store.models import Product
from CoreAuth.models import Seller
from django.utils.text import slugify
from faker import Faker
import random

fake = Faker()

# اختار أي seller موجود في DB
seller = Seller.objects.first()

image = 'images/products/placeholder.png'

for i in range(20):
    name = fake.word().capitalize() + " " + fake.word().capitalize()
    Product.objects.create(
        name=name,
        slug=slugify(name),
        price=round(random.uniform(10.0, 500.0), 2),
        seller=seller,
        image=image,
        rate=random.randint(0, 5)
    )

print("✅ تمت إضافة بيانات وهمية بنجاح")
