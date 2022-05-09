import factory
import pytest
from faker import Faker
from pytest_factoryboy import register

fake = Faker()

from inventory import models

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = fake.lexify(text="cat_name_??????")
    slug = fake.lexify(text="cat_name_??????")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    web_id = factory.Sequence(lambda n: "web_id_%d" % n)
    slug = fake.lexify(text="cat_name_??????")
    name = fake.lexify(text="cat_name_??????")
    description = fake.text()
    is_active = True
    created_at = "2022-05-05 07:01:23.840"
    updated_at = "2022-05-05 07:01:23.840"

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if extracted:
            for cat in extracted:
                self.category.add(cat)

class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductType

    name = factory.Sequence(lambda n: "type_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brand

    name = factory.Sequence(lambda n: "brand_%d" % n)

class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductInventory

    sku = factory.Sequence(lambda n: "sku_%d" % n)
    upc = factory.Sequence(lambda n: "upc_%d" % n)
    product_type = factory.SubFactory(ProductTypeFactory)
    product = factory.SubFactory(ProductFactory)
    brand = factory.SubFactory(BrandFactory)
    is_active = 1
    retail_price = 97
    store_price = 92
    sale_price = 46
    weight = 987

class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Media
    product_inventory = factory.SubFactory(ProductInventoryFactory)
    image = "images/cap.png"
    alt_text = "a default image solid color"
    is_feature = True

register(CategoryFactory)
register(ProductFactory)
register(ProductTypeFactory)
register(BrandFactory)
register(ProductInventoryFactory)
register(MediaFactory)