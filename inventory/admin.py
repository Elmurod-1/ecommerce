from django.contrib import admin
from . import models

admin.site.register([
    models.Category,
    models.Product,
    models.Brand,
    models.ProductType,
    models.ProductInventory,
    models.Media,
    models.ProductAttribute,
    models.ProductAttributeValue,
    models.ProductAttributeValues,
    models.Stock
])
